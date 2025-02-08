from django.urls import path
from Indicateurs_app import views  
from django.views.generic import RedirectView

app_name = 'Indicateurs_app'  

urlpatterns = [
    path('', views.demographic_indicators, name='ind_dem'),
    path('ind_dem/', views.demographic_indicators, name='ind_dem'),
    path('ind_eco/', views.economic_indicators, name='ind_eco'),
    path('ind_soc/', views.social_indicators, name='ind_soc'),
    path('visualisation_ind/<int:indicator_id>/', views.visualization, name='visualisation'),
]

