# Generated by Django 4.0.6 on 2024-03-18 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CrimeMapping', '0026_complainantsdetails_firkarnataka_rowdyshetters_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MOBDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('District_Name', models.CharField(max_length=255, null=True)),
                ('Unit_Name', models.CharField(max_length=255, null=True)),
                ('Name', models.CharField(max_length=255, null=True)),
                ('Person_No', models.CharField(max_length=255, null=True)),
                ('MOB_Number', models.CharField(max_length=255, null=True)),
                ('MobOpenDate', models.CharField(max_length=255, null=True)),
                ('MOB_Open_Year', models.FloatField(null=True)),
                ('Arrested_By', models.CharField(max_length=255, null=True)),
                ('KGID', models.CharField(max_length=255, null=True)),
                ('Caste', models.CharField(max_length=255, null=True)),
                ('Grading', models.FloatField(null=True)),
                ('Occupation', models.CharField(max_length=255, null=True)),
                ('PS_Native', models.CharField(max_length=255, null=True)),
                ('PS_District', models.CharField(max_length=255, null=True)),
                ('Offender_Class', models.FloatField(null=True)),
                ('Crime_No', models.CharField(max_length=255, null=True)),
                ('ActSection', models.CharField(max_length=255, null=True)),
                ('Brief_Fact', models.CharField(max_length=255, null=True)),
                ('Present_WhereAbouts', models.CharField(max_length=255, null=True)),
                ('Gang_Strength', models.IntegerField(null=True)),
                ('Ident_Officer', models.CharField(max_length=255, null=True)),
                ('officer_rank', models.CharField(max_length=255, null=True)),
                ('Crime_Group1', models.CharField(max_length=255, null=True)),
                ('Crime_Head2', models.CharField(max_length=255, null=True)),
                ('class1', models.CharField(max_length=255, null=True)),
                ('AGE', models.FloatField(null=True)),
                ('PresentAge', models.CharField(max_length=255, null=True)),
                ('DOB', models.CharField(max_length=255, null=True)),
                ('Address', models.CharField(max_length=255, null=True)),
                ('SEX', models.CharField(max_length=255, null=True)),
                ('Locality', models.CharField(max_length=255, null=True)),
                ('LastUpdatedDate', models.CharField(max_length=255, null=True)),
            ],
        ),
    ]
