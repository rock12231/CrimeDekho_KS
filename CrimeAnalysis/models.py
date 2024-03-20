from django.db import models

# Create your models here.


class Fir_Karnataka(models.Model):
    District_Name = models.CharField(max_length=255, null=True)
    UnitName = models.CharField(max_length=255, null=True)
    FIRNo = models.CharField(max_length=255, null=True)
    RI = models.IntegerField(null=True)
    Year = models.IntegerField(null=True)
    Month = models.IntegerField(null=True)
    Offence_From_Date = models.CharField(max_length=255, null=True)
    Offence_To_Date = models.CharField(max_length=255, null=True)
    FIR_Reg_DateTime = models.CharField(max_length=255, null=True)
    FIR_Date = models.CharField(max_length=255, null=True)
    FIR_Type = models.CharField(max_length=255, null=True)
    FIR_Stage = models.CharField(max_length=255, null=True)
    Complaint_Mode = models.CharField(max_length=255, null=True)
    CrimeGroup_Name = models.CharField(max_length=255, null=True)
    CrimeHead_Name = models.CharField(max_length=255, null=True)
    Latitude = models.FloatField(null=True)
    Longitude = models.FloatField(null=True)
    ActSection = models.CharField(max_length=255, null=True)
    IOName = models.CharField(max_length=255, null=True)
    KGID = models.CharField(max_length=255, null=True)
    Internal_IO = models.IntegerField(null=True)
    Place_of_Offence = models.CharField(max_length=255, null=True)
    Distance_from_PS = models.CharField(max_length=255, null=True)
    Beat_Name = models.CharField(max_length=255, null=True)
    Village_Area_Name = models.CharField(max_length=255, null=True)
    Male = models.IntegerField(null=True)
    Female = models.IntegerField(null=True)
    Boy = models.IntegerField(null=True)
    Girl = models.IntegerField(null=True)
    Age_0 = models.IntegerField(null=True)
    VICTIM_COUNT = models.IntegerField(null=True)
    Accused_Count = models.IntegerField(null=True)
    Arrested_Male = models.IntegerField(null=True)
    Arrested_Female = models.IntegerField(null=True)
    Arrested_Count = models.IntegerField(null=True)
    Accused_ChargeSheeted_Count = models.IntegerField(null=True)
    Conviction_Count = models.IntegerField(null=True)
    FIR_ID = models.IntegerField(null=True)
    Unit_ID = models.IntegerField(null=True)
    Crime_No = models.IntegerField(null=True)
    
    class Meta:
        db_table = 'Fir_Karnataka'
        app_label = 'CrimeAnalysis'
        managed = True
    
