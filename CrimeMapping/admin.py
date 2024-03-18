from django.contrib import admin

# Register your models here.
from CrimeMapping.models import Crimes2001, ContactUs, GraphData, PoliceStationList ,ukdata, UKPoliceStationList, FirData, RajPolice, PoliceStationJaipurList, FirKarnataka, VictimInfo, RowdyShetters, ComplainantsDetails

class Crime(admin.ModelAdmin):
    list_display = ('id','caseno', 'block', 'Type', 'Type_desc', 'Where', 'Arrest', 'Domestic', 'District', 'Community_area', 'Year', 'Latitude', 'Longitude', 'Date')
admin.site.register(Crimes2001, Crime)


class ContactAdmin(admin.ModelAdmin):
    list_display = ('id','first_name', 'last_name', 'User_email', 'User_subject', 'User_message', 'date_created')
admin.site.register(ContactUs, ContactAdmin)

class GraphDataAdmin(admin.ModelAdmin):
    list_display = ('id','created', 'title', 'Type', 'Where', 'Arrest', 'Domestic', 'District', 'YearS', 'YearE')
admin.site.register(GraphData, GraphDataAdmin)

class PoliceStationListAdmin(admin.ModelAdmin):
    list_display = ('id','district', 'disname', 'address', 'city', 'zip', 'website', 'latitude', 'longitude')
admin.site.register(PoliceStationList, PoliceStationListAdmin)

#Rajasthan Police
class UKPoliceAdmin(admin.ModelAdmin):
    list_display = ('id','district', 'disname', 'address', 'city', 'zip', 'website', 'latitude', 'longitude')
admin.site.register(UKPoliceStationList, UKPoliceAdmin)

class ukAdmin(admin.ModelAdmin):
     list_display = ('caseno', 'block', 'Type', 'Type_desc', 'Where', 'Arrest', 'Domestic', 'District', 'Community_area', 'Year', 'Latitude', 'Longitude', 'IPC','Session','Day','Date')
admin.site.register(ukdata,ukAdmin )

class FirDataAdmin(admin.ModelAdmin):
     list_display = ('case_no', 'date', 'police_station', 'ipc', 'ipc_no', 'time', 'CrPC', 'date_happened', 'date_reported', 'format_fir_type', 'address',
                    'distance_police_station', 'name', 'father_name', 'age', 'nationality', 'office_address', 'additional_info', 'suspected_individual', 
                    'latitude', 'longitude', 'file', 'language')
admin.site.register(FirData,FirDataAdmin)

class RajPoliceAdmin(admin.ModelAdmin):
     list_display = ('address', 'latitude', 'longitude')
admin.site.register(RajPolice,RajPoliceAdmin)


class PoliceStationJaipurListAdmin(admin.ModelAdmin):
     list_display = ('Police_Station', 'Phone_Number','Address', 'Latitude', 'Longitude')
admin.site.register(PoliceStationJaipurList,PoliceStationJaipurListAdmin)


class FirKaranatakaAdmin(admin.ModelAdmin):
    list_display = ('District_Name', 'UnitName', 'FIRNo', 'RI', 'Year', 'Month', 'Offence_From_Date', 'Offence_To_Date', 'FIR_Reg_DateTime', 'FIR_Date', 'FIR_Type', 'FIR_Stage', 'Complaint_Mode', 'CrimeGroup_Name', 'CrimeHead_Name', 'Latitude', 'Longitude','ActSection', 'IOName', 'KGID', 'Internal_IO', 'Place_of_Offence', 'Distance_from_PS', 'Beat_Name', 'Village_Area_Name', 'Male', 'Female', 'Boy', 'Girl', 'Age_0', 'VICTIM_COUNT', 'Accused_Count','Arrested_Male', 'Arrested_Female', 'Arrested_Count', 'Accused_ChargeSheeted_Count', 'Conviction_Count',   'FIR_ID', 'Unit_ID', 'Crime_No')
admin.site.register(FirKarnataka, FirKaranatakaAdmin)

class VictimInfoAdmin(admin.ModelAdmin):
    list_display = ('District_Name', 'UnitName', 'FIRNo', 'Year', 'Month', 'VictimName', 'age', 'Caste', 'Profession', 'Sex', 'PresentAddress', 'PresentCity', 'PresentState', 'PermanentAddress', 'PermanentCity', 'PermanentState', 'Nationality_Name', 'DOB', 'PersonType', 'InjuryType', 'Injury_Nature', 'Crime_No', 'Arr_ID', 'Victim_ID')
admin.site.register(VictimInfo, VictimInfoAdmin)


class RowdyShettersAdmin(admin.ModelAdmin):
    list_display = ('District_Name', 'Unit_Name', 'Rowdy_Sheet_No', 'Name', 'AliasName', 'RS_Open_Date', 'Rowdy_Classification_Details', 'Activities_Description', 'Rowdy_Category', 'PrevCase_Details', 'Address', 'Age', 'Father_Name', 'Source_Of_Income', 'LastUpdatedDate', 'PresentWhereabout')
admin.site.register(RowdyShetters, RowdyShettersAdmin)


class ComplainantsDetailsAdmin(admin.ModelAdmin):
    list_display = ('District_Name', 'UnitName', 'FIRNo', 'Year', 'Month', 'ComplainantName', 'Relation', 'RelationshipName', 'DateOfBirth', 'Age', 'Sex', 'Nationality', 'Occupation', 'Address', 'City', 'State', 'Pincode', 'Caste', 'Religion', 'FIR_ID', 'Unit_ID', 'Complaint_ID')
admin.site.register(ComplainantsDetails, ComplainantsDetailsAdmin)
