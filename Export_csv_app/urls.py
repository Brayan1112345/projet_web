from django.urls import path
from . import views  

app_name = "Export_csv_app"

urlpatterns = [
    path('export_csv', views.export_csv, name='export_csv'),
    path('index', views.index, name='index'),

]