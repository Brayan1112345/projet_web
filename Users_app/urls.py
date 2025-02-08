from django.urls import path
from Users_app import views  

app_name = "Users_app"

urlpatterns = [
    path('', views.inscription, name='inscription'),
    path('verification', views.verification, name='verification'),
    path('connexion', views.connexion, name='connexion'),
    path('Accueil', views.accueil, name='accueil'),
    path('deconnexion', views.deconnexion, name='deconnexion'),
]