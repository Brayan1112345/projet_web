from django.shortcuts import render, redirect
from django.contrib import messages
from Form_app.forms import CountryYearForm, IndicatorValuesForm, ConfirmationForm
from Form_app.models import Country, EconomicIndicator, EconomicIndicatorClass , Indicator_List


# Create your views here.

# =================================================================================================
                ###     FORMULAIRE D'AJOUT D'UN INDICATEUR DANS LA BASE     ###
# =================================================================================================


def Save_Indicator1(request):

    form1 = CountryYearForm()

    if request.method == 'POST':
        form1 = CountryYearForm(request.POST)

        if form1.is_valid():
            country = form1.cleaned_data['country']
            year = form1.cleaned_data['year']

            country1 = Country.objects.get(Countryname=country)


            # Vérifiez si l'indicateur existe déjà
            if EconomicIndicator.objects.filter(Country=country1, Year=year).exists():
                messages.error(request, 'Les informations pour ce pays et cette année existent déjà')
                return render(request, 'Form_app/Enrégistrement.html', {
                    'form1': form1,
                    'show_step2': False
                })

            country_data = {
                'ID_Country': country1.ID_Country,
                'Countryname': country1.Countryname,
                'Code': country1.Code
            }

            request.session['country'] = country_data
            request.session['year'] = year

            # Prépare form2 pour affichage
            form2 = IndicatorValuesForm()

            return render(request, 'Form_app/Enrégistrement.html', {
                'form1': form1,
                'form2': form2,
                'show_step2': True
            })
        else:
            messages.error(request, 'Erreur dans les données soumises.')
            return render(request, 'Form_app/Enrégistrement.html', {
                'form1': form1,
                'show_step2': False
            })

    messages.info(request, 'Veuillez entrer le nom du pays et l\'année.')
    return render(request, 'Form_app/Enrégistrement.html', {
        'form1': form1,
        'show_step2': False
    })


def Save_Indicator2(request):
    country_data = request.session.get('country')
    year = request.session.get('year')

    if not country_data or not year:
        messages.error(request, 'Les données de session sont manquantes. Veuillez recommencer.')
        return render(request, 'Form_app/Enrégistrement.html', {
            'show_step2': False
        })

    form2 = IndicatorValuesForm(request.POST)

    if form2.is_valid():
        country = Country.objects.get(ID_Country=country_data['ID_Country'])

        economic_indicator = EconomicIndicator(
            Country=country,
            Year=year,
            GDP=form2.cleaned_data['GDP'],
            Inflation_Rate=form2.cleaned_data['Inflation_Rate'],
            Population=form2.cleaned_data.get('Population'), 
            Population_growth=form2.cleaned_data.get('Population_growth'),
            Balance_com=form2.cleaned_data.get('Balance_com'),
            IDE=form2.cleaned_data.get('IDE'),
            GDP_growth=form2.cleaned_data.get('GDP_growth'),
            GDP_per_capita=form2.cleaned_data.get('GDP_per_capita'),
            GNI=form2.cleaned_data.get('GNI'),
            GNI_per_capita=form2.cleaned_data.get('GNI_per_capita'),
            Life_exp=form2.cleaned_data.get('Life_exp'),
            Maternal_mortality_ratio=form2.cleaned_data.get('Maternal_mortality_ratio'),
            Mortality_rate_infant=form2.cleaned_data.get('Mortality_rate_infant')
        )

        economic_indicator.save()

        messages.success(request, f"Données enrégistrées avec succès pour le pays {country.Countryname}, à l'année {year}")
        return render(request, 'Form_app/Enrégistrement.html', {
            'show_step2': False,
            'form1': CountryYearForm()
        })
    else:
        messages.error(request, 'Erreur dans les données du formulaire 2.')
        return render(request, 'Form_app/Enrégistrement.html', {
            'form2': form2,
            'show_step2': True
        })
      

# =================================================================================================
                ###     FORMULAIRE DE MODIFICATION D'INDICATEURS DANS LA BASE     ###
# =================================================================================================



