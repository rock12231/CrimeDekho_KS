import os
import json
import folium 
import numpy as np
import pandas as pd
from openai import OpenAI
from django.views import View
from folium.plugins import MiniMap
from geopy.geocoders import Nominatim
from CrimeMapping.models import FirData
from django.shortcuts import render, redirect 
from CrimeMapping.models import Crimes2001, PoliceStationList, GraphData, PoliceStationJaipurList, PoliceDetails

# Initialize the Nominatim geolocator
geolocator = Nominatim(user_agent="myapp")

# Read data from csv file
ukdf = pd.read_csv("CrimeMapping/data/UK-Dataset-Final.csv", on_bad_lines='skip' )

ukdfp = pd.read_csv("CrimeMapping/data/UK-Police-Station.csv")

rjdf = pd.read_csv("CrimeMapping/data/fir_rajasthan.csv")

rjdfp=pd.read_csv("CrimeMapping/data/raj_police.csv")

df = pd.DataFrame(Crimes2001.objects.all().values())
df=df.dropna()

dfp = pd.DataFrame(PoliceStationList.objects.all().values())
dfp=dfp.dropna()

dfg = pd.DataFrame(GraphData.objects.all().values())

# # Jaipur Rajasthan Police DataFrame
jrjpdf= pd.DataFrame(PoliceStationJaipurList.objects.all().values())

model_rjdf = pd.DataFrame(FirData.objects.all().values())

# To add Open AI key here
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

global img_url
# img_url = staticfiles_storage.url('assets/img/policeman.png')
img_url = 'https://raw.githubusercontent.com/rock12231/Rest-Framework-API-With-AJAX/master/policeman.png'
# dict_from_csv = pd.read_csv('CrimeMapping/data/PoliceStation.csv', sep = ',') 
# print(dict_from_csv)
# print(type(dict_from_csv))

crime: dict = {
    'District':any,
    'Type':any,
    'Where':any,
    'selDistrict':"",
    'selType':"",
    'selWhere':"",
    'startDate':"",
    'endDate':"",
    'domestic':"",
    'arrest':"",
    'startendDates':"",
    'flag':False,
}

cards: dict={
    'dataAll':int,
    'dataArrest':int,
    'dataDomestic':int,
    'dataStations':int,
    'most_type':"",
}

