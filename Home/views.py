from django.views import View
from django.shortcuts import render 
from CrimeMapping.views import ukdf, ukdfp, cards, cardData, graphData
from CrimeMapping.views import getstaticmap
import pandas as pd
from CrimeMapping.models import PoliceStationJaipurList, FirKarnataka
jaipur_police=pd.read_csv("CrimeMapping/data/jaipur_p.csv")
# Create your views here.
dfk=pd.read_csv("CrimeMapping/data/FIR_Details.csv")

class Home(View):
    def get(self, request):
        cardData()
        graphData()


        # for index, row in dfk.iterrows():

        #     data = {
        #         'District_Name': row['District_Name'],
        #         'UnitName': row['UnitName'],
        #         'FIRNo': row['FIRNo'],
        #         'RI': row['RI'],
        #         'Year': row['Year'],
        #         'Month': row['Month'],
        #         'Offence_From_Date': row['Offence_From_Date'],
        #         'Offence_To_Date': row['Offence_To_Date'],
        #         'FIR_Reg_DateTime': row['FIR_Reg_DateTime'],
        #         'FIR_Date': row['FIR_Date'],
        #         'FIR_Type': row['FIR_Type'],
        #         'FIR_Stage': row['FIR_Stage'],
        #         'Complaint_Mode': row['Complaint_Mode'],
        #         'CrimeGroup_Name': row['CrimeGroup_Name'],
        #         'CrimeHead_Name': row['CrimeHead_Name'],
        #         'Latitude': row['Latitude'],
        #         'Longitude': row['Longitude'],
        #         'ActSection': row['ActSection'],
        #         'IOName': row['IOName'],
        #         'KGID': row['KGID'],
        #         'Internal_IO': row['Internal_IO'],
        #         'Place_of_Offence': row['Place_of_Offence'],
        #         'Distance_from_PS': row['Distance_from_PS'],
        #         'Beat_Name': row['Beat_Name'],
        #         'Village_Area_Name': row['Village_Area_Name'],
        #         'Male': row['Male'],
        #         'Female': row['Female'],
        #         'Boy': row['Boy'],
        #         'Girl': row['Girl'],
        #         'Age_0': row['Age_0'],
        #         'VICTIM_COUNT': row['VICTIM_COUNT'],
        #         'Accused_Count': row['Accused_Count'],
        #         'Arrested_Male': row['Arrested_Male'],
        #         'Arrested_Female': row['Arrested_Female'],
        #         'Arrested_Count': row['Arrested_Count_No'],
        #         'Accused_ChargeSheeted_Count': row['Accused_ChargeSheeted_Count'],
        #         'Conviction_Count': row['Conviction_Count'],
        #         'FIR_ID': row['FIR_ID'],
        #         'Unit_ID': row['Unit_ID'],
        #         'Crime_No': row['Crime_No'],
        #     }
            
        #     FirKarnataka.objects.create(**data)

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


        #      ukdata.objects.create(**data)
        
        # return render(request, 'Home/home.html',{"cards":cards}) 

    def post(self, request):
        pass

