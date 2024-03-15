import folium 
from django.views import View
from django.shortcuts import render, redirect 

import cv2
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import render
import numpy as np

from PIL import Image
import cv2
import pytesseract


class Test(View):

    def get(self, request):
        lat = 25.1706
        lng = 75.8609
        map = folium.Map(location=[lat, lng], zoom_start=15)

        js_code = f"""
            <script>
                function submitForm() {{
                var latitude = document.getElementsByName('lat')[0].value;
                var longitude = document.getElementsByName('lng')[0].value;
                var noteHeading = document.getElementsByName('note_heading')[0].value;
                var noteDescription = document.getElementsByName('note_des')[0].value;

                console.log('Latitude:', latitude);
                console.log('Longitude:', longitude);
                console.log('Note Heading:', noteHeading);
                console.log('Note Description:', noteDescription);

                }}
            </script>
        """

        html = f"""
        <form action="" method="POST" id="noteForm">
            <div class="form-group">
                <label for="note_heading">Note heading</label>
                <input type="text" name="note_heading" class="form-control">
            </div>
            <input type="text" name="lat" value="{lat}">
            <input type="text" name="lng" value="{lng}">
            <div class="form-group">
                <label for="note">Note</label>
                <textarea class="form-control" name="note_des">Enter note here</textarea>
            </div>
            <button type="button" class="btn btn-primary" onclick="submitForm();">Submit</button>
        </form>
        {js_code}
        """

        iframe = folium.IFrame(html, width=200, height=200)
        popup = folium.Popup(iframe)
        marker = folium.Marker([lat, lng], popup, draggable=True).add_to(map)
        map.add_child(folium.ClickForMarker(popup="Waypoint"))
        map = map._repr_html_()
        context = {"lat": lat, "lng": lng, "map": map}
        return render(request, 'Test/test.html', context)

    # def post(self, request):
    #     if request.method == 'POST' and request.FILES['image']:
    #         # Assuming you have an uploaded image
    #         uploaded_file = request.FILES['image']

    #         image_bytes = uploaded_file.read()
    #         nparr = np.frombuffer(image_bytes, np.uint8)
    #         cvimg = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
    #         if cvimg.shape[-1] == 3:  # Assuming BGR image
    #             gray_image = cv2.cvtColor(cvimg, cv2.COLOR_BGR2GRAY)
    #             print("BGR image ............")
    #         else:
    #             gray_image = cvimg
    #             print("Grayscale image .....")

    #         # Read the uploaded image using OpenCV
    #         image = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_UNCHANGED)

    #         # Convert the image to grayscale
    #         gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #         # Apply any additional image processing or enhancement steps if needed

    #         # Save the processed image to the media folder
    #         processed_filename = f"processed_image_{uploaded_file.name}"
    #         processed_path = default_storage.save(processed_filename, ContentFile(cv2.imencode('.png', gray_image)[1].tobytes()))

    #         # Use Tesseract OCR to extract text
    #         text = pytesseract.image_to_string(Image.open(default_storage.path(processed_path)))

    #         # Display the extracted text or use it as needed
    #         text = "Extracted text: " + text

    #     return render(request, 'Test/test.html', {'text': text})





    #     # if request.method == 'POST' and request.FILES.get('pdf_file'):
    #     #     pdf_file = request.FILES['pdf_file']
    #     #     fs = FileSystemStorage()
    #     #     filename = fs.save(pdf_file.name, pdf_file)
    #     #     pdf_path = fs.url(filename)
        


    #     # if request.method == 'POST' and request.FILES['image']:
    #     #     # Assuming you have an uploaded image
    #     #     uploaded_file = request.FILES['image']
    #     #     # Read the uploaded image
    #     #     image = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    #     #     # Convert to grayscale
    #     #     gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #     #     # Save the grayscale image to the media folder
    #     #     file_name = f"grayscale_{uploaded_file.name}"
    #     #     file_path = default_storage.save(file_name, ContentFile(cv2.imencode('.png', gray_image)[1].tobytes()))

    #     #     # You can now use file_path to display or further process the saved image
    #         # path = "Grayscale image saved at: {file_path}"

    #         # return render(request, 'Test/test.html', {'path': path})
    #     return render(request, 'Test/test.html', {'pdf_path': None})

    def post(self, request):
        if request.method == 'POST' and request.FILES['image']:
            # Assuming you have an uploaded image
            uploaded_file = request.FILES['image']

            # Read the binary data of the uploaded file
            image_bytes = uploaded_file.read()

            # Convert the binary data to a NumPy array
            nparr = np.frombuffer(image_bytes, np.uint8)

            # Decode the image using OpenCV
            cvimg = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)

            if cvimg.shape[-1] == 3:  # Assuming BGR image
                gray_image = cv2.cvtColor(cvimg, cv2.COLOR_BGR2GRAY)
                print("BGR image ............")
            else:
                gray_image = cvimg
                print("Grayscale image .....")

            # Apply any additional image processing or enhancement steps if needed

            # Save the processed image to the media folder
            processed_filename = f"processed_image_{uploaded_file.name}"
            processed_path = default_storage.save(processed_filename, ContentFile(cv2.imencode('.png', gray_image)[1].tobytes()))

            # Use Tesseract OCR to extract text
            text = pytesseract.image_to_string(Image.open(default_storage.path(processed_path)), lang='hin')

            # Display the extracted text or use it as needed
            text = "Extracted text: " + text
            print(text)
            return render(request, 'Test/test.html', {'text': text})
