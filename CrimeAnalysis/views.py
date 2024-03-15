import os
import re
import json
import pandas as pd
from langchain import OpenAI
from django.views import View
from dotenv import load_dotenv
from datetime import datetime
from CrimeMapping.views import crime
from CrimeMapping.models import FirData
from django.shortcuts import render, redirect
from langchain_experimental.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent

load_dotenv()

rjdf = pd.DataFrame(FirData.objects.all().values())
ukdf = pd.read_csv("CrimeMapping/data/UK-Dataset-Final.csv", on_bad_lines='skip' )

class CrimeAnalysis(View):
    
    def get(self, request):
        if request.user.is_authenticated:    
            # tempDF = ukdf.copy()
            # tempDF['Arrest'] = tempDF['Arrest'].map({True: 'True', False: 'False'})
            # tempDF['Domestic'] = tempDF['Domestic'].map({True: 'True', False: 'False'})
            # tempDF['Date']=tempDF['Date'].astype(str)
            # Samp=tempDF[tempDF["Community_area"]==""]

            # Q1 Which Type of Crime is most recorded ?
            # crime['Type'] = tempDF["Type"].unique()
            # crime['Where'] = tempDF["Where"].unique()
            # crime['District'] = tempDF["District"].unique()
            # q1=tempDF.Type.value_counts().rename_axis('Crime_Type').reset_index(name='counts')
            # df_type=list(q1["Crime_Type"].head(13))
            # type_count=list(q1["counts"].head(13))
    
            # Q1 Most Frequent Time of FIR Reported to the Station
            tempDF1= rjdf.copy()
            tempDF1['time'] = pd.to_datetime(tempDF1['time'], errors='coerce')
            tempDF1['hour'] = tempDF1['time'].dt.hour
            fir_counts = tempDF1['hour'].value_counts().sort_index()
            # Assuming 'fir_counts is your DataFrame
            df_type = fir_counts.index.tolist()
            type_count = fir_counts.values.flatten().tolist() 
            




            #Object of Array (Dictionary) for Different Questions representation in analytics
            #Use Js Ternary Operator
            # Q2 Where most no. of crimes are recorded?
            # Top 5 place where 
            # q2=tempDF.Where.value_counts().rename_axis('Where_Type').reset_index(name='counts')
            # df_type2=list(q2["Where_Type"].head(5))
            # type_count2=list(q2["counts"].head(5))


            # Q2 Which Day most no. of FIR's are reported
            tempDF1['date'] = tempDF1['date'].replace('.', '-')
            tempDF1['date'] = pd.to_datetime(tempDF1['date'], errors='coerce')
            tempDF1.sort_values(by='date', inplace=True)
            
            fir_counts2 = tempDF1['date'].dt.date.value_counts().sort_index()
            # Assuming 'df' is your DataFrame and 'date' is your column
            

            dates = fir_counts2.index.tolist()
            type_count2 = fir_counts2.values.flatten().tolist() 
            df_type2 = [date.strftime('%Y-%m-%d') for date in dates]


            # Q3 Which IPC Section is most recorded in FIR
            counts_ipc = tempDF1['ipc_no'].value_counts()
            df_type3 = counts_ipc.index.tolist()
            type_count3 = counts_ipc.values.flatten().tolist()




            #Q4 Age Distribution of the victim reported in the FIR Records
            tempDF2= rjdf.copy()
            tempDF2['age'] = tempDF2['age'].apply(lambda x: ''.join(re.findall('\d+', str(x))))
            tempDF2['age'] = pd.to_numeric(tempDF2['age'])
            tempDF2['age']=tempDF2['age'].dropna()
            counts = tempDF2['age'].value_counts()
            print(counts)
            df_type4 = counts.index.tolist()
            type_count4 = counts.values.tolist()





            # #Which Type of Crime is more and arrest is done?
            # df_arrest=tempDF[tempDF["Arrest"]=="True"]
            # q3=df_arrest.Type.value_counts().rename_axis('Crime_Type1').reset_index(name='counts')
            # df_type3=list(q3["Crime_Type1"].head(5))
            # type_count3=list(q3["counts"].head(5))
            '''
            # Q4 On which day of week; the crime is more?
            df_type4=['Monday','Tuesday','Wednesday',  'Thursday', 'Friday', 'Saturday', 'Sunday']
            type_count4=tempDF.groupby([tempDF.index.dayofweek]).size()
            print("*******", type_count4)
    
            # Q5 In which month, most no. of crime is recorded?

            df_type5=['Jan','Feb','Mar',  'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            type_count5=tempDF.groupby([tempDF.index.month]).size()
            '''
            # On page load graph will be shown
            df_typeAll=list(tempDF2["ipc_no"].unique())
            type_countAll=[]
            for x in range(len(tempDF2.ipc_no.value_counts())):
                type_countAll.append(int(tempDF2.ipc_no.value_counts()[x]))
            dataX = type_countAll
            dataY = df_typeAll
        
            #tempDF.drop("Arrest", inplace=True, axis=1)
            #tempDF.drop("Domestic", inplace=True, axis=1)
            # dumbdata = tempDF.to_dict('records')
            # print(tempDF.to_dict('records'))
            # JSONdata =json.dumps(rjdf.to_dict('records'))
            data_dict = rjdf.to_dict('records')
            JSONdata = json.dumps(data_dict, ensure_ascii=False)
            print('''
            *****************
            *****************
            *****************
            *****************
            ''', type_count)
            print(df_type)
            print('''
            *****************
            *****************
            *****************
            *****************
            ''', type_count2)
            print(df_type2)
            print('''
            *****************
            *****************
            *****************
            *****************
            ''', type_count3)
            print(df_type3)
            print('''
            *****************
            *****************
            *****************
            *****************
            ''', type_count4)
            print(df_type4)
            # dataT = str(tempDF.values.tolist())
            data = [
                {
                'title': 'Most Frequent Time of FIR Reported to the Station',
                'dataX': type_count,
                'dataY': df_type
                },
                {
                'title': 'Which Day most no. of FIRs are reported',
                'dataX': type_count2,
                'dataY': df_type2
                },
                {
                'title': 'Which IPC Section is most recorded in FIR',
                'dataX': type_count3,
                'dataY': df_type3
                }, 
                {
                'title': 'Age Distribution of the victim reported in the FIR Records',
                'dataX': type_count4,
                'dataY': df_type4
                }
            ]
            # Convert rjdf to List of object
            context = {
                'crime':crime,
                # 'map':getmap(),
                'JSONdata':JSONdata,
                'dataX':dataX,
                'dataY':dataY,
                'df_type':df_type,
                'df_type2':df_type2,
                'df_type3':df_type3,
                'df_type4':df_type4,
                'type_count':type_count,
                'type_count2':type_count2,
                'type_count3':type_count3,
                'type_count4':type_count4,
                'questions':data,
                }
            return render(request, 'CrimeAnalysis/crimeanalysis.html',context)
        # pp()
        return redirect('/login')

    def agent_llm(self, ukdf):
        llm = OpenAI(openai_api_key=os.getenv('OPENAI_API_KEY'))

        return create_pandas_dataframe_agent(llm, rjdf, verbose=False)


    def query_llm(self, agent, query):

        prompt = (
            """
                For the following query, if it requires drawing a table, reply as follows:
                {"table": {"columns": ["column1", "column2", ...], "data": [[value1, value2, ...], [value1, value2, ...], ...]}}

                If the query requires creating a bar chart, reply as follows:
                {"bar": {"columns": ["A", "B", "C", ...], "data": [25, 24, 10, ...]}}

                If the query requires creating a line chart, reply as follows:
                {"line": {"columns": ["A", "B", "C", ...], "data": [25, 24, 10, ...]}}

                The various types of chart, "bar", "line" and "pie" plot

                If it is just asking a question that requires neither, reply as follows:
                {"answer": "answer"}
                Example:
                {"answer": "The title with the highest rating is 'Gilead'"}

                If you do not know the answer, reply as follows:
                {"answer": "I do not know."}

                Return all output as a string.

                All strings in "columns" list and data list, should be in double quotes,

                For example: {"columns": ["title", "ratings_count"], "data": [["Gilead", 361], ["Spider's Web", 5164]]}

                Lets think step by step.

                Below is the query.
                Query: 
                """
            + query
        )

        response = agent.run(prompt)
        return response.__str__()



    def decode_response(self, response: str) -> dict:

        return json.loads(response)
 
    
    def post(self, request):
        if request.method == 'POST':
            query = request.POST['query']
            agent = self.agent_llm(rjdf)
            response = self.query_llm(agent=agent, query=query)
            decoded_response = self.decode_response(response)



            tempDF = ukdf.copy()
            tempDF['Arrest'] = tempDF['Arrest'].map({True: 'True', False: 'False'})
            tempDF['Domestic'] = tempDF['Domestic'].map({True: 'True', False: 'False'})
            tempDF['Date']=tempDF['Date'].astype(str)
            Samp=tempDF[tempDF["Community_area"]==""]

            # Q1 Which Type of Crime is most recorded ?
            crime['Type'] = tempDF["Type"].unique()
            crime['Where'] = tempDF["Where"].unique()
            crime['District'] = tempDF["District"].unique()
    
            q1=tempDF.Type.value_counts().rename_axis('Crime_Type').reset_index(name='counts')
            df_type=list(q1["Crime_Type"].head(13))
            type_count=list(q1["counts"].head(13))

            #Object of Array (Dictionary) for Different Questions representation in analytics
            #Use Js Ternary Operator
            # Q2 Where most no. of crimes are recorded?
            # Top 5 place where 
            q2=tempDF.Where.value_counts().rename_axis('Where_Type').reset_index(name='counts')
            df_type2=list(q2["Where_Type"].head(5))
            type_count2=list(q2["counts"].head(5))

            #Which Type of Crime is more and arrest is done?
            df_arrest=tempDF[tempDF["Arrest"]=="True"]
            q3=df_arrest.Type.value_counts().rename_axis('Crime_Type1').reset_index(name='counts')
            df_type3=list(q3["Crime_Type1"].head(5))
            type_count3=list(q3["counts"].head(5))
            '''
            # Q4 On which day of week; the crime is more?
            df_type4=['Monday','Tuesday','Wednesday',  'Thursday', 'Friday', 'Saturday', 'Sunday']
            type_count4=tempDF.groupby([tempDF.index.dayofweek]).size()
            print("*******", type_count4)
    
            # Q5 In which month, most no. of crime is recorded?

            df_type5=['Jan','Feb','Mar',  'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            type_count5=tempDF.groupby([tempDF.index.month]).size()
            '''
            # On page load graph will be shown
            df_typeAll=list(tempDF["Type"].unique())
            type_countAll=[]
            for x in range(len(tempDF.Type.value_counts())):
                type_countAll.append(int(tempDF.Type.value_counts()[x]))
            dataX = type_countAll
            dataY = df_typeAll
        
            #tempDF.drop("Arrest", inplace=True, axis=1)
            #tempDF.drop("Domestic", inplace=True, axis=1)
            # dumbdata = tempDF.to_dict('records')
            # print(tempDF.to_dict('records'))
            # JSONdata =json.dumps(rjdf.to_dict('records'))
            data_dict = rjdf.to_dict('records')
            JSONdata = json.dumps(data_dict, ensure_ascii=False)
            print('''
            *****************
            *****************
            *****************
            *****************
            ''', type_count)
            print(df_type)
            print('''
            *****************
            *****************
            *****************
            *****************
            ''', type_count2)
            print(df_type2)
            print('''
            *****************
            *****************
            *****************
            *****************
            ''', type_count3)
            print(df_type3)
            # dataT = str(tempDF.values.tolist())
            data = [
                {
                'title': 'Most Type of crime recorded',
                'dataX': type_count,
                'dataY': df_type
                },
                {
                'title': 'Location with most number of crimes are recorded',
                'dataX': type_count2,
                'dataY': df_type2
                },
                {
                'title': 'Type of crime in which most number of arrest is done',
                'dataX': type_count3,
                'dataY': df_type3
                }, 
                {
                'title': 'In which month, most no. of crime is recorded',
                'dataX': [10, 6, 15, 20, 23, 30, 33, 15, 13, 15, 20, 25],
                'dataY': ['Jan','Feb','Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                },
                {
                'title': 'On which of day of week, the more crime is recorded',
                'dataX': [25, 20, 16, 11, 6, 28, 38],
                'dataY': ['Monday','Tuesday','Wednesday',  'Thursday', 'Friday', 'Saturday', 'Sunday']
                }
            ]

            context = {
                'result1': decoded_response,
                'query': query,
                'crime':crime,
                'JSONdata':JSONdata,
                'dataX':dataX,
                'dataY':dataY,
                'df_type':df_type,
                'df_type2':df_type2,
                'df_type3':df_type3,
                'type_count':type_count,
                'type_count2':type_count2,
                'type_count3':type_count3,
                'questions':data,
            }
            return render(request, 'CrimeAnalysis/crimeanalysis.html', context)

    # def post(self, request):
    #     if request.method == 'POST':
    #         name = request.POST['name']
    #         if name.find(' ') != -1:
    #             first_name, Last_name = name.split(' ', 1)
    #         else:
    #             first_name = name
    #             Last_name = name
    #         email = request.POST['email']
    #         subject = request.POST['subject']
    #         message = request.POST['message']
    #         objects = ContactUs()
    #         data = ContactUs.objects.create(first_name=first_name, last_name=Last_name, User_email=email, User_subject=subject, User_message=message)
    #         data.save()
    #         alert = "Thankyou for contacting us! Our team will get back to you soon."
    #         return render(request, 'CrimeMapping/index.html',{'alert':alert})
    #     else:
    #         alert = "Please fill the form again."
    #     return render(request, 'CrimeMapping/index.html',{'alert':alert})




