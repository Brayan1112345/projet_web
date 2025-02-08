from django.shortcuts import render, redirect
from Users_app.forms import UserForm, VerificationForm
from Users_app.models import User, Profile
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse, FileResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User as DefaultUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group


# =================================================================================================
                                ###     GESTION DES UTILISATEURS     ###
# =================================================================================================


def inscription(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            # Récupérer les données du formulaire
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            raw_password = form.cleaned_data['password2']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            bio = form.cleaned_data['bio']
            role = form.cleaned_data['Role']
            # Déterminer le rôle
            if role == 'is_admin':
                role = 'a'
            elif role == 'is_secretary':
                role = 's'
            else:
                role = 'u'

            # Vérifier si le nom d'utilisateur existe déjà
            if DefaultUser.objects.filter(username=username).exists():
                form.add_error('username', 'Ce nom d’utilisateur est déjà utilisé.')
                return render(request, 'Users_app/inscription.html', {'form': form})  
            elif DefaultUser.objects.filter(email=email).exists():
                form.add_error('email', 'Cette adresse email est déjà utilisée.')
                return render(request, 'Users_app/inscription.html', {'form': form})

            if ((role == 'a')|(role == 's')) :
                # Enregistrer les données du formulaire dans la session
                request.session['username'] = username
                request.session['email'] = email
                request.session['raw_password'] = raw_password
                request.session['first_name'] = first_name
                request.session['last_name'] = last_name
                request.session['bio'] = bio
                request.session['role'] = role
                # Rediriger 
                return redirect('Users_app:verification')
            else:
                # Enregistrer l'utilisateur avec la fonction dédiée
                enregistrer_utilisateur(
                    username=username,
                    email=email,
                    raw_password=raw_password,
                    first_name=first_name,
                    last_name=last_name,
                    bio=bio,
                    role=role
                )

            # Rediriger après succès
            return redirect('Users_app:connexion')  # Changez 'success' par l'URL de votre choix
    else:
        try:
            form = UserForm()
        except Exception as e:
            for field, errors in form.errors.items():
                form.add_error(field, errors[0])

    # Afficher le formulaire en cas de requête GET ou erreur
    return render(request, 'Users_app/inscription.html', {'form': form})


def verification(request):
    CODE_ADMIN = '1234'
    CODE_STAFF = '5678'

    # Récupérer les données de la session
    username = request.session.get('username')
    email = request.session.get('email')
    raw_password = request.session.get('raw_password')
    first_name = request.session.get('first_name')
    last_name = request.session.get('last_name')
    bio = request.session.get('bio')
    role = request.session.get('role')

    if request.method == "POST":
        form = VerificationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['Code']
            if (((role == 'a') & (code == CODE_ADMIN)) | ((role == 's') & (code == CODE_STAFF))):
                enregistrer_utilisateur(
                    username=username,
                    email=email,
                    raw_password=raw_password,
                    first_name=first_name,
                    last_name=last_name,
                    bio=bio,
                    role=role
                )
                return redirect('Users_app:connexion')
            else:
                form.add_error('Code', 'Code incorrect. Veuillez réessayer !')
    else:
        form = VerificationForm()

    return render(request, 'Users_app/verification.html', {'form': form})



def enregistrer_utilisateur(username, email, raw_password, first_name, last_name, bio, role):

    # Définir les statuts admin ou staff en fonction du rôle
    is_superuser = role == 'a'
    is_staff = role in ['a', 's']

    # Créer un utilisateur par défaut de Django
    django_user = DefaultUser.objects.create(
        username=username,
        email=email,
        password=make_password(raw_password), 
        first_name=first_name,
        last_name=last_name,
        is_superuser=is_superuser,  
        is_staff=is_staff,          
    )

    # Créer l'utilisateur personnalisé
    custom_user = User.objects.create(
        ID_USER='',  # Sera généré automatiquement dans save()
        Username=username,
        Email=email,
        Password=django_user.password,  # Haché par Django
        Role=role,
    )

    # Créer le profil lié à cet utilisateur
    profile = Profile.objects.create(
        User=custom_user,
        ID_Profile='',  # Sera généré automatiquement dans save()
        First_Name=first_name,
        Last_Name=last_name,
        Bio=bio,
    )

    return django_user


def connexion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('Users_app:accueil')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    return render(request, 'Users_app/connexion.html')


def accueil(request):
    return render(request, 'pages/home.html')


@login_required
def deconnexion(request):
    logout(request)
    return redirect('Users_app:connexion')

