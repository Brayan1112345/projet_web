from django.shortcuts import render, redirect
from Form_app.models import Country, EconomicIndicator, Indicator_List, EconomicIndicatorClass
from django.http import JsonResponse
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from plotly.io import to_image
from math import ceil
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
from django.db.models import Avg, StdDev
import json
from django.views.decorators.http import require_GET
from scipy import stats




INDICATORS = [
        {'id': 'GDP', 'name': 'PIB', 'description': 'Produit Intérieur Brut : c\'est la production économique totale d\'un pays au cours d\'une année'},
        {'id': 'Inflation_Rate', 'name': 'Taux d\'inflation', 'description': 'Taux d\'inflation : c\'est l\'augmentation généralisée des prix des biens et services dans une économie'},
        {'id': 'Population', 'name': 'Population', 'description': 'Population : c\'est le nombre total d\'habitants dans un pays'},
        {'id': 'GDP_growth', 'name': 'Croissance du PIB', 'description': 'Taux de croissance du PIB : c\'est la variation annuelle du PIB en pourcentage'},
        {'id': 'Balance_com', 'name': 'Balance commerciale', 'description': 'Balance commerciale : c\'est le solde représentant la différence entre les exportations et importations de biens et services'},
        {'id': 'IDE', 'name': 'Investissements directs étrangers', 'description': ' IDE : ce sont les mouvements internationaux de capitaux significatifs réalisés par les étrangers dans un pays'},
        {'id': 'GDP_per_capita', 'name': 'PIB par habitant', 'description': 'PIB par habitant : c\'est PIB divisé par la population totale'},
        {'id': 'GNI', 'name': 'RNB', 'description': 'Revenu National Brut: c\'est le produit intérieur brut plus entre autres les revenus nets reçus de l\'étranger pour la rémunération des salariés'},
        {'id': 'GNI_per_capita', 'name': 'RNB par habitant', 'description': 'RNB par habitant : c\'est la moyenne des revenus générés dans un pays par habitant au cours d \'une année'},
        {'id': 'Life_exp', 'name': 'Espérance de vie', 'description': 'Espérance de vie: c\'est le nombre d\'années moyen de vie de la population d\'un pays '},
        {'id': 'Population_growth', 'name': 'Croissance démographique', 'description': 'Croissance démographique : c\'est la variation annuelle de la population en PIB'},
    ]



### POUR COMPARER PLUSIEURS PAYS 
def compare_countries(request):
    
    statistics = [
        {'id': 'mean', 'name': 'Moyenne'},
        {'id': 'std', 'name': 'Écart-type'},
        {'id': 'var', 'name': 'Variance'},
        {'id': 'median', 'name': 'Médiane'},
        {'id': 'seasonality', 'name': 'Saisonnalité'},
        {'id': 'skewness', 'name': 'Asymétrie'},
        {'id': 'kurtosis', 'name': 'Aplatissement'}
    ]
    
    countries = Country.objects.all().values('ID_Country', 'Countryname')
    
    context = {
        'indicators': INDICATORS,
        'countries': list(countries),
        'statistics': statistics,
        'start_year': 2000,
        'end_year': 2023,
    }
    
    return render(request, 'Visualisation_app/Compare_countries.html', context)



@require_GET
def get_country_data(request):
    try:
        indicator = request.GET.get('indicator')
        country_ids = request.GET.getlist('countries[]')
        start_year = int(request.GET.get('start_year', 2000))
        end_year = int(request.GET.get('end_year', 2020))
        selected_stats = request.GET.getlist('statistics[]')
        
        if not indicator or not country_ids:
            return JsonResponse({'error': 'Veuillez sélectionner un indicateur et au moins un pays'})
        
        data = {}
        stats = {}
        
        for country_id in country_ids:
            country_data = EconomicIndicator.objects.filter(
                Country_id=country_id,
                Year__gte=start_year,
                Year__lte=end_year
            ).values('Year', indicator)
            
            # Convertir les DecimalField en float pour la sérialisation JSON
            values = [float(entry[indicator]) if entry[indicator] is not None else None for entry in country_data]
            years = [entry['Year'] for entry in country_data]
            
            if not values:
                continue
                
            data[country_id] = {
                'years': years,
                'values': values
            }
            
            values = [v for v in values if v is not None]  # Filtrer les valeurs None
            
            # Calcul des statistiques sélectionnées
            stats[country_id] = calculate_statistics(values, selected_stats)
        
        # Récupérer la description de l'indicateur
        indicator_info = next((ind for ind in INDICATORS if ind['id'] == indicator), None)
        description = indicator_info['description'] if indicator_info else ''
        
        return JsonResponse({
            'data': data,
            'stats': stats,
            'description': description
        })
        
    except Exception as e:
        return JsonResponse({
            'error': f'Erreur lors de la récupération des données : {str(e)}'
        }, status=400)



