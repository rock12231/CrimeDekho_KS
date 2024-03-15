from django.views import View
from django.shortcuts import render 
from CrimeMapping.views import ukdf, ukdfp, cards, cardData, graphData
from CrimeMapping.views import getstaticmap
import pandas as pd
from CrimeMapping.models import PoliceStationJaipurList
jaipur_police=pd.read_csv("CrimeMapping/data/jaipur_p.csv")
# Create your views here.


class Home(View):
    def get(self, request):
        cardData()
        graphData()




        # tempDF = jaipur_police.copy()
        # print(tempDF)
        # print(type(tempDF))
        # for i in range (len(tempDF)):
        #     # Police_Station, Phone_Number,Address, Latitude,Longitude
        #     data = {
        #         'Police_Station' : tempDF['Police_Station'][i],	
        #         'Phone_Number' : tempDF['Phone_Number'][i],
        #         'Address' : tempDF['Address'][i],
        #         'Latitude' : tempDF['Latitude'][i],
        #         'Longitude' : tempDF['Longitude'][i],
        #     }
        #     PoliceStationJaipurList.objects.create(**data)
        #     print(data,".......................")



        # if request.user.is_authenticated:
        return render(request, 'Home/home.html',{"cards":cards, "map": getstaticmap(400,None) }) 
        # else:
            # return redirect('/')
        #Import CSV file to database


    
        #  Import CSV file to database RECORDS
        # tempDF =ukdf.copy()
        # for i in range (len(tempDF)):
        #      #tempDF.unique(i)
        #      data = {
        #         'caseno' : tempDF['caseno'][i],	
        #         'block' : tempDF['block'][i],
        #         'Type' : tempDF['Type'][i],
        #         'Type_desc' : tempDF['Type_desc'][i],
        #         'Where' : tempDF['Where'][i],
        #         'Arrest' : tempDF['Arrest'][i],
        #         'Domestic' : tempDF['Domestic'][i],
        #         'District' : tempDF['District'][i],
        #         'Community_area' : tempDF['Community_area'][i],
        #         'Year' : tempDF['Year'][i],
        #         'Latitude' : tempDF['Latitude'][i],
        #         'Longitude' : tempDF['Longitude'][i],
        #         'IPC':tempDF['IPC'][i],
        #         'Session':tempDF['Session'][i],
        #         'Day':tempDF['Day'][i],

        #     }
        #      print(data,".......................")


            #  ukdata.objects.create(**data)
        
        # return render(request, 'Home/home.html',{"cards":cards}) 

    def post(self, request):
        pass

