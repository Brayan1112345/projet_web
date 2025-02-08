from functools import wraps
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
import Users_app.views

def connectez_vous(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Vérifier si l'utilisateur est authentifié
        if not request.user.is_authenticated:
            # Rediriger vers la page de connexion
            return redirect('Users_app:connexion')
        # Si authentifié, exécuter la vue
        return view_func(request, *args, **kwargs)
    return _wrapped_view