def calculate_statistics(values, selected_stats):
    stats = {}
    if not values:
        return stats
        
    for stat in selected_stats:
        try:
            if stat == 'mean':
                stats['mean'] = float(np.mean(values))
            elif stat == 'std':
                stats['std'] = float(np.std(values))
            elif stat == 'var':
                stats['var'] = float(np.var(values))
            elif stat == 'median':
                stats['median'] = float(np.median(values))
            elif stat == 'seasonality':
                if len(values) >= 4:
                    series = pd.Series(values)
                    stats['seasonality'] = float(series.diff().std())
                else:
                    stats['seasonality'] = None
            elif stat == 'skewness':
                stats['skewness'] = float(pd.Series(values).skew())
            elif stat == 'kurtosis':
                stats['kurtosis'] = float(pd.Series(values).kurtosis())
        except Exception:
            stats[stat] = None
            
    return stats





###    POUR COMPARER PLUSIEURS INDICATEURS ####
def compare_indicators(request):
    statistics = [
        {'id': 'mean', 'name': 'Moyenne'},
        {'id': 'std', 'name': 'Écart-type'},
        {'id': 'var', 'name': 'Variance'},
        {'id': 'median', 'name': 'Médiane'},
        {'id': 'seasonality', 'name': 'Saisonnalité'},
        {'id': 'skewness', 'name': 'Asymétrie'},
        {'id': 'kurtosis', 'name': 'Aplatissement'}
    ]
    
    countries = Country.objects.all().values('ID_Country', 'Countryname')
    
    context = {
        'indicators': INDICATORS,
        'countries': list(countries),
        'statistics': statistics,
        'start_year': 2000,
        'end_year': 2020,
        'default_stats': ['mean', 'std']  # Statistiques sélectionnées par défaut
    }
    
    return render(request, 'Visualisation_app/compare_indicators.html', context)



@require_GET
def get_indicator_data(request):
    try:
        country_id = request.GET.get('country')
        indicator_ids = request.GET.getlist('indicators[]')
        start_year = int(request.GET.get('start_year', 2000))
        end_year = int(request.GET.get('end_year', 2020))
        selected_stats = request.GET.getlist('statistics[]')
        
        if not country_id or not indicator_ids or len(indicator_ids) > 4:
            return JsonResponse({
                'error': 'Veuillez sélectionner un pays et entre 1 et 4 indicateurs'
            })
            
        data = {}
        stats = {}
        
        for indicator_id in indicator_ids:
            indicator_data = EconomicIndicator.objects.filter(
                Country_id=country_id,
                Year__gte=start_year,
                Year__lte=end_year
            ).values('Year', indicator_id)
            
            values = [float(entry[indicator_id]) if entry[indicator_id] is not None else None 
                     for entry in indicator_data]
            years = [entry['Year'] for entry in indicator_data]
            
            if not values:
                continue
            
            data[indicator_id] = {
                'years': years,
                'values': values,
                'name': next((ind['name'] for ind in INDICATORS if ind['id'] == indicator_id), indicator_id),
                'description': next((ind['description'] for ind in INDICATORS if ind['id'] == indicator_id), '')
            }
            
            values = [v for v in values if v is not None]
            stats[indicator_id] = calculate_statistics(values, selected_stats)
        
        return JsonResponse({
            'data': data,
            'stats': stats
        })
        
    except Exception as e:
        return JsonResponse({
            'error': f'Erreur lors de la récupération des données : {str(e)}'
        }, status=400)



### POUR PRESENTER LA DISTRIBUTION D'UN SEUL GRAPHIQUE  ###

