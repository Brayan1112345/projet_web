from django import forms
from django.db import models
from .models import Country, EconomicIndicator,   EconomicIndicatorClass , Indicator_List
import datetime
#from utils.helpers import get_model_content_type, create_table_if_not_exists

class CountryYearForm(forms.Form):
    class Meta:
        model = EconomicIndicator
        fields = ['Country', 'Year']
    # Liste déroulante pour sélectionner un pays
    country = forms.ModelChoiceField(queryset=Country.objects.all(), label="Sélectionner le pays", required=True)
    # Champ pour sélectionner l'année
    year = forms.IntegerField(label="Sélectionner l'année", required=True, min_value=1900, max_value=datetime.datetime.now().year)


class IndicatorValuesForm(forms.Form):

    class Meta:
        model = EconomicIndicator
        fields = ['ID_Indicator','Country', 'Year', 'GDP', 'Inflation_Rate', 'Population', 'Population_growth', 'Balance_com', 'IDE', 'GDP_growth', 'GDP_per_capita',
                    'GNI', 'GNI_per_capita', 'Life_exp', 'Maternal_mortality_ratio', 'Mortality_rate_infant']


    Inflation_Rate = forms.DecimalField(label="Taux d'inflation (en %)", required=True, max_digits=5, decimal_places=2)
    Population = forms.IntegerField(label="Nombre d'habitants", required=True)
    Population_growth = forms.DecimalField(label="Taux de croissance de la population (en %)", required=True, max_digits=5, decimal_places=2)
    Balance_com = forms.DecimalField(label="Balance Commerciale (en FCFA)", required=True, max_digits=12, decimal_places=2)
    IDE = forms.DecimalField(label="Investissement Directs Etrangers (en FCFA)", required=True, max_digits=12, decimal_places=2)
    GDP = forms.DecimalField(label="Produit Intérieur Brut (en FCFA)", required=True, max_digits=15, decimal_places=2)
    GDP_growth = forms.DecimalField(label="Taux de croissance économique (en %)", required=True, max_digits=5, decimal_places=2)
    GDP_per_capita = forms.DecimalField(label="Croissance par habitant (en %)", required=True, max_digits=12, decimal_places=2)
    GNI = forms.DecimalField(label="Revenu National Brut (en FCFA)", required=True, max_digits=12, decimal_places=2)
    GNI_per_capita = forms.DecimalField(label="Revenu National Brut par habitant (en FCFA)", required=True, max_digits=10, decimal_places=2)
    Life_exp = forms.DecimalField(label="Espérance de vie à la naissance (en année)", required=True, max_digits=5, decimal_places=2)
    Maternal_mortality_ratio = forms.DecimalField(label="Taux de mortalité maternelle (en %)", required=True, max_digits=5, decimal_places=2)
    Mortality_rate_infant = forms.DecimalField(label="Taux de mortalité infantile (en %)", required=True, max_digits=5, decimal_places=2)


class ConfirmationForm(forms.Form):
    """
    Formulaire de confirmation de suppression avec deux boutons.
    - Un bouton 'Supprimer' pour confirmer la suppression
    - Un bouton 'Annuler' pour revenir en arrière sans action
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        