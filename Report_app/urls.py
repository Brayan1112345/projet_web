from django.urls import path
from Report_app import views  

app_name = "Report_app"

urlpatterns = [
    path('generate_PDF', views.generate_PDF, name='generate_PDF'),
    path('download_PDF', views.download_PDF, name='download_PDF'),

]