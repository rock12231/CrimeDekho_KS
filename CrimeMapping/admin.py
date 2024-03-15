from django.contrib import admin

# Register your models here.
from CrimeMapping.models import Crimes2001, ContactUs, GraphData, PoliceStationList ,ukdata, UKPoliceStationList, FirData, RajPolice, PoliceStationJaipurList

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