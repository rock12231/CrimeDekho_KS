import os
import cv2 
import fitz 
import json
import textwrap
import http.client
import pytesseract
import numpy as np
import pandas as pd
from PIL import Image
from io import BytesIO
from base64 import b64encode
from django.views import View
import google.generativeai as genai
from langchain import OpenAI
from langchain.chains import RetrievalQA
from langchain_community.llms import OpenAI
from langchain_community.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from django.shortcuts import render, redirect 
from django.core.files.storage import FileSystemStorage
from CrimeMapping.views import getstaticmap
from CrimeMapping.models import PoliceStationList, PoliceStationJaipurList, FirData

from dotenv import load_dotenv
load_dotenv()

dfp = pd.DataFrame(PoliceStationJaipurList.objects.all().values())
dfp=dfp.dropna()
ndf = pd.DataFrame(PoliceStationList.objects.all().values())

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

class FIR(View):

    def get(self, request):
        if request.user.is_authenticated:    
            return render(request, 'FIR/firdata.html')    
        return redirect('/login')


class Addcrime(View):

    def get(self, request):
        if request.user.is_authenticated:
            crime_last_record = FirData.objects.order_by('-id')[0]
            police_record = PoliceStationJaipurList.objects.all().values()
            police_station = []
            for station in range(len(police_record)):
                police_station.append(police_record[station]['Police_Station'])
            context = {
                'map':getstaticmap(400,None),
                'crime_last_record':crime_last_record,
                'police_station':police_station 
                }
            return render(request, 'FIR/addcrime.html',context)    
        return redirect('/login')

    def wrap_text_preserve_newlines(self, text, width=110):
        # Split the input text into lines based on newline characters
        lines = text.split('\n')
        # Wrap each line individually
        wrapped_lines = [textwrap.fill(line, width=width) for line in lines]
        # Join the wrapped lines back together using newline characters
        wrapped_text = '\n'.join(wrapped_lines)
        return wrapped_text

    def process_llm_response(self, llm_response):
        ipc_section = self.wrap_text_preserve_newlines(llm_response['result'])
        print(ipc_section)
        return ipc_section

    def post(self, request):
        if request.method=='POST':
                crime_last_record = FirData.objects.order_by('-id')[0]                
                police_record = PoliceStationJaipurList.objects.all().values()
                police_station = []
                for station in range(len(police_record)):
                    police_station.append(police_record[station]['Police_Station'])
        if request.method == 'POST' and request.FILES.get('pdf_file'):
            fs = FileSystemStorage()
            lang: str = request.POST['language']
            text: str = ''
            pdf: bool = True
            genai.configure(api_key=os.getenv('API_KEY'))
            generation_config = {
              "temperature": 0.5,
              "top_p": 1,
              "top_k": 1,
              "max_output_tokens": 2048,
            }
            model = genai.GenerativeModel(model_name="gemini-pro", generation_config=generation_config)

            pdf_file = request.FILES['pdf_file']
            filename = fs.save(pdf_file.name, pdf_file)
            pdf_path = fs.url(filename)
            pdf_path_local = fs.path(filename)
            _, file_extension = os.path.splitext(pdf_path_local)

            if file_extension ==".pdf":
                pdf_document = fitz.open(pdf_path_local)
                for page_number in [0, len(pdf_document)-1]:
                    page = pdf_document.load_page(page_number)    
                    image_list = page.get_images(full=True)
                    for image_index, img in enumerate(image_list):
                        xref = img[0]
                        base_image = pdf_document.extract_image(xref)
                        image_bytes = base_image["image"]
                        
                        nparr = np.frombuffer(image_bytes, np.uint8)
                        cvimg = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
                        
                        if cvimg.shape[-1] == 3:  # Assuming BGR image
                            gray_image = cv2.cvtColor(cvimg, cv2.COLOR_BGR2GRAY)
                        else:
                            gray_image = cvimg
                        threshold_image = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
                        kernel = np.ones((3, 3), np.uint8)
                        processed_image = cv2.morphologyEx(threshold_image, cv2.MORPH_OPEN, kernel)
                        smoothed_image = cv2.GaussianBlur(processed_image, (5, 5), 0)
                        equalized_image = cv2.equalizeHist(smoothed_image)
                        # Save the grayscale image
                        image_filename = fs.save(f"images/image{page_number + 1}_{image_index + 1}.png", BytesIO(cv2.imencode('.png', equalized_image)[1].tobytes()))
                        image_path = fs.path(image_filename)
                        image = Image.open(image_path)
                        text += pytesseract.image_to_string(image, config=r'--psm 3 -l eng+hin')
                        fs.delete(image_filename)
            else:
                pdf = False
                pdf_file = request.FILES['pdf_file']
                filename = fs.save(pdf_file.name, pdf_file)
                pdf_path_local = fs.path(filename)
                f=open(pdf_path_local,"rb")
                enc=b64encode(f.read())
                f.close()
                # Convert the byte string to a string using the str() constructor
                audio = str(enc, encoding='utf-8')
                conn = http.client.HTTPSConnection("dhruva-api.bhashini.gov.in")
                payload = json.dumps({
                "pipelineTasks": [
                    {
                    "taskType": "asr",
                    "config": {
                        "language": {
                        "sourceLanguage": "hi"
                        },
                        "serviceId": "ai4bharat/conformer-hi-gpu--t4",
                        "audioFormat": "mp3",
                        "preProcessors": ["vad"],
                        "postProcessors": ["itn", "punctuation"],
                        "samplingRate": 16000
                    }
                    }
                ],
                "inputData": {
                    "audio": [
                    {
                        "audioContent": str(audio)
                    }]
                }
                })
                headers = {
                'Accept': ' */*',
                'User-Agent': ' Thunder Client (https://www.thunderclient.com)',
                'Authorization': 'AMTefwBuJRIk11yYf06Oj9zoWG_RKWkoj2gfO2U0BypjiaBohj3eV_Atp-Uc2E05',
                'Content-Type': 'application/json'
                }
                conn.request("POST", "/services/inference/pipeline", payload, headers)
                res = conn.getresponse()
                data = res.read()
                data = data.decode("utf-8")
                text = json.loads(data)
                fs.delete(filename)

            if lang=='eng':
                lang = 'English'
                prompt = [
                f"""You are a professional Police Officer based in Rajasthan from India, Your task is to convert the Context FIR into the JSON format,
                having the headers - case_no, date, police_station, ipc, ipc_no, time, CrPC, date_happened, date_reported, format_fir_type, address, distance_police_station, 
                name, father_name, age, nationality, office_address, additional_info,  suspected_individual, location, case_description.
                Include complete description for ipc for ipc header and just the ipc number for ipc_no header.
                Always remeber to convert the Context FIR to English language if it has other language.
                Put the values from the Context FIR for the respective key holder in English only. If relevant answer is not found, then don't include that header in json. 
                JSON key and value both must be as string only. Never include backslash.
                The Context FIR provided might be in Hindi Language but the json output must be strictly in English language only.
                Don't generate the answer strictly follow the below context. Provide Json Format for given text of Context FIR.
                Context FIR - {text} 

                --- Provide Json Format for given the provided Context FIR. Everything should be in english.  
                """
                ]
            else:
                lang = 'Hindi'
                prompt = [
                f"""You are a professional Police Officer based in Rajasthan from India, Your task is to convert the Context FIR into the JSON format,
                having the headers - case_no, date, police_station, ipc, ipc_no, time, CrPC, date_happened, date_reported, format_fir_type, address, distance_police_station, 
                name, father_name, age, nationality, office_address, additional_info,  suspected_individual, location, case_description.
                Include complete description for ipc for ipc header and just the ipc number for ipc_no header.
                Put the values from the Context FIR for the respective key holder in Hindi only. If relevant answer is not found, then don't include that header in json. 
                JSON key and value both must be as string only. Key must be in English and value should be in hindi only. Never include backslash.
                Don't generate the answer strictly follow the below context. Provide Json Format for given text of Context FIR.
                Context FIR - {text} 

                --- Provide Json Format for given the provided Context FIR.
                """
                ]
            try:
                response = model.generate_content(prompt)
                fir_data = str(response.text)
            except(Exception):
                context = {
                    "error": "Please try again (Check your Internet)"
                }
                return render(request, 'FIR/addcrime.html', context) 

            while fir_data[0]!='{':
                fir_data = fir_data[1:]
            while fir_data[-1]!='}':
                fir_data = fir_data[:len(fir_data)-1]
            fir_data = json.loads(fir_data)
            fir_data = {key: value for key, value in fir_data.items() if value is not None}

            context = {
                'map':getstaticmap(400,None),
                'crime_last_record':crime_last_record,
                'pdf_name': filename,
                'fir_details': fir_data,
                'filename': filename, 
                'language': lang,
                'pdf': pdf,
                'police_station': police_station
            }

            if 'pdf' in request.POST:
                context['pdf_path'] = pdf_path
            return render(request, 'FIR/addcrime.html', context)   
                        
        elif request.method == 'POST' and 'save' in request.POST:
            fs = FileSystemStorage()
            data = {
                'case_no' : request.POST['case_no'],	
                'date' : request.POST['date'],
                'police_station': request.POST['police_station'],
                'ipc_no' : request.POST['ipc_no'],
                'ipc' : request.POST['ipc_desc'],
                'time': request.POST['time'],
                'CrPC': request.POST['CrPC'],
                'date_happened' : request.POST['date_happened'],	
                'date_reported' : request.POST['date_reported'],
                'format_fir_type' : request.POST['format_fir_type'],
                'address' : request.POST['address'],
                'distance_police_station': request.POST['distance_police_station'],
                'name': request.POST['name'],
                'father_name': request.POST['father_name'],
                'age': request.POST['age'],
                'nationality': request.POST['nationality'],
                'office_address': request.POST['office_address'],
                'suspected_individual': request.POST['suspected_individual'],
                'latitude': request.POST['latitude'],
                'longitude': request.POST['longitude'],
                'additional_info': request.POST['additional_info'],
                'file': 'https://home.rajasthan.gov.in/content/dam/homeportal/anticorruptionbureaudepartment/FIR-2023/'+request.POST['filename'],
                'language': request.POST['language']
            }
            FirData.objects.create(**data)
            crime_last_record = FirData.objects.order_by('-id')[0]
            context = {
                'map':getstaticmap(400,None),
                'crime_last_record':crime_last_record,
                'police_station': police_station
                }
            fs.delete(request.POST['filename'])
            return render(request, 'FIR/addcrime.html',context)
        
        elif request.method=='POST' and 'formPredict' in request.POST:
            # IPC Prediction throguh the embedding model
            model_name = "sentence-transformers/all-mpnet-base-v2"
            instructor_embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': False}
            )

            embedding = instructor_embeddings
            persist_directory='FIR/data/db'
            vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)
            retriever = vectordb.as_retriever(search_kwargs={"k": 3})
            qa_chain = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=retriever, return_source_documents=True)
            crime_desc = request.POST['crime_desc'] 
            query = f"""You're a Rajasthan Police Department Official and tasked to evaluate the context FIR.

                    -- Provide the answer on the Context Indian FIR Case by providing the IPC Section, Court, Bailable, Cognizable, Offence, Punishment. 
                    Consider the Context Indian FIR as single case and give single answer. 
                    Answer must be in Json format only. Follow Json Rules. Never use slashes or new line characters etc in the json output.

                    Context Indian FIR -
                    {crime_desc}

                    Example Output answer in Json Format to follow for the respective Context Indian FIR - 
                    {{
                        "ipc_sec_pred":"237",
                        "court_pred":"Court of Session",
                        "bailable_pred":"Bailable",
                        "cognizable_pred":"Non-Cognizable",
                        "offence_pred":"Import or export of counterfeit coin, knowing the same to be counterfeit",
                        "punishment_pred":"3 Years + Fine"
                    }}
                    """
            
            llm_response = qa_chain(query)
            result_ipc=self.process_llm_response(llm_response)
            predicted_dict = json.dumps(result_ipc)
            predicted_dict = json.loads(result_ipc)
            
            context = {
                'map':getstaticmap(400,None),
                'crime_last_record':crime_last_record,
                'prediction': predicted_dict,
                'police_station': police_station,
                'crime_description': crime_desc
                }
            return render(request, 'FIR/addcrime.html',context)

        return redirect('/add-crime')

  
