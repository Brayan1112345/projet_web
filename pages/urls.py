from django.urls import path
from .views import AboutView, ContactView
from . import views

app_name = 'pages'  

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
]