class Crimemapping(View):
    def get(self, request):
        #DynamicAnalytics2(df)
        if request.user.is_authenticated:
            # get all data from PoliceDetail model
            police = PoliceDetails.objects.all()
            tempDF = ukdf.copy()
            tempDF['Arrest'] = tempDF['Arrest'].map({True: 'True', False: 'False'})
            tempDF['Domestic'] = tempDF['Domestic'].map({True: 'True', False: 'False'})
            tempDF['Date']=tempDF['Date'].astype(str)
            tempDF[tempDF["Community_area"]==""]
            
            crime['Type'] = tempDF["Type"].unique()
            crime['Where'] = tempDF["Where"].unique()
            crime['District'] = tempDF["District"].unique()

            mtemp = model_rjdf.copy()
            pstation = mtemp["police_station"].unique()
            ipcs = mtemp["ipc_no"].unique()
    
            context = {
                'crime':crime,
                'map':getmap(),
                'pstation':pstation,
                'ipcs':ipcs,
                'police' : police
                }
            return render(request, 'CrimeMapping/crimemapping.html',context)
        return redirect('/login')
    
    def post(self, request):
        if request.method == 'POST':
            mtemp = model_rjdf.copy()
            pstation = mtemp["police_station"].unique()
            ipcs = mtemp["ipc_no"].unique()

            tempDF = ukdf.copy()
            crime['Type']  = tempDF["Type"].unique()
            crime['District']  = tempDF["District"].unique()
            crime['Where']  = tempDF["Where"].unique()

            if request.POST.get("form_type") == 'formOne':
                Where = request.POST['Where']
                Arrest = bool(request.POST.get('arrest'))
                Domestic = bool(request.POST.get('domestic'))
                Type = request.POST.getlist('states')
                startDate = int(request.POST['start'])
                endDate = int(request.POST['end'])
                crime['startDate'] = startDate
                crime['endDate'] = endDate
                crime['selType'] = Type
                crime['arrest'] = Arrest
                crime['domestic'] = Domestic
                crime['startendDates'] = str(startDate) + " - " + str(endDate)
                crime['selWhere'] = Where
                print(crime, ".......................")
                df11=tempDF[tempDF["Type"]==str(Type[0])]
                print("(((((((((((((()))))))))))))))", len(df11))
                location=[29.8240,  78.0057]
                #Latitude: 41.8285 Longitude: -87.8137
                map = folium.Map(location, zoom_start=10)
                #Set Zooming size
                print(df11.head(10))
                print(df11.tail(10))
                #DynamicAnalytics2(tempDF)
                folium.Marker(location).add_to(map)
                folium.raster_layers.TileLayer('Stamen Terrain').add_to(map)
                folium.raster_layers.TileLayer('Stamen Toner').add_to(map)
                folium.raster_layers.TileLayer('Stamen Watercolor').add_to(map)
                map.add_child(folium.LatLngPopup())
                # folium.Circle(
                #     radius=1000,
                #     location=[41.8970, -87.7299],
                #     popup="The Waterfront",
                #     color="crimson",
                #     fill=False,
                # ).add_to(map)
                print("+++++++++++++++++++", Where)
                print("+++++++++++++++++++", Type)
                print("+++++++++++++++++++", startDate)
                print("+++++++++++++++++++", endDate)
                print("+++++++++++++++++++", Arrest)
                print("+++++++++++++++++++", Domestic)
                # print(df11.head())
                for p in range(len(Type)):
                    color1=['#ff005a','#AB96FF','#FCE49C','#FE9A65','#7BFC90','#CFFC8F','#A5FCD4','#95FDEA','#FF785A',
                            '#FF785A','#EF511F','#F9B0A5','#8FBDFF','#FF5244','#FF8861','#FF81C9','#FAFC87','#9BFBB4',
                            '#737BFF','#FDFD89','#FAEB70','#FE9491','#F9C4C2','#D1F9C2','#CDFEC0','#E74A31','#FCE096']
                    color2=['#eb0c83','#7251F9','#FBCF4F','#FD7C37','#11F537','#B6FA54','#6CFFBA','#5FFCE0','#FC4B24',
                            '#FC4B24','#B63208','#DE7E6F','#1B73F3','#F71300','#FF521B','#FF119A','#E1E412','#1AF953',
                            '#0915CF','#FCFC41','#F7DE06','#B60904','#F10C05','#5EE12D','#75F951','#DD270B','#FBC127']
                    mapping(tempDF,Type[p], color1[p], color2[p], Where,Type, Arrest, Domestic,startDate, endDate, map)
                
                # policestation(dfp, map)
                '''
                for x in range(0, len(df11)):
                    if ((df11.iloc[x]["Where"]==str(Where)) & (df11.iloc[x]["Type"]==str(Type[0])) & (df11.iloc[x]["Arrest"]==Arrest) & (df11.iloc[x]["Domestic"]==Domestic)):
                        folium.CircleMarker(location=[df11.iloc[x]['Latitude'], df11.iloc[x]['Longitude']],  radius=25, popup=df11.iloc[x]["Type"], color=c1, fill=True, fill_color=c2).add_to(map)
                        print("Latitude************", df11.iloc[x]['Latitude'])
                '''
                #tempDF,Type[p], color1[p], color2[p], Where,Type, Arrest, Domestic, map
                #tempDF, type11, c1, c2, Where, Type, Arrest, Domestic, map

                df11=tempDF.copy()
                df11['Arrest'] = df11['Arrest'].map({True: 'True', False: 'False'})
                df11['Domestic'] = df11['Domestic'].map({True: 'True', False: 'False'})
                df11['Date']=df11['Date'].astype(str)
                print("+++++++++++++++", Where)
                print("+++++++++++++++", Type)
                print("+++++++++++++++", Arrest)
                print("+++++++++++++++", Domestic)
                Tabledf=pd.DataFrame()
                '''
                tempDF.Date = pd.to_datetime(tempDF.Date, format='%m/%d/%Y %I:%M:%S %p')
                tempDF.index = pd.DatetimeIndex(tempDF.Date)
                '''
                # print("+++++++++++++++", type_count3)
                #DataTable= df11[(df11["Where"]==str(Where)) & ((df11["Type"]==str(Type[0]))) & (df11["Arrest"]==str(Arrest)) & (df11["Domestic"]==str(Domestic))]
                for x in range(0, len(Type)):
                    DataTable1= df11[(df11["Where"]==str(Where)) & ((df11["Type"]==str(Type[x]))) & (df11["Arrest"]==str(Arrest)) & (df11["Domestic"]==str(Domestic)) & (df11.iloc[x]["Year"]>=int(startDate)) & (df11.iloc[x]["Year"]<=int(endDate))]
                    Tabledf=Tabledf._append(DataTable1, ignore_index = True)
                print(Tabledf.to_string())
                folium.LayerControl().add_to(map)
                map = map._repr_html_()
                
                # Table and graph
                tempDF['Arrest'] = tempDF['Arrest'].map({True: 'True', False: 'False'})
                tempDF['Domestic'] = tempDF['Domestic'].map({True: 'True', False: 'False'})
                tempDF['Date']=tempDF['Date'].astype(str)

                # DynamicAnalytics3()
            
                context = {
                    'crime':crime,
                    'map':map,
                    'pstation':pstation,
                    'ipcs':ipcs,
                    }
                return render(request, 'CrimeMapping/crimemapping.html', context)
            
            if request.POST.get("form_type") == 'formTwo':
                selectedipc = request.POST.getlist('ipc')
                selctedpstation = request.POST.getlist('pstation')
                print(selectedipc, selctedpstation,"........................")

                location=[26.9371,  75.8122]
                #Latitude: 41.8285 Longitude: -87.8137
                map = folium.Map(location, zoom_start=12)
                #Set Zooming size
                print(mtemp.head(10))
                print(mtemp.tail(10))
                mtemp=mtemp.dropna()
                #DynamicAnalytics2(tempDF)
                folium.Marker(location).add_to(map)
                folium.raster_layers.TileLayer('Stamen Terrain').add_to(map)
                folium.raster_layers.TileLayer('Stamen Toner').add_to(map)
                folium.raster_layers.TileLayer('Stamen Watercolor').add_to(map)



                for x in range(0, len(jrjpdf)):
                    if len(jrjpdf.iloc[x]["Police_Station"])>0:
                        popup = f'''<table class="table" style="white-space:nowrap">\
                        <thead class="table-dark"><tr><th scope="col" colspan="2" class="text-center">{jrjpdf["Police_Station"][x]}</th></tr></thead>\
                        <tbody><tr><th scope="row">Address:</th><td>{jrjpdf["Address"][x]}</td></tr> \
                        <tr><th scope="row">Phone Number:</th><td>{jrjpdf["Phone_Number"][x]}</td></tr> \
                        <tr><th scope="row">Latitude:</th><td>{jrjpdf["Latitude"][x]}</td></tr> \
                        <tr><th scope="row">Longitude:</th><td>{jrjpdf["Longitude"][x]}</td></tr> \
                        
                        </tbody></table>'''
                        folium.Marker([jrjpdf.iloc[x]['Latitude'], jrjpdf.iloc[x]['Longitude']], popup=popup, icon=folium.features.CustomIcon(img_url, icon_size=(40, 40))).add_to(map),

                map.add_child(folium.LatLngPopup())





                # folium.Circle(
                #     radius=1000,
                #     location=[41.8970, -87.7299],
                #     popup="The Waterfront",
                #     color="crimson",
                #     fill=False,
                # ).add_to(map)
                # print("+++++++++++++++++++", Where)
                # print("+++++++++++++++++++", Type)
                # print("+++++++++++++++++++", startDate)
                # print("+++++++++++++++++++", endDate)
                # print("+++++++++++++++++++", Arrest)
                # print("+++++++++++++++++++", Domestic)
                # print(df11.head())
                # for p in range(len(selctedpstation)):
                #     color1=['#ff005a','#AB96FF','#FCE49C','#FE9A65','#7BFC90','#CFFC8F','#A5FCD4','#95FDEA','#FF785A',
                #             '#FF785A','#EF511F','#F9B0A5','#8FBDFF','#FF5244','#FF8861','#FF81C9','#FAFC87','#9BFBB4',
                #             '#737BFF','#FDFD89','#FAEB70','#FE9491','#F9C4C2','#D1F9C2','#CDFEC0','#E74A31','#FCE096']
                #     color2=['#eb0c83','#7251F9','#FBCF4F','#FD7C37','#11F537','#B6FA54','#6CFFBA','#5FFCE0','#FC4B24',
                #             '#FC4B24','#B63208','#DE7E6F','#1B73F3','#F71300','#FF521B','#FF119A','#E1E412','#1AF953',
                #             '#0915CF','#FCFC41','#F7DE06','#B60904','#F10C05','#5EE12D','#75F951','#DD270B','#FBC127']
                mapping2(mtemp,selectedipc, selctedpstation, map)
                
                # policestation(dfp, map)
                '''
                for x in range(0, len(df11)):
                    if ((df11.iloc[x]["Where"]==str(Where)) & (df11.iloc[x]["Type"]==str(Type[0])) & (df11.iloc[x]["Arrest"]==Arrest) & (df11.iloc[x]["Domestic"]==Domestic)):
                        folium.CircleMarker(location=[df11.iloc[x]['Latitude'], df11.iloc[x]['Longitude']],  radius=25, popup=df11.iloc[x]["Type"], color=c1, fill=True, fill_color=c2).add_to(map)
                        print("Latitude************", df11.iloc[x]['Latitude'])
                '''
                #tempDF,Type[p], color1[p], color2[p], Where,Type, Arrest, Domestic, map
                #tempDF, type11, c1, c2, Where, Type, Arrest, Domestic, map

                df11=mtemp.copy()
                # df11['Arrest'] = df11['Arrest'].map({True: 'True', False: 'False'})
                # df11['Domestic'] = df11['Domestic'].map({True: 'True', False: 'False'})
                # df11['Date']=df11['Date'].astype(str)
                # print("+++++++++++++++", Where)
                # print("+++++++++++++++", Type)
                # print("+++++++++++++++", Arrest)
                # print("+++++++++++++++", Domestic)
                Tabledf=pd.DataFrame()
                '''
                tempDF.Date = pd.to_datetime(tempDF.Date, format='%m/%d/%Y %I:%M:%S %p')
                tempDF.index = pd.DatetimeIndex(tempDF.Date)
                '''
                # print("+++++++++++++++", type_count3)
                #DataTable= df11[(df11["Where"]==str(Where)) & ((df11["Type"]==str(Type[0]))) & (df11["Arrest"]==str(Arrest)) & (df11["Domestic"]==str(Domestic))]
                for x in range(0, len(selectedipc)):
                    DataTable1= df11[(df11["ipc_no"]==str(selectedipc)) & (df11["police_station"]==str(selctedpstation))]
                    Tabledf=Tabledf._append(DataTable1, ignore_index = True)
                print(Tabledf.to_string())
                folium.LayerControl().add_to(map)
                map = map._repr_html_()
                
                # Table and graph
                # tempDF['Arrest'] = tempDF['Arrest'].map({True: 'True', False: 'False'})
                # tempDF['Domestic'] = tempDF['Domestic'].map({True: 'True', False: 'False'})
                # tempDF['Date']=tempDF['Date'].astype(str)

                context = {
                    'crime':crime,
                    'map':map,
                    'pstation':pstation,
                    'ipcs':ipcs,
                    }
                return render(request, 'CrimeMapping/crimemapping.html', context)

            if request.POST.get("form_type") == 'formThree':

                police = PoliceDetails.objects.all().values()
                crimes = [{'crime_id':1, 'longitude':'26', 'latitude':'75', 'risk_level':'High'},{'crime_id':2, 'longitude':'223', 'latitude':'1223', 'risk_level':'High'},{'crime_id':3, 'longitude':'312', 'latitude':'312', 'risk_level':'Medium'}]
                for i in range(len(crimes)):
                    lat = crimes[i]['latitude']
                    long = crimes[i]['longitude']
                    try:
                        location = geolocator.reverse([long, lat])
                        crimes[i]['location'] = location.address      
                    except Exception:
                        crimes[i]['location'] = lat+long                                              
                police_officers = []
                for p in police:
                    if request.POST.get(f"name-{p['id']}"):
                        police_officers.append({'police_id':p['id'], 'police_officer':p['PoliceName']})

                prompt = f"""
                    You have to assign given police_officers to crimes according to the risk_level. 
                    If there are less police_officers try to allocate two or more nearest locations to same police_officers. 
                    If there are more number of police_officers assign greater number of police_officers to crimes with higher risks.

                    crimes - {crimes}

                    police_officers - {police_officers}

                    Don't return the code. Just return the assignments of police_officers to crimes in json format only.

                    Example JSON Output to Strictly Follow -
                    {{
                        "assignments": [
                            {{"crime_id":12, "location":"address", "risk_level":"High", "police_id":1, "police_officer":"anand"}},
                            {{"crime_id":13, "location":"address", "risk_level":"Medium", "police_id":2, "police_officer":"nobita"}}
                        ]
                    }}
                """

                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "system", "content": prompt}]
                )
                allocation_json = response.choices[0].message.content
                context = {
                    'crime':crime,
                    'map':getmap(),
                    'pstation':pstation,
                    'ipcs':ipcs,
                    'police':police
                }
                try:
                    allocation = json.loads(allocation_json)
                    context['allocation'] = allocation['assignments']
                except Exception:
                    pass
                return render(request, 'CrimeMapping/crimemapping.html', context)


