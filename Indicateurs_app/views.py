from django.shortcuts import render, get_object_or_404
from Form_app.models import Country, Indicator_List, EconomicIndicator
import json
import pandas as pd
from django.http import JsonResponse
from decimal import Decimal

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
    
    # Récupérer les données
    data = EconomicIndicator.objects.filter(
        Country_id=selected_country,
        Year__gte=start_year,
        Year__lte=end_year
    ).values('Year', indicator.Name_EconomicIndicator)
    
    # Convertir en listes pour JSON et convertir les Decimal en float
    df = pd.DataFrame(list(data))
    graph_data = {
        'x': df['Year'].tolist(),
        'y': [float(y) if isinstance(y, Decimal) else y for y in df[indicator.Name_EconomicIndicator].tolist()],
        'indicator_name': indicator.Name
    }
    
    context = {
        'indicator': indicator,
        'countries': countries,
        'selected_country': selected_country,
        'start_year': start_year,
        'end_year': end_year,
        'graph_data': json.dumps(graph_data)
    }
    
    return render(request, 'Indicateurs_app/visualization.html', context)