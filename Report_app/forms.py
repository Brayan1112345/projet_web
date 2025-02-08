from django import forms
from django.db import models
from Form_app.models import  Country, EconomicIndicator, Indicator_List

class reportForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        super(reportForm, self).__init__(*args, **kwargs)
        
        # Récupérer les objets pour le champ 'indicateur'
        indicators_obj = Indicator_List.objects.all()
        self.fields['indicateur'] = forms.ModelChoiceField(
            queryset=indicators_obj, 
            required=True,
            label="Sélectionner un indicateur"
        )

        # Récupérer les objets pour le champ 'pays'
        countries = Country.objects.all()
        self.fields['pays'] = forms.MultipleChoiceField(
            choices=[(country.ID_Country, country.Countryname) for country in countries],
            widget=forms.CheckboxSelectMultiple,
            label="Sélectionner les pays"
        )

        # Récupérer les années min et max pour 'annee_min' et 'annee_max'
        try:
            min_year = EconomicIndicator.objects.aggregate(models.Min('Year'))['Year__min'] 
            max_year = EconomicIndicator.objects.aggregate(models.Max('Year'))['Year__max']
        except EconomicIndicator.DoesNotExist:
            min_year = 1990
            max_year = 2023
        
        self.fields['annee_min'] = forms.ChoiceField(
            choices=[(year, year) for year in range(min_year, max_year + 1)],
            label="De : "
        )
        self.fields['annee_max'] = forms.ChoiceField(
            choices=[(year, year) for year in range(min_year, max_year + 1)],
            label="A : "
        )

    class Meta:
        fields = ['indicateur', 'pays', 'annee_min', 'annee_max']