def mapping(tempDF, type11, c1, c2, Where, Type, Arrest, Domestic,startDate, endDate, map):

    df11=tempDF[tempDF["Type"]==str(type11)]
    print("aaaaaaaaaaa...........",df11)
    for x in range(0, len(df11)):
            if ((df11.iloc[x]["Where"]==str(Where)) & (df11.iloc[x]["Type"]==str(type11)) & (df11.iloc[x]["Arrest"]==Arrest) & (df11.iloc[x]["Domestic"]==Domestic) & (df11.iloc[x]["Year"]>=int(startDate)) & (df11.iloc[x]["Year"]<=int(endDate))):
                popup1 = f'<table class="table" style="white-space:nowrap">\
                <thead class="table-dark"><tr><th scope="col" colspan="2" class="text-center">{df11.iloc[x]["Type"]}</th></tr></thead>\
                <tbody><tr><th scope="row">Case no:</th><td>{df11.iloc[x]["caseno"]}</td></tr> \
                <tbody><tr><th scope="row">IPC Code:</th><td>{df11.iloc[x]["IPC"]}</td></tr> \
                <tr><th scope="row">Crime Description:</th><td>{df11.iloc[x]["Type_desc"]}</td></tr> \
                <tr><th scope="row">Address:</th><td>{df11.iloc[x]["block"]}</td></tr> \
                <tr><th scope="row">Date:</th><td>{df11.iloc[x]["Date"]}</td></tr> \
                </tbody></table>'
                folium.CircleMarker(location=[df11.iloc[x]['Latitude'], df11.iloc[x]['Longitude']],  radius=15, popup=popup1, color=c1, fill=True, fill_color=c2).add_to(map)
                print("Latitude************", df11.iloc[x]['Latitude'])



