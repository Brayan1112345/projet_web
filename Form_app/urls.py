from django.urls import path
from Form_app import views  
from django.views.generic import RedirectView
app_name = "Form_app"

urlpatterns = [
    path('Save_Indicator1/', views.Save_Indicator1, name='Save_Indicator1'),
    path('Save_Indicator2/', views.Save_Indicator2, name='Save_Indicator2'),
    path('Modify_Indicator1/', views.Modify_Indicator1, name='Modify_Indicator1'),
    path('Modify_Indicator2/', views.Modify_Indicator2, name='Modify_Indicator2'),
    path('delete_indicator1/', views.delete_indicator1, name='delete_indicator1'),
    path('delete_indicator2/', views.delete_indicator2, name='delete_indicator2'),
    path('', RedirectView.as_view(url='/Form/Save_Indicator1/', permanent = False)),
]