def distribute_indicator(request):
    countries = Country.objects.all().values('ID_Country', 'Countryname')
    chart_types = [
        {'id': 'pie', 'name': 'Camembert'},
        {'id': 'bar', 'name': 'Diagramme à barres'}
    ]
    statistics = [
        {'id': 'mean', 'name': 'Moyenne'},
        {'id': 'variance', 'name': 'Variance'},
        {'id': 'percentage', 'name': 'Part en pourcentage'}
    ]
    
    context = {
        'indicators': INDICATORS,
        'countries': list(countries),
        'chart_types': chart_types,
        'statistics': statistics,
        'default_year': 2020
    }
    
    return render(request, 'Visualisation_app/distribute_indicator.html', context)

@require_GET
def get_distribution_data(request):
    try:
        selected_countries = request.GET.getlist('countries[]')
        selected_indicators = request.GET.getlist('indicators[]')
        year = int(request.GET.get('year', 2020))
        selected_stats = request.GET.getlist('statistics[]')
        
        if not selected_countries or not selected_indicators:
            return JsonResponse({
                'error': 'Veuillez sélectionner au moins un pays et un indicateur'
            })
            
        if len(selected_indicators) > 4:
            return JsonResponse({
                'error': 'Vous ne pouvez pas sélectionner plus de 4 indicateurs'
            })
            
        data = {}
        stats = {}
        
        # Récupérer toutes les données en une seule requête
        query_data = EconomicIndicator.objects.filter(
            Country_id__in=selected_countries,
            Year=year
        ).select_related('Country').values(
            'Country__Countryname',
            'Country__ID_Country',
            *selected_indicators
        )
        
        for indicator in selected_indicators:
            values = []
            labels = []
            
            for entry in query_data:
                value = entry.get(indicator)
                if value is not None:
                    values.append(float(value))
                    labels.append(entry['Country__Countryname'])
            
            data[indicator] = {
                'values': values,
                'labels': labels
            }
            
            # Calcul des statistiques
            if values:
                stats[indicator] = {}
                
                if 'mean' in selected_stats:
                    stats[indicator]['mean'] = float(np.mean(values))
                    
                if 'variance' in selected_stats:
                    stats[indicator]['variance'] = float(np.var(values))
                    
                if 'percentage' in selected_stats:
                    total = sum(values)
                    if total > 0:  # Éviter la division par zéro
                        stats[indicator]['percentage'] = [
                            float((value / total) * 100) for value in values
                        ]
                    else:
                        stats[indicator]['percentage'] = [0] * len(values)
            
        # Récupérer les descriptions des indicateurs
        descriptions = {}
        for indicator in selected_indicators:
            indicator_info = next((ind for ind in INDICATORS if ind['id'] == indicator), None)
            descriptions[indicator] = indicator_info['description'] if indicator_info else ''
        
        return JsonResponse({
            'data': data,
            'stats': stats,
            'descriptions': descriptions
        })
        
    except Exception as e:
        return JsonResponse({
            'error': f'Erreur lors de la récupération des données : {str(e)}'
        }, status=400)
    




### POUR PRESENTER LA  CARTOGRAPHIE D'UN MEME INDICATEUR  ###


def cartography_indicator(request):
    countries = Country.objects.all().values('ID_Country', 'Countryname', 'Code').exclude(Countryname="Sao Tome and Principe")
    context = {
        'indicators': INDICATORS,
        'countries': list(countries),
        'default_year': 2020,
    }
    return render(request, 'Visualisation_app/cartography_indicator.html', context)




@require_GET
def get_map_data(request):
    try:
        indicator = request.GET.get('indicator')
        country_ids = request.GET.getlist('countries[]')
        year = int(request.GET.get('year', 2020))
        
        if not indicator or not country_ids:
            return JsonResponse({'error': 'Veuillez sélectionner un indicateur et au moins un pays'})
        
        data = {}
        indicator_info = next((ind for ind in INDICATORS if ind['id'] == indicator), None)
        
        economic_data = EconomicIndicator.objects.filter(
            Country_id__in=country_ids,
            Year=year
        ).select_related('Country').values('Country__Code', 'Country__Countryname', indicator)
        
        for entry in economic_data:
            data[entry['Country__Code']] = {
                'name': entry['Country__Countryname'],
                'value': float(entry[indicator]) if entry[indicator] is not None else None
            }
            
        return JsonResponse({
            'data': data,
            'description': indicator_info['description'] if indicator_info else '',
            'indicator_name': indicator_info['name'] if indicator_info else ''
        })
        
    except Exception as e:
        return JsonResponse({
            'error': f'Erreur lors de la récupération des données : {str(e)}'
        }, status=400)