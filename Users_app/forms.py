from django import forms
from django.db import models

class UserForm(forms.Form):
    username = forms.CharField(max_length=150, label="Nom d'utilisateur", required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Entrez votre nom d\'utilisateur...'}))
    email = forms.EmailField(label="Email", max_length=150, required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Entrez votre Email   Ex: xxxx@gmail.com'}))
    password1 = forms.CharField(
        label="Mot de passe",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Insérer votre mot de passe...'}),
    )
    password2 = forms.CharField(
        label="Confirmation du mot de passe",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Confirmer votre mot de passe...'}),
        strip=False,
    )
    first_name = forms.CharField(
        max_length=20,
        label="Prénom",
        widget=forms.TextInput(attrs={'placeholder': 'Entrez votre prénom...'})
    )
    last_name = forms.CharField(
        max_length=20, 
        label="Nom", 
        widget=forms.TextInput(attrs={'placeholder': 'Entrez votre nom...'})
    )
    bio = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5, 'placeholder': "Entrez votre biographie..."}),
        label="Biographie",
        required=False,
    )
    CHOICES = [('is_user', "Utilisateur"), ('is_secretary', "Secrétaire"), ('is_admin', "Administrateur")]
    Role = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=CHOICES,
        required=True,           
        initial='is_user',         
    )
    # Validation supplémentaire pour les mots de passe
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return cleaned_data

class VerificationForm(forms.Form):
    Code = forms.CharField(
        label="Code de confirmation",
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Veuillez entrer le code de confirmation. Ex: 1234'}),
    )