def Modify_Indicator1(request):
    form1 = CountryYearForm()

    if request.method == 'POST':
        form1 = CountryYearForm(request.POST)

        if form1.is_valid():
            country = form1.cleaned_data['country']
            year = form1.cleaned_data['year']

            country1 = Country.objects.get(Countryname=country)


            country_data = {
                'ID_Country': country1.ID_Country,
                'Countryname': country1.Countryname,
                'Code': country1.Code
            }

            request.session['country'] = country_data
            request.session['year'] = year

            # Prépare form2 pour affichage
            try:
                # Récupérer l'indicateur existant
                indicateur = EconomicIndicator.objects.get(
                    Country__ID_Country=country_data['ID_Country'],
                    Year=year
                )
            except EconomicIndicator.DoesNotExist:
                messages.error(request, 'Les indicateurs économiques pour ce pays et cette année sont introuvables.')
                return render(request, 'Form_app/Modification.html', {
                    'show_step2': False,
                    'form1': CountryYearForm()
                })
                
            request.session['form2_data'] = {
                'GDP': float(indicateur.GDP),
                'Inflation_Rate': float(indicateur.Inflation_Rate),
                'Population': float(indicateur.Population),
                'Population_growth': float(indicateur.Population_growth),
                'Balance_com': float(indicateur.Balance_com),
                'IDE': float(indicateur.IDE),
                'GDP_growth': float(indicateur.GDP_growth),
                'GDP_per_capita': float(indicateur.GDP_per_capita),
                'GNI': float(indicateur.GNI),
                'GNI_per_capita': float(indicateur.GNI_per_capita),
                'Life_exp': float(indicateur.Life_exp),
                'Maternal_mortality_ratio': float(indicateur.Maternal_mortality_ratio),
                'Mortality_rate_infant': float(indicateur.Mortality_rate_infant)
            }

            form2 = IndicatorValuesForm(initial=request.session['form2_data'])

            return render(request, 'Form_app/Modification.html', {
                'form1': form1,
                'form2': form2,
                'show_step2': True
            })
        else:
            messages.error(request, 'Erreur dans les données soumises.')
            return render(request, 'Form_app/Modification.html', {
                'form1': form1,
                'show_step2': False
            })
    
    messages.info(request, 'Veuillez entrer le nom du pays et l\'année.')
    return render(request, 'Form_app/Modification.html', {
        'form1': form1,
        'show_step2': False,
    })


def Modify_Indicator2(request): #update
    country_data = request.session.get('country')
    year = request.session.get('year')

    if not country_data or not year:
        messages.error(request, 'Les données de session sont manquantes. Veuillez recommencer.')
        return render(request, 'Form_app/Modification.html', {
            'show_step2': False,
            'form1':CountryYearForm()
        })

    try:
        # Récupérer l'indicateur existant
        indicateur = EconomicIndicator.objects.get(
            Country__ID_Country=country_data['ID_Country'],
            Year=year
        )
    except EconomicIndicator.DoesNotExist:
        messages.error(request, 'Les indicateurs économiques pour ce pays et cette année sont introuvables.')
        return render(request, 'Form_app/Modification.html', {
            'form1':CountryYearForm(),
            'show_step2': False,
        })
    
    if request.method == 'POST':
        form2 = IndicatorValuesForm(request.POST)

        if form2.is_valid():
            country = Country.objects.get(ID_Country=country_data['ID_Country'])

            gdp = form2.cleaned_data['GDP']
            inflation_rate = form2.cleaned_data['Inflation_Rate']
            population = form2.cleaned_data['Population']
            population_growth = form2.cleaned_data['Population_growth']
            Balance_com = form2.cleaned_data['Balance_com']
            IDE = form2.cleaned_data['IDE']
            GDP_growth = form2.cleaned_data['GDP_growth']
            GDP_per_capita = form2.cleaned_data['GDP_per_capita']
            GNI = form2.cleaned_data['GNI']
            GNI_per_capita = form2.cleaned_data['GNI_per_capita']
            Life_exp = form2.cleaned_data['Life_exp']
            Maternal_mortality_ratio = form2.cleaned_data['Maternal_mortality_ratio']
            Mortality_rate_infant = form2.cleaned_data['Mortality_rate_infant']
            
            economic_indicator = EconomicIndicator(
                Country=country,
                Year=year,
                Inflation_Rate=inflation_rate,
                Population=population,
                Population_growth=population_growth,
                Balance_com=Balance_com,
                IDE=IDE,
                GDP=gdp,
                GDP_growth=GDP_growth,
                GDP_per_capita=GDP_per_capita,
                GNI=GNI,
                GNI_per_capita=GNI_per_capita,
                Life_exp=Life_exp,
                Maternal_mortality_ratio=Maternal_mortality_ratio,
                Mortality_rate_infant=Mortality_rate_infant
            )

            economic_indicator.save()


        messages.success(request, f"Données modifiées avec succès pour le pays {country.Countryname}, à l'année {year}")
        return render(request, 'Form_app/Modification.html', {
            'show_step2': False,
            'form1': CountryYearForm()
        })
    else:
        # Charger les données du formulaire 2 depuis la session
        form2_data = request.session.get('form2_data', {})
        form2 = IndicatorValuesForm(initial=form2_data)

        messages.error(request, 'Erreur dans les données du formulaire 2.')
        return render(request, 'Form_app/Modification.html', {
            'form2': form2,
            'show_step2': True
        })



# =================================================================================================
                ###     FORMULAIRE DE SUPPRESSION D'INDICATEURS DANS LA BASE     ###
# =================================================================================================