def mapping2(mtemp,selectedipc, selctedpstation, map):
    
    if selectedipc[0] in mtemp["ipc_no"].unique().tolist():
        df11=mtemp[mtemp["ipc_no"]==str(selectedipc[0])]

    if selctedpstation[0] in mtemp["police_station"].unique().tolist():
        df11=mtemp[mtemp["police_station"]==str(selctedpstation[0])]


        df11 = df11.dropna(subset=['latitude', 'longitude'])
        
        # df11['latitude'] =float(df11['latitude'])
        print(df11.info())
        # df11['latitude'] = pd.to_numeric(df11['latitude'], errors='coerce')
        # df11['longitude'] = pd.to_numeric(df11['longitude'], errors='coerce')
        # df11['latitude'] = df11['latitude'].astype(float)
        # df11['longitude'] = df11['longitude'].astype(float)

        df11['latitude'] = df11['latitude'].apply(lambda x: None if x == '' else float(x))
        df11['longitude'] = df11['longitude'].apply(lambda x: None if x == '' else float(x))



        # df11['latitude'] = df11['latitude'].apply(float)
        # df11['longitude'] = df11['longitude'].apply(float)

        print(selectedipc)

        print("aaaaaaaaaaa...........",df11)
        for x in range(0, len(df11)):
                if ((df11.iloc[x]["ipc_no"]==str(selectedipc[0])) | (df11.iloc[x]["police_station"]==str(selctedpstation[0])) |  ((df11.iloc[x]["ipc_no"]==str(selectedipc[0])) & (df11.iloc[x]["police_station"]==str(selctedpstation[0])))):
                    popup1 = f'<table class="table" style="white-space:nowrap">\
                    <thead class="table-dark"><tr><th scope="col" colspan="2" class="text-center">{df11.iloc[x]["case_no"]}</th></tr></thead>\
                    <tbody><tr><th scope="row">IPC:</th><td>{df11.iloc[x]["ipc"]}</td></tr> \
                    <tbody><tr><th scope="row">Police Station:</th><td>{df11.iloc[x]["police_station"]}</td></tr> \
                    <tbody><tr><th scope="row">Date:</th><td>{df11.iloc[x]["date"]}</td></tr> \
                    <tr><th scope="row">Name:</th><td>{df11.iloc[x]["name"]}</td></tr> \
                    <tr><th scope="row">Address:</th><td>{df11.iloc[x]["address"]}</td></tr> \
                    <tr><th scope="row">Additional Info:</th><td>{df11.iloc[x]["additional_info"]}</td></tr> \
                    </tbody></table>'



                    # df11['latitude'] = pd.to_numeric(df11['latitude'], errors='coerce')
                    # df11['latitude'] = df11['latitude'].replace('', np.nan).astype(float)
                    # df11['longitude'] = pd.to_numeric(df11['longitude'], errors='coerce')
                    # df11['longitude'] = df11['longitude'].replace('', np.nan).astype(float)

                    # df11.iloc[x]['latitude'] = None if df11.iloc[x]['latitude'] == '' else float(df11.iloc[x]['latitude'])
                    # df11.iloc[x]['longitude'] = None if df11.iloc[x]['longitude'] == '' else float(df11.iloc[x]['longitude'])

                    # if df11.iloc[x]['latitude'] != '':
                    #     df11.iloc[x]['latitude'] = float(df11.iloc[x]['latitude'])
                    # if df11.iloc[x]['longitude'] != '':
                    #     df11.iloc[x]['longitude'] = float(df11.iloc[x]['longitude'])


    

                    folium.CircleMarker(location=[float(df11.iloc[x]['latitude']), float(df11.iloc[x]['longitude'])],  radius=15, popup=popup1, color="#ff005a", fill=True, fill_color="#eb0c83").add_to(map)
                    # print(type(df11.iloc[x]['longitude']))
                    # print(type(df11.iloc[x]['latitude']))

                    print("Latitude************", df11.iloc[x]['latitude'])
                    print("L************", df11.iloc[x]['longitude'])
                    