class Policestations(View):

    def get(self, request):
        if request.user.is_authenticated:
            tempDF = dfp.copy()
            # tempDF['Date']=tempDF['Date'].astype(str)
            police_last_record = PoliceStationJaipurList.objects.order_by('-id')[0]
            JSONdataPolice =json.dumps(tempDF.to_dict('records'))
            context ={
                'map':getstaticmap(400,None),
                'police_last_record':police_last_record,
                'JSONdataPolice':JSONdataPolice
                }
            return render(request, 'FIR/policestations.html', context)    
        return redirect('/login')
        
    def post(self, request):
        if request.method == 'POST':
            tempDF = dfp.copy()
            # tempDF['Date']=tempDF['Date'].astype(str)
            police_last_record = PoliceStationJaipurList.objects.order_by('-id')[0]
            JSONdataPolice =json.dumps(tempDF.to_dict('records'))
            data = {
                'map':getstaticmap(400,None),
                'police_last_record':police_last_record,
                'JSONdataPolice':JSONdataPolice,
                'district' : int(request.POST['district']),	
                'disname' : request.POST['disname'],
                'address' : request.POST['address'],
                'city' : request.POST['city'],
                'zip' : int(request.POST['zip']),
                'website' :  request.POST['website'],
                'latitude' : float(request.POST['latitude']),
                'longitude' : float(request.POST['longitude']),
            }
            PoliceStationList.objects.create(**data)