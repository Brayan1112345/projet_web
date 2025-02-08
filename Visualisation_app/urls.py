from django.urls import path
from Visualisation_app import views 
from django.views.generic import RedirectView 

app_name = "Visualisation_app"

urlpatterns = [
    path('', RedirectView.as_view(url='/Visualisation/compare-countries/', permanent = False)),
    path('compare-countries/', views.compare_countries, name='compare_countries'),
    path('compare-indicators/', views.compare_indicators, name='compare_indicators'),
    path('distribute-indicator/', views.distribute_indicator, name='distribute_indicator'),
    path('cartography/', views.cartography_indicator, name='cartography_indicator'),
    path('get-country-data/', views.get_country_data, name='get_country_data'),
    path('get-indicator-data/', views.get_indicator_data, name='get_indicator_data'),
    path('get-distribution-data/', views.get_distribution_data, name='get_distribution_data'),
    path('get-map-data/', views.get_map_data, name='get_map_data'),
]