def pp():
        location=[29.8240,  78.0057]
        map = folium.Map(location,)
        folium.Marker(location).add_to(map)
        folium.raster_layers.TileLayer('Stamen Terrain').add_to(map)
        folium.raster_layers.TileLayer('Stamen Toner').add_to(map)
        folium.raster_layers.TileLayer('Stamen Watercolor').add_to(map)
        folium.CircleMarker(location=[29.9680, 77.5552],  radius=15, color="#ff005a", fill=True, fill_color="#eb0c83").add_to(map)
        map.add_child(folium.LatLngPopup())
        folium.LayerControl().add_to(map)
        # folium.MiniMap().add_to(map)
        map = map._repr_html_() 
        return map
    
# def policestation(dfp, map):
#     for x in range(0, len(dfp)):
#             if len(dfp.iloc[x]["address"])>0:
#                 popup = f'<table class="table" style="white-space:nowrap">\
#                 <thead class="table-dark"><tr><th scope="col" colspan="2" class="text-center">{dfp["disname"][x]}</th></tr></thead>\
#                 <tbody><tr><th scope="row">Address:</th><td>{dfp["address"][x]}</td></tr> \
#                 <tr><th scope="row">Zipcode:</th><td>{dfp["zip"][x]}</td></tr> \
#                 <tr><th scope="row">Website:</th><td><a href="{dfp["website"][x]}" target="_blank">{dfp["disname"][x]}</a></td></tr>\
#                 </tbody></table>'
#                 #folium.Marker([dfp.iloc[x]['latitude'], dfp.iloc[x]['longitude']], popup=dfp.iloc[x]["address"], icon=folium.features.CustomIcon('CrimeMapping\data\policeman.png', icon_size=(50, 50))).add_to(map),
#                 folium.Marker([dfp.iloc[x]['latitude'], dfp.iloc[x]['longitude']], popup=popup, icon=folium.features.CustomIcon(img_url, icon_size=(40, 40))).add_to(map),

