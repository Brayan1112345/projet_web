from django.core.management.base import BaseCommand
import pandas as pd
from Form_app.models import Country, EconomicIndicator, Indicator_List, EconomicIndicatorClass
from django.db import transaction

class Command(BaseCommand):
    help = 'Import economic indicators data'

    def handle(self, *args, **kwargs):
        try:
            # Chargement des fichiers Excel
            df = pd.read_excel('media/Base.xlsx')
            df = df.fillna(value=0) # Django ne reconnaît pas les valeurs NAN. 

            df_ind = pd.read_excel('media/Indicateur.xlsx')

            for group in df_ind['Group'].unique():
                EconomicIndicatorClass.objects.get_or_create(
                        Class_name = group
                    )

            # Création des classes économiques et des indicateurs
            for _, row in df_ind.iterrows():
                class_instance = EconomicIndicatorClass.objects.get(Class_name=row['Group'])

                Indicator_List.objects.get_or_create(
                    Class=class_instance,
                    Name=row['Indicateur'],
                    Description=row['Description'],
                    Name_EconomicIndicator=row['Model_Name']
                )

            # Création des pays
            countries_data = df[['Country_name', 'Country_id', 'Country_code']].iloc[0:11]
            for _, row in countries_data.iterrows():
                Country.objects.get_or_create(
                    ID_Country=row['Country_id'],
                    defaults={
                        'Countryname': row['Country_name'],
                        'Code': row['Country_code']
                    }
                )

            # Création des indicateurs économiques
            df_gdp = df[df['Indicator'] == 'GDP (current US$)']
            for i in range(df_gdp.shape[0]):  # Limiter à 10 ou au nombre réel de lignes
                try:
                    country_instance = Country.objects.get(Countryname=df_gdp['Country_name'].iloc[i])
                except Country.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Country {df_gdp['Country_name'].iloc[i]} not found. Skipping..."))
                    continue

                EconomicIndicator.objects.get_or_create(
                    Year=df_gdp['Year'].iloc[i],
                    Country=country_instance,
                    defaults={
                        'GDP': df_gdp['Value'].iloc[i],
                        'Population': df[df['Indicator'] == 'Population totale']['Value'].iloc[i] if not df[df['Indicator'] == 'Population totale'].empty else None,
                        'Inflation_Rate': df[df['Indicator'] == 'Inflation, GDP PCI (annual %)']['Value'].iloc[i] if not df[df['Indicator'] == 'Inflation, GDP PCI (annual %)'].empty else None,
                        'Population_growth': df[df['Indicator'] == 'Population growth (annual %)']['Value'].iloc[i] if not df[df['Indicator'] == 'Population growth (annual %)'].empty else None,
                        'Balance_com': df[df['Indicator'] == 'Current account balance (% of GDP)']['Value'].iloc[i] if not df[df['Indicator'] == 'Current account balance (% of GDP)'].empty else None,
                        'IDE': df[df['Indicator'] == 'Foreign direct investment, net inflows (% of GDP)']['Value'].iloc[i] if not df[df['Indicator'] == 'Foreign direct investment, net inflows (% of GDP)'].empty else None,
                        'GDP_growth': df[df['Indicator'] == 'GDP growth (annual %)']['Value'].iloc[i] if not df[df['Indicator'] == 'GDP growth (annual %)'].empty else None,
                        'GDP_per_capita': df[df['Indicator'] == 'GDP per capita (current US$)']['Value'].iloc[i] if not df[df['Indicator'] == 'GDP per capita (current US$)'].empty else None,
                        'GNI': df[df['Indicator'] == 'GNI (current US$)']['Value'].iloc[i] if not df[df['Indicator'] == 'GNI (current US$)'].empty else None,
                        'GNI_per_capita': df[df['Indicator'] == 'GNI per capita (current LCU)']['Value'].iloc[i] if not df[df['Indicator'] == 'GNI per capita (current LCU)'].empty else None,
                        'Life_exp': df[df['Indicator'] == 'Life expectancy at birth, total (years)']['Value'].iloc[i] if not df[df['Indicator'] == 'Life expectancy at birth, total (years)'].empty else None,
                        'Maternal_mortality_ratio': df[df['Indicator'] == 'Maternal mortality ratio (modeled estimate, per 100,000 live births)']['Value'].iloc[i] if not df[df['Indicator'] == 'Maternal mortality ratio (modeled estimate, per 100,000 live births)'].empty else None,
                        'Mortality_rate_infant': df[df['Indicator'] == 'Mortality rate, infant (per 1,000 live births)']['Value'].iloc[i] if not df[df['Indicator'] == 'Mortality rate, infant (per 1,000 live births)'].empty else None,
                    }
                )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))