def delete_indicator(request):

    confirm_delete = False
    form = CountryYearForm()

    if request.method == 'POST':
        # Si le formulaire de sélection est soumis
        if form.is_valid():
            country = form.cleaned_data['country']
            year = form.cleaned_data['year'] 
            try:
                country1 = Country.objects.get(Countryname=country)
            except Country.DoesNotExist:
                messages.error(request, 'Pays non trouvé.')
                return render(request, 'Form_app/Suppréssion.html', {
                    'form': form,
                    'confirm_delete': False
                })

            country_data = {
                'ID_Country': country1.ID_Country,
                'Countryname': country1.Countryname,
                'Code': country1.Code
            }

            request.session['country'] = country_data
            request.session['year'] = year

            # Chercher l'instance à supprimer
            try:
                indicator = EconomicIndicator.objects.get(ID_Indicator = f'{country1.Code}, {year}')

                return render(request, 'Form_app/Suppréssion.html', {
                    'confirm_delete': True,
                })
            except EconomicIndicator.DoesNotExist:
                messages.error(request, 'Aucun indicateur trouvé pour ce pays et cette année.')
                return render(request, 'Form_app/Suppréssion.html', {
                    'form':form,
                    'confirm_delete':False
                })
                return redirect('delete_indicator')
            
            
        
        # Si le formulaire de confirmation est soumis
        if 'confirm_delete1' in request.POST:
            # Supprimer l'indicateur
            country = request.session.get('country')

            year = request.session.get('year')
            EconomicIndicator.objects.get(ID_Indicator = f'{country['Code']}, {year}').delete()

            messages.success(request, f"Les indicateurs pour {country['Countryname']} en {year} ont été supprimés avec succès.")
            return render(request, 'Form_app/Suppréssion.html', {
                'form': CountryYearForm(),
                'confirm_delete': False
            })
        
        # Si l'utilisateur annule
        if 'cancel_delete' in request.POST:
            messages.info(request, 'La suppression a été annulée.')
            return render(request, 'Form_app/Suppréssion.html', {
                'form': form,
                'confirm_delete': False
            })
    
    messages.info(request, 'Veuillez entrer le nom du pays et l\'année.')
    return render(request, 'Form_app/Suppréssion.html', {
        'form': form,
        'confirm_delete': False,
    })



def delete_indicator1(request):

    form1 = CountryYearForm()

    if request.method == 'POST':
        form1 = CountryYearForm(request.POST)

        if form1.is_valid():
            country = form1.cleaned_data['country']
            year = form1.cleaned_data['year']

            country1 = Country.objects.get(Countryname=country)


            # Vérifiez si les données de cet instance existe
            if not EconomicIndicator.objects.filter(Country=country1, Year=year).exists():
                messages.error(request, "Les informations pour ce pays et cette année n'existent pas.")
                return render(request, 'Form_app/Suppréssion.html', {
                    'form1': form1,
                    'show_step2': False
                })

            country_data = {
                'ID_Country': country1.ID_Country,
                'Countryname': country1.Countryname,
                'Code': country1.Code
            }

            request.session['country'] = country_data
            request.session['year'] = year

            # Prépare form2 pour affichage
            form2 = ConfirmationForm()

            return render(request, 'Form_app/Suppréssion.html', {
                'form1': form1,
                'form2': form2,
                'show_step2': True
            })
        else:
            messages.error(request, 'Erreur dans les données soumises.')
            return render(request, 'Form_app/Suppréssion.html', {
                'form1': form1,
                'show_step2': False
            })

    messages.info(request, 'Veuillez entrer le nom du pays et l\'année.')
    return render(request, 'Form_app/Suppréssion.html', {
        'form1': form1,
        'show_step2': False
    })


def delete_indicator2(request):
    country_data = request.session.get('country')
    year = request.session.get('year')

    if not country_data or not year:
        messages.error(request, 'Les données de session sont manquantes. Veuillez recommencer.')
        return render(request, 'Form_app/Suppréssion.html', {
            'show_step2': False
        })

    form2 = ConfirmationForm(request.POST)

    if form2.is_valid():
        # Si l'utilsateur confirme
        if 'confirm_delete' in request.POST:
            # Supprimer l'indicateur
            country = Country.objects.get(ID_Country=country_data['ID_Country'])
           
            EconomicIndicator.objects.filter(Country=country, Year=year).delete()

            messages.success(request, f"Les indicateurs pour {country_data['Countryname']} en {year} ont été supprimés avec succès.")
            return render(request, 'Form_app/Suppréssion.html', {
                'form1': CountryYearForm(),
                'show_step2': False
            })
        
        # Si l'utilisateur annule
        if 'cancel_delete' in request.POST:
            messages.info(request, 'La suppression a été annulée.')
            return render(request, 'Form_app/Suppréssion.html', {
                'form1': CountryYearForm(),
                'show_step2': False
            })
    else:
        messages.error(request, 'Une erreur s\' est produite.')
        return render(request, 'Form_app/Suppréssion.html', {
            'form2': form2,
            'show_step2': True
        })
 