def DynamicAnalytics1(df):
    tempDF1=dfg.copy()
    #List for non empty features
    nonempf=[]
    for x in range(0, len(dfg)):
        features=["Type", "Where", "District"]
        for y in features:
            print('''++++++++++++++++++
                    ++++++++++++++++++
                    ++++++++++++++++++''')
            if ((dfg.iloc[x][y]) == None):
                features.remove(y)
                
def DynamicAnalytics2(df):
    tempDF = dfg.copy()
    # tempDF['created']=tempDF['created'].astype(str)
    #List for non empty features
    nonempf=[]
    for x in range(0, len(dfg)):
        tempG=df[(df["Where"]==str(dfg.iloc[x]["Where"])) | ((df["Type"]==str(dfg.iloc[x]["Type"]))) | (df["Arrest"]==str(dfg.iloc[x]["Arrest"])) | (df["Domestic"]==str(dfg.iloc[x]["Domestic"])) | (df["Year"]>=int(dfg.iloc[x]["YearS"])) | (df.iloc[x]["Year"]<=int(dfg.iloc[x]["YearE"]))]    
        print(tempG)   

# def DynamicAnalytics3():
#     tempDF = dfg.copy()

#     DF=df.copy()
#     DF['Arrest'] = DF['Arrest'].map({True: 'True', False: 'False'})
#     DF['Domestic'] = DF['Domestic'].map({True: 'True', False: 'False'})
#     # tempDF['created']=tempDF['created'].astype(str)
#     for x in range(0, len(tempDF)):
#         features=[]
#         if (tempDF.iloc[x]['YearS']) != None:
#             #print("***********YearS", tempDF)
#             # tempDF = tempDF['YearS']
#             features.append('YearS')
#         if (tempDF.iloc[x]['YearS']) != "nan":
#             #print("***********YearE", tempDF)
#             features.append('YearE')
#         if (tempDF.iloc[x]['Type']) != None:
#             #print("***********Type", tempDF)
#             features.append('Type')
#         if (tempDF.iloc[x]['Where']) != None:
#             #print("***********Where", tempDF)
#             features.append('Where')
#         if (tempDF.iloc[x]['Arrest']) == True:
#             #print("***********Arrest", tempDF)
#             features.append('Arrest')
#         if (tempDF.iloc[x]['Domestic']) == True:
#             #print("***********Domestic", tempDF)
#             features.append('Domestic')
#         if (tempDF.iloc[x]['District']) == True:
#             #print("***********District", tempDF)
#             features.append('District')
#         print('''+++++++++++++++++++
#             ++++++++++++++++++++
#             ++++++++++++++++++++''', features)
#         for y in features:
#             if  y=="Arrest":
#                 DF=DF[DF["Arrest"]==str(tempDF.iloc[x]['Arrest'])]
#                 print(str(tempDF.iloc[x]['Arrest']))
                
#             if y=="Domestic":
#                 DF=DF[DF["Domestic"]==str(tempDF.iloc[x]['Domestic'])]
#                 print(str(tempDF.iloc[x]['Domestic']))
#             if y=="YearS":
#                 DF=DF[DF["Year"]>=(tempDF.iloc[x]['YearS'])]
#                 print(tempDF.iloc[x]['YearS'])
#             if y=="YearE":
#                 DF=DF[DF["Year"]<=(tempDF.iloc[x]['YearE'])]
#                 print(tempDF.iloc[x]['YearE'])

#         '''
#         dataX=[]
#         dataY=[]
#         title=[]
#         data=[
#             {

#             },
#             {

#             }
#         ]
#         Return data
#         '''

