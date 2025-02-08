from django.contrib import admin
from Form_app.models import Country, EconomicIndicator, Indicator_List, EconomicIndicatorClass

# Register your models here.

# Enregistrer le modèle Country
class CountryAdmin(admin.ModelAdmin):
    list_display = ('ID_Country', 'Countryname', 'Code')  # Colonnes affichées dans la liste
    search_fields = ('Countryname',)

admin.site.register(Country, CountryAdmin)

# Enregistrer le modèle EconomicIndicator
class EconomicIndicatorAdmin(admin.ModelAdmin):
    list_display = ('Country','ID_Indicator', 'GDP', 'Inflation_Rate', 'Population', 'Life_exp')
    list_filter = ('Country', 'Year', )
    search_fields = ('Country', 'Year',)
    list_per_page = 15

admin.site.register(EconomicIndicator, EconomicIndicatorAdmin)

class IndicatorInline(admin.TabularInline):  # Ou StackedInline selon vos préférences
    model = Indicator_List
    extra = 0  # Nombre de formulaires vides à afficher

#Enrégistrer le modèle de liste d'indicateurs
class Indicator_ListAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Description', 'Class',)
    search_fields = ('Name',)
    list_filter = ('Class',)

admin.site.register(Indicator_List, Indicator_ListAdmin)

#Enrégistrer le modèle de classes d'indicateurs
class EconomicIndicatorClassAdmin(admin.ModelAdmin):
    list_display = ('Class_name', )
    inlines = [IndicatorInline]
    search_fields = ('Class_name',)

admin.site.register(EconomicIndicatorClass, EconomicIndicatorClassAdmin)