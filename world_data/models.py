from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=20)
    otp = models.CharField(max_length=6)


class Country(models.Model):
    code = models.CharField(primary_key=True, max_length=3)
    name = models.CharField(max_length=52)
    continent = models.CharField(max_length=13)
    region = models.CharField(max_length=26)
    surface_area = models.FloatField()
    indep_year = models.PositiveIntegerField(null=True, blank=True)
    population = models.PositiveIntegerField()
    life_expectancy = models.FloatField(null=True, blank=True)
    gnp = models.FloatField(null=True, blank=True)
    gnp_old = models.FloatField(null=True, blank=True)
    local_name = models.CharField(max_length=45)
    government_form = models.CharField(max_length=45)
    head_of_state = models.CharField(max_length=60, null=True, blank=True)
    # Rename the related_name for the capital field
    capital = models.OneToOneField('City', related_name='country_as_capital', on_delete=models.SET_NULL, null=True, blank=True)
    code2 = models.CharField(max_length=2)

    def __str__(self):
        return self.name


class City(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=35)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    district = models.CharField(max_length=20)
    population = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class CountryLanguage(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    language = models.CharField(max_length=30)
    is_official = models.BooleanField()
    percentage = models.FloatField()

    def __str__(self):
        return self.language