def getmap():
        location=[26.9197,75.8085]
        crime_where = crime['Where'].tolist()
        print(">>>>>>>",crime_where ,"<<<<<<<<<<")
        crime_type = crime['Type'].tolist()
        print(">>>>>>>",crime_type ,"<<<<<<<<<<")

        js_code = f"""
            <script>
                var currentYear = new Date().getFullYear();
                var startYear = 2001;
                for (var year = currentYear; year >= startYear; year--) {{
                    var option = document.createElement("option");
                    option.value = year;
                    option.text = year;
                    document.getElementById("fromYear").appendChild(option);
                }}
           
            function updateToYear() {{
                    var fromYearSelect = document.getElementById("fromYear");
                    var toYearSelect = document.getElementById("toYear");
                    toYearSelect.innerHTML = '<option selected>To</option>';
                    var selectedFromYear = parseInt(fromYearSelect.value);
                    for (var year = currentYear; year > selectedFromYear; year--) {{
                        var option = document.createElement("option");
                        option.value = year;
                        option.text = year;
                        toYearSelect.appendChild(option);
                    }}
                }}


                var crimeWhereOptions = {crime_where};
                var selectElement1 = document.getElementById('inputGroupSelect01');
                for (var i = 0; i < crimeWhereOptions.length; i++) {{
                var option = document.createElement('option');
                option.value = crimeWhereOptions[i];
                option.text = crimeWhereOptions[i];
                selectElement1.appendChild(option);
                }}

                
                var crime_type = {crime_type};
                var selectElement2 = document.getElementById('inputGroupSelect02');
                for (var i = 0; i < crime_type.length; i++) {{
                    var option = document.createElement('option');
                    option.value = crime_type[i];
                    option.text = crime_type[i];
                    selectElement2.appendChild(option);
                }}

            function submitForm() {{
            
                var types = [];
            
                for (var i = 0; i < selectElement2.options.length; i++) {{
                    if (selectElement2.options[i].selected) {{
                        types.push(selectElement2.options[i].text);
                    }}
                }}

                var where = document.getElementsByName('Where')[0].value;
                var arrest = document.getElementById("ArrestI").checked;
                var domestic = document.getElementById("DomesticI").checked;
                var from = parseInt(document.getElementsByName('fromYear')[0].value);
                var to = parseInt(document.getElementsByName('toYear')[0].value);

                console.log('Type:', types);
                console.log('Where:', where);
                console.log('Arrest:', arrest);
                console.log('Domestic:', domestic);
                console.log('From:', from);
                console.log('To:', to);

                var crime_types = types.join(',');
                console.log('Crime Types:', crime_types);

                $(document).ready(function () {{
                        $.ajax({{
                            type: 'GET',
                            url: 'http://127.0.0.1:8000/api/crime/?param_type=' + crime_types + '&param_where=' + where + '&param_arrest=' + arrest + '&param_domestic=' + domestic + '&param_from=' + from + '&param_to=' + to,

                            success: function (response) {{
                                console.log(response);
                                //window.location.href = 'http://localhost:8000/test/';
                                window.top.location.href = 'http://localhost:8000/crime-mapping/';
                            }},
                            error: function (error) {{
                                console.error('Error:', error);
                            }}
                        }});
                    }});

                }}
                
            </script>
            
        """

        html = f"""
        <script src="https://code.jquery.com/jquery-3.6.4.min.js"></script>
        <form action="/crime-mapping/" method="POST" id="noteForm">
            <center>
                <b style="margin: 5px;">AT : {location[0]},{location[1]}</b>
                <br>
                <select name="Where" class="form-control" id="inputGroupSelect01" aria-label="Example select with button addon" style="width: 178px;" required>
                    <option selected>Choose Crime Location</option>
                </select>
                
                Domestic <input type="checkbox" id="DomesticI" name="Domestic">
                Arrest <input type="checkbox" id="ArrestI" name="Arrest">
                
                <select class="form-select form-select-sm" aria-label=".form-select-sm example" id="fromYear" name="fromYear" onchange="updateToYear()" style="width: 83px;">
                    <option selected>From</option>
                </select>
                
                <select class="form-select form-select-sm" aria-label=".form-select-sm example" id="toYear" name="toYear" style="width: 83px;">
                    <option selected>To</option>
                </select>

                <select name="Type" class="form-control" id="inputGroupSelect02" aria-label="Example select with button addon" multiple="multiple" style="width: 178px;  margin-top: 5px;" required>
                </select>
            </center>
            <br>
            <center><input type="submit" class="btn btn-primary" onclick="submitForm();" value="Search"></center>
        </form>
        {js_code}
        """
        map = folium.Map(location, height=750, zoom_start=12)
        iframe = folium.IFrame(html, width=210, height=215)
        popup = folium.Popup(iframe)
        folium.Marker(location, popup, draggable=True).add_to(map)

        # context = {"lat": lat, "lng": lng, "map": map}

        # map = folium.Map(location, height=750, zoom_start=13.5)
        # folium.Marker(location).add_to(map)
        folium.plugins.Geocoder().add_to(map)

        folium.raster_layers.TileLayer('Stamen Terrain').add_to(map)
        folium.raster_layers.TileLayer('Stamen Toner').add_to(map)
        folium.raster_layers.TileLayer('Stamen Watercolor').add_to(map)

        folium.plugins.Fullscreen(position="topright",title="Expand me",title_cancel="Exit me",force_separate_button=True,).add_to(map)

        # print(jrjpdf.head())
        # print(jrjpdf.info())
        for x in range(0, len(jrjpdf)):
            if len(jrjpdf.iloc[x]["Police_Station"])>0:
                popup = f'''<table class="table" style="white-space:nowrap">\
                <thead class="table-dark"><tr><th scope="col" colspan="2" class="text-center">{jrjpdf["Police_Station"][x]}</th></tr></thead>\
                <tbody><tr><th scope="row">Address:</th><td>{jrjpdf["Address"][x]}</td></tr> \
                <tr><th scope="row">Phone Number:</th><td>{jrjpdf["Phone_Number"][x]}</td></tr> \
                <tr><th scope="row">Latitude:</th><td>{jrjpdf["Latitude"][x]}</td></tr> \
                <tr><th scope="row">Longitude:</th><td>{jrjpdf["Longitude"][x]}</td></tr> \
                
                </tbody></table>'''
                folium.Marker([jrjpdf.iloc[x]['Latitude'], jrjpdf.iloc[x]['Longitude']], popup=popup, icon=folium.features.CustomIcon(img_url, icon_size=(40, 40))).add_to(map),
        # folium.Circle(
        #     radius=1000,
        #     location=[19.1465, 73.2538],
        #     popup="The Waterfront",
        #     color="crimson",
        #     fill=False,
        # ).add_to(map)
        # data = folium.LatLngPopup().add_to(map)
        map.add_child(folium.LatLngPopup())
        folium.LayerControl().add_to(map)
        MiniMap().add_to(map)
        map = map._repr_html_() 
        return map

