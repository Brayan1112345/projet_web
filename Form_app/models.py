from django.db import models
import uuid

# Create your models here.

class Country(models.Model):
    ID_Country = models.IntegerField(primary_key=True) #Par exemple 237 pour le cameroun
    Countryname = models.CharField(max_length=40, unique=True)
    Code = models.CharField(max_length=3)#Par exemple CMR pour le Cameroun

    def __str__(self):
        return self.Countryname
    
    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"



class EconomicIndicatorClass(models.Model):
    ID_class = models.AutoField(primary_key=True)
    Class_name = models.CharField(max_length=30, unique=True, verbose_name="Catégorie")
    def __str__(self):
        return self.Class_name



class EconomicIndicator(models.Model):#Pour un pays donnée, à une année donnée, on a une liste d'indicateurs
    ID_Indicator = models.CharField(primary_key=True, max_length=24, editable=False)
    Year = models.IntegerField()
    GDP = models.DecimalField(max_digits=15, decimal_places=3)
    Inflation_Rate = models.DecimalField(max_digits=10, decimal_places=4)
    Population = models.IntegerField()
    Population_growth = models.DecimalField(max_digits=10, decimal_places=3)
    Balance_com = models.DecimalField(max_digits=15, decimal_places=4)
    IDE = models.DecimalField(max_digits=15, decimal_places=3)
    GDP_growth = models.DecimalField(max_digits=10, decimal_places=3)
    GDP_per_capita = models.DecimalField(max_digits=15, decimal_places=3)
    GNI = models.DecimalField(max_digits=15, decimal_places=3)
    GNI_per_capita = models.DecimalField(max_digits=10, decimal_places=3)
    Life_exp = models.DecimalField(max_digits=10, decimal_places=3)
    Maternal_mortality_ratio = models.DecimalField(max_digits=10, decimal_places=3)
    Mortality_rate_infant = models.DecimalField(max_digits=10, decimal_places=3)
    Country = models.ForeignKey('Country', on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return f'{self.Country.Countryname} ({self.Year}) ' 

    def save(self, *args, **kwargs):
        self.ID_Indicator=f'{self.Country.Code}, {self.Year}'

        super().save(*args, **kwargs)


class Indicator_List(models.Model):
    ID_Indicator = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100)
    Description = models.TextField(max_length=2000)
    Name_EconomicIndicator = models.CharField(max_length=25)
    
    Class = models.ForeignKey('EconomicIndicatorClass', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.Name
    
    class Meta:
        verbose_name = "Indicator"
        verbose_name_plural = "Indicators"


