from django.views.generic import TemplateView
from django.shortcuts import render
from Form_app.models import Country, EconomicIndicator
from django.db.models import Max


class AboutView(TemplateView):
    """Vue pour la page À propos"""
    template_name = "pages/about.html"

class ContactView(TemplateView):
    """Vue pour la page Contact"""
    template_name = "pages/contact.html"


def home(request):
    # Récupérer tous les pays
    countries = Country.objects.all()
    
    # Récupérer les 5 dernières années de données
    latest_year = EconomicIndicator.objects.aggregate(Max('Year'))['Year__max']
    years_range = range(latest_year - 4, latest_year + 1)
    
    # Préparer les données pour le graphique PIB
    gdp_data = EconomicIndicator.objects.filter(
        Year__in=years_range,
        Country__Countryname='Cameroun'  
    ).order_by('Year').values('Year', 'GDP_per_capita')
    
    # Préparer les données pour le graphique Population
    population_data = EconomicIndicator.objects.filter(
        Year__in=years_range,
        Country__Countryname='Guinée équatoriale'
    ).order_by('Year').values('Year', 'Population')
    
    # Convertir les données en format JSON pour JavaScript
    gdp_years = [str(data['Year']) for data in gdp_data]
    gdp_values = [float(data['GDP_per_capita']) for data in gdp_data]
    population_years = [str(data['Year']) for data in population_data]
    population_values = [data['Population'] for data in population_data]
    
    context = {
        'countries': countries,
        'gdp_years': gdp_years,
        'gdp_values': gdp_values,
        'population_years': population_years,
        'population_values': population_values,
    }
    
    return render(request, 'pages/home.html', context)