def getstaticmap(h,w:None):
        location=[26.9371,  75.8122]
        # js_code = f"""
        #     <script>
        #         //LatLngPopup()  get lat long from the popup
        #         var LatLngPopup = function () {{
                
        #             }}
        #     </script>
        # """

        # html = f""" {js_code} """

        if w is None:
            map = folium.Map(location, height=h, zoom_start=12)
        else:
            map = folium.Map(location, height=h, width=w, zoom_start=12)
        # iframe = folium.IFrame(html, width=210, height=215)
        # popup = folium.Popup(iframe)
        # folium.Marker(location, popup, draggable=True).add_to(map)

        for x in range(0, len(jrjpdf)):
            if len(jrjpdf.iloc[x]["Police_Station"])>0:
                popup = f'''<table class="table" style="white-space:nowrap">\
                <thead class="table-dark"><tr><th scope="col" colspan="2" class="text-center">{jrjpdf["Police_Station"][x]}</th></tr></thead>\
                <tbody><tr><th scope="row">Address:</th><td>{jrjpdf["Address"][x]}</td></tr> \
                <tr><th scope="row">Phone Number:</th><td>{jrjpdf["Phone_Number"][x]}</td></tr> \
                <tr><th scope="row">Latitude:</th><td>{jrjpdf["Latitude"][x]}</td></tr> \
                <tr><th scope="row">Longitude:</th><td>{jrjpdf["Longitude"][x]}</td></tr> \
                
                </tbody></table>'''
                folium.Marker([jrjpdf.iloc[x]['Latitude'], jrjpdf.iloc[x]['Longitude']], popup=popup, icon=folium.features.CustomIcon(img_url, icon_size=(40, 40))).add_to(map),

        folium.Marker(location, draggable=True).add_to(map)
        map.add_child(folium.LatLngPopup())
        folium.plugins.Geocoder().add_to(map)
        map = map._repr_html_() 
        return map

def cardData():
    # tempDF = jrjpdf.copy() 
    sum_records=len(model_rjdf)
    sum_arrest=len(jrjpdf)
    # temp_domestic=tempDF[tempDF["Domestic"]==bool(True)]
    sum_domestic=(model_rjdf['ipc'].value_counts()).max()
    cards["dataAll"]=int(sum_records)
    cards["dataArrest"]=int(sum_arrest)
    cards["dataDomestic"]=int(sum_domestic) 
    # tempDFP = dfp.copy() 
    model_rjdf['age'] = model_rjdf['age'].astype(str)
    model_rjdf['age'] = model_rjdf['age'].str.extract('(\d+)').astype(float)
    sum_station=model_rjdf['age'].mean()
    cards["dataStations"]=int(sum_station)

def graphData():
    tempDF = dfg.copy()
    # tempDF['created']=tempDF['created'].astype(str)
    for x in range(0, len(tempDF)):
        if (tempDF.iloc[x]['YearS']) != None:
            print("***********YearS", tempDF)
            # tempDF = tempDF['YearS']
        if (tempDF.iloc[x]['YearE']) != None:
            print("***********YearE", tempDF)
        if (tempDF.iloc[x]['Type']) != None:
            print("***********Type", tempDF)
        if (tempDF.iloc[x]['Where']) != None:
            print("***********Where", tempDF)
        if (tempDF.iloc[x]['Arrest']) == True:
            print("***********Arrest", tempDF)
        if (tempDF.iloc[x]['Domestic']) == True:
            print("***********Domestic", tempDF)
        if (tempDF.iloc[x]['District']) == True:
            print("***********District", tempDF)
    # tempDF =  tempDF[''].isnull()
    # print("tempDF", tempDF)
    data = [
            {
            'title': 'Crime Data1',
            'dataX': [10,23,45,4,6,34,23],
            'dataY': ['A','B','C','D','E','F','G']
            },
            {
            'title': 'In which month, most no. of crime is recorded',
            'dataX': [10, 6, 15, 20, 23, 30, 33, 15, 13, 15, 20, 25],
            'dataY': ['Jan','Feb','Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            }
        ]
    return data





