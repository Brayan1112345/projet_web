from django.shortcuts import render, get_object_or_404
from Form_app.models import Country, Indicator_List, EconomicIndicator
import plotly.express as px
import pandas as pd
from django.http import JsonResponse
    

def demographic_indicators(request):
    # Filtrer les indicateurs démographiques
    demographic_indicators = Indicator_List.objects.filter(
        Class__ID_class=3
    ).select_related('Class')
    
    context = {
        'demographic_indicators': demographic_indicators,
    }

    return render(request, 'Indicateurs_app/ind_dem.html', context)


def economic_indicators(request):
    # Filtrer les indicateurs économiques
    economic_indicators = Indicator_List.objects.filter(
        Class__ID_class=2
    ).select_related('Class')
    
    context = {
        'economic_indicators': economic_indicators,
    }

    return render(request, 'Indicateurs_app/ind_eco.html', context)


def social_indicators(request):
    # Filtrer les indicateurs sociaux
    social_indicators = Indicator_List.objects.filter(
        Class__ID_class=1
    ).select_related('Class')
    
    context = {
        'social_indicators': social_indicators,
    }

    return render(request, 'Indicateurs_app/ind_soc.html', context)


def visualization(request, indicator_id):
    # Récupérer l'indicateur spécifique
    indicator = get_object_or_404(Indicator_List, ID_Indicator=indicator_id)
    countries = Country.objects.all()
    
    # Valeurs par défaut
    default_country = Country.objects.get(Countryname='Cameroun')
    start_year = request.POST.get('start_year', '2000')
    end_year = request.POST.get('end_year', '2020')
    selected_country = request.POST.get('country', default_country.ID_Country)

    # Convertir en entiers
    start_year = int(start_year)
    end_year = int(end_year)
    selected_country = int(selected_country)

    # Récupérer les données pour le graphique
    data = EconomicIndicator.objects.filter(
        Country_id=selected_country,
        Year__gte=start_year,
        Year__lte=end_year
    ).values('Year', indicator.Name_EconomicIndicator)

    # Créer un DataFrame pour Plotly
    df = pd.DataFrame(list(data))
    
    # Créer le graphique avec Plotly
    fig = px.line(
        df, 
        x='Year', 
        y=indicator.Name_EconomicIndicator,
        title=f'Évolution de {indicator.Name} ({start_year}-{end_year})'
    )
    
    # Convertir le graphique en JSON pour l'affichage
    chart_json = fig.to_json()

    context = {
        'indicator': indicator,
        'countries': countries,
        'selected_country': selected_country,
        'start_year': start_year,
        'end_year': end_year,
        'chart_json': chart_json
    }
    
    return render(request, 'Indicateurs_app/visualization.html', context)
