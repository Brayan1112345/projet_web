from django.shortcuts import render, redirect
from Export_csv_app.forms import export_to_csv_Form
from django.contrib.auth.decorators import login_required
from Form_app.models import Country, EconomicIndicator, Indicator_List, EconomicIndicatorClass
import numpy as np
from math import ceil
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
import csv
import io
import json

# Create your views here.

# =================================================================================================
                            ###     GESTION DE LA BASE DE DONNEES    ###
# =================================================================================================



def index(request):
    
    if request.method == "POST":

        form = export_to_csv_Form(request.POST)

        if form.is_valid():
            indicators = form.cleaned_data['indicateurs']
            countries = form.cleaned_data['pays']
            year_min = form.cleaned_data['annee_min']
            year_max = form.cleaned_data['annee_max']

            if year_min > year_max:
                return render(request, 'Export_csv_app/index0.html', {
                    'message': 'Saisie invalide !!',
                    "form": form,
                })

            # Filtrer les données

            # Gérer le cas où la base de données n'a pas encore été créée
            try:
                filtered_data = EconomicIndicator.objects.filter(
                    Year__gte=year_min,
                    Year__lte=year_max,
                    Country__in=countries,
                )

                n_data = pd.DataFrame(list(filtered_data.values()))
                n_data['Country'] = [element.Country.Countryname for element in filtered_data]

                # Récupérer les noms des indicateurs
                name_indicators = Indicator_List.objects.filter(ID_Indicator__in=indicators)
                list_obj_ind_name = [name_obj.Name_EconomicIndicator for name_obj in name_indicators]

                # Vérifiez que les colonnes existent
                available_columns = ['Country', 'Year'] + list_obj_ind_name
                n_data = n_data[[col for col in available_columns if col in n_data.columns]]

                from decimal import Decimal
                data_records = n_data.to_dict(orient='records')
                for record in data_records:
                    for key, value in record.items():
                        if isinstance(value, Decimal):
                            record[key] = float(value)

                request.session['data'] = data_records

                # Pagination
                page = request.GET.get('page', 1)  # Par défaut, la page 1
                page = int(page)
                lines_per_page = 10  # Nombre de lignes par page
                total_pages = ceil(n_data.shape[0] / lines_per_page)

                # Découper le DataFrame
                start = (page - 1) * lines_per_page
                end = start + lines_per_page
                data_page = n_data.iloc[start:end]

                # Convertir en liste de dictionnaires
                data_page_dict = data_page.to_dict(orient='records')

                pages = list(range(1, total_pages + 1))

                context = {
                    'data_page': data_page_dict,
                    'page': page,
                    'pages': pages,
                    'total_pages': total_pages,
                    "form": form,
                    'show_data': True,
                    'list_obj_ind_name': list_obj_ind_name,
                }
                return render(request, 'Export_csv_app/index0.html', context)
            
            except (not EconomicIndicator.objects.exists()) or (filtered_data.count() == 0):
                return render(request, 'Export_csv_app/index0.html', {
                    'message': 'Aucune donnée trouvée !!',
                    "form": form,
                    'show_data': False,
                })

        return render(request, 'Export_csv_app/index0.html', {
            'message': 'Formulaire mal renseigné !!',
            "form": form,
            'show_data': False,
        })
    
    else:
        page = request.GET.get('page', 1) 
        page = int(page)
        if page > 1:
            lines_per_page = 10
            n_data = pd.DataFrame(list(request.session.get('data')))
            total_pages = ceil(n_data.shape[0] / lines_per_page)
            pages = list(range(1, total_pages + 1))
            list_obj_ind_name = n_data.columns.difference(['Country', 'Year']).tolist()

            start = (page - 1) * lines_per_page
            end = start + lines_per_page
            data_page = n_data.iloc[start:end]
            
            # Convertir en liste de dictionnaires
            data_page_dict = data_page.to_dict(orient='records')
            form = export_to_csv_Form()
            context = {
                    'data_page': data_page_dict,
                    'page': page,
                    'pages': pages,
                    'rows': n_data.shape[0],
                    'total_pages': total_pages,
                    "form": form,
                    'show_data': True,
                    'list_obj_ind_name': list_obj_ind_name,
                }
            return render(request, 'Export_csv_app/index0.html', context)

    form = export_to_csv_Form()
    
    return render(request, 'Export_csv_app/index0.html', {
        "form": form,
        'show_data': False,
    })


import csv
from django.http import HttpResponse
from Users_app.decorators import connectez_vous

@connectez_vous
def export_csv(request):
    # Créer une réponse avec le bon type MIME pour un fichier CSV
    response = HttpResponse(content_type='text/csv', charset='utf-8')
    response['Content-Disposition'] = 'attachment; filename=base_indicateur.csv'
    
    # Récupérer les données de la session
    data = request.session.get('data')  # La session contient une liste de dictionnaires

    # Vérifier si les données existent dans la session
    if data is None:
        return HttpResponse("Aucune donnée à exporter", status=400)
    
    # Créer un writer CSV pour la réponse
    output_csv = 'base.csv'
    with open(output_csv, mode='w', newline='', encoding='utf-8') as response:
        writer = csv.writer(response)
        writer.writerow(data[0].keys())
        for row in data:
            writer.writerow(row.values())
    
    # Si ça ne fonctionne pas, effacer le "with"
    return response
