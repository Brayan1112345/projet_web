from django import forms
from django.db import models
from Form_app.models import Country, EconomicIndicator,  Indicator_List, EconomicIndicatorClass
import datetime

class export_to_csv_Form(forms.Form):

    indicators = Indicator_List.objects.all()
    indicateurs = forms.MultipleChoiceField(
        choices=[(indicator.ID_Indicator, indicator.Name) for indicator in indicators],
        widget=forms.CheckboxSelectMultiple,
        label="Sélectionner les indicateurs"
    )

    countries = Country.objects.all()
    pays = forms.MultipleChoiceField(
        choices=[(country.ID_Country, country.Countryname) for country in countries],
        widget=forms.CheckboxSelectMultiple,
        label="Sélectionner les pays"
    )

    # Si indicators n'est pas vide, obtenir l'annee_min et l'annee_max
    if indicators:
        min_year = EconomicIndicator.objects.aggregate(models.Min('Year'))['Year__min']
        max_year = EconomicIndicator.objects.aggregate(models.Max('Year'))['Year__max']
    else:
        max_year=datetime.datetime.now().year
        min_year=1990
    
    annee_min = forms.ChoiceField(
        choices=[(year, year) for year in range(min_year, max_year)],
        label="De : "
    )
    annee_max = forms.ChoiceField(
        choices=[(year, year) for year in range(min_year, max_year )],
        label="A : "
    )

    class Meta:
        fields = ['indicateurs', 'pays', 'annee_min', "annee_max"]
