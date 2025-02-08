from django.contrib import admin
from Users_app.models import User, Profile

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('ID_USER', 'Username', 'Email', 'Role')  # Colonnes affichées dans la liste
    search_fields = ('Username', 'Email')  # Permet la recherche dans l'admin

admin.site.register(User, UserAdmin)

# Enregistrer le modèle Profile
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('First_Name', 'Last_Name', 'Bio', 'Date_Joined')  # Colonnes affichées dans la liste
    search_fields = ('First_Name', 'Last_Name')

admin.site.register(Profile, ProfileAdmin)