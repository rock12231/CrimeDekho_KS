from django.db import models

# STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])

# Create your models here.
class Crimes2001(models.Model):
    caseno = models.CharField(max_length=20)
    Date = models.DateTimeField(auto_now_add=True)
    block = models.CharField(max_length=100)
    Type = models.CharField(max_length=100)
    Type_desc = models.CharField(max_length=100)
    Where = models.CharField(max_length=100)
    Arrest = models.BooleanField()
    Domestic = models.BooleanField()
    District = models.IntegerField()
    Community_area = models.FloatField(null=True)
    Year = models.IntegerField()
    Latitude = models.FloatField(max_length=20, null=True)
    Longitude = models.FloatField(max_length=20, null=True)
    # IPC = models.CharField(max_length=20)	
    
# district,disname,address,city,zip,website,latitude,longitude
class PoliceStationList(models.Model):
    Date = models.DateTimeField(auto_now_add=True)
    district = models.IntegerField()
    disname = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zip = models.IntegerField()
    website = models.CharField(max_length=500)
    latitude = models.FloatField(max_length=20, null=True)
    longitude = models.FloatField(max_length=20, null=True)
    
# UTTRAKHAND POLICE DATA district,disname,address,city,zip,website,latitude,longitude
class UKPoliceStationList(models.Model):
    Date = models.DateTimeField(auto_now_add=True)
    district = models.IntegerField()
    disname = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zip = models.IntegerField()
    website = models.CharField(max_length=500)
    latitude = models.FloatField(max_length=20, null=True)
    longitude = models.FloatField(max_length=20, null=True)    
    
class ContactUs(models.Model):
    first_name = models.CharField(max_length=50,default='')
    last_name = models.CharField(max_length=50,default='')
    User_email = models.EmailField( max_length=50,default='')
    User_subject = models.CharField(max_length=100,default='')
    User_message = models.TextField( max_length=1000,default='')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.User_email

# Uttrakhand data
class ukdata(models.Model):
    caseno = models.CharField(max_length=20)
    Date = models.DateTimeField(auto_now_add=True)
    block = models.CharField(max_length=100)
    Type = models.CharField(max_length=100)
    Type_desc = models.CharField(max_length=100)
    Where = models.CharField(max_length=100)
    Arrest = models.BooleanField()
    Domestic = models.BooleanField()
    District = models.IntegerField()
    Community_area = models.FloatField(null=True)
    Year = models.IntegerField()
    Latitude = models.FloatField(max_length=20, null=True)
    Longitude = models.FloatField(max_length=20, null=True)
    IPC = models.CharField(max_length=20, null=True)
    Session = models.CharField(max_length=20, null=True)
    Day = models.CharField(max_length=20, null=True)

    
getAll = Crimes2001.objects.all()

AllYear = list(getAll.values_list('Year',flat=True).distinct())
TupleYear = sorted([(item, item) for item in AllYear])

AllType = list(getAll.values_list('Type',flat=True).distinct())
TupleType = sorted([(item, item) for item in AllType])

AllBlock = list(getAll.values_list('block',flat=True).distinct())
TupleBlock = sorted([(item, item) for item in AllBlock])

AllWhere = list(getAll.values_list('Where',flat=True).distinct())
TupleWhere = sorted([(item, item) for item in AllWhere])

AllDistrict = list(getAll.values_list('District',flat=True).distinct())
TupleDistrict = sorted([(item, item) for item in AllDistrict])

class GraphData(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.TextField(null=True)
    Type = models.TextField(choices=TupleType, blank=True, null=True)
    Where = models.TextField(choices=TupleWhere, blank=True, null=True)
    Arrest = models.BooleanField(default=False)
    Domestic = models.BooleanField(default=False)
    District = models.IntegerField(choices=TupleDistrict, blank=True, null=True)
    YearS = models.IntegerField(choices=TupleYear, blank=True, null=True)
    YearE = models.IntegerField(choices=TupleYear, blank=True, null=True)

class FirData(models.Model):
    case_no	= models.TextField(null=True)
    date = models.TextField(null=True)
    police_station = models.TextField(null=True)
    ipc	= models.TextField(null=True)
    ipc_no = models.TextField(null=True)
    time =models.TextField(null=True)
    CrPC = models.TextField(null=True)	
    date_happened = models.TextField(null=True)
    date_reported= models.TextField(null=True)
    format_fir_type= models.TextField(null=True)
    address	= models.TextField(null=True)
    distance_police_station	= models.TextField(null=True)
    name= models.TextField(null=True)
    father_name	= models.TextField(null=True)
    age	= models.TextField(null=True)
    nationality	= models.TextField(null=True)
    office_address= models.TextField(null=True)
    additional_info	= models.TextField(null=True)
    suspected_individual = models.TextField(null=True)	
    latitude = models.TextField(null=True, blank=True)
    longitude = models.TextField(null=True, blank=True)
    file = models.URLField(max_length=200)
    language = models.TextField(null=True)

class RajPolice(models.Model):
    address=models.TextField(null=True)
    latitude=models.FloatField(max_length=20, null=True)
    longitude=models.FloatField(max_length=20, null=True)


class PoliceStationJaipurList(models.Model):
    Police_Station=models.TextField(null=True)
    Phone_Number=models.TextField(null=True)
    Address=models.TextField(null=True)
    Latitude=models.FloatField(max_length=20, null=True)
    Longitude=models.FloatField(max_length=20, null=True)