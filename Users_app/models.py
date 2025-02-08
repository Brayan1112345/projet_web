from django.db import models
from django.urls import reverse
import uuid

# Create your models here.

class User(models.Model):
    ID_USER = models.CharField(primary_key=True, max_length=24, editable=False)
    Username = models.CharField(max_length=200, help_text='Entrez votre nom d\'utilisateur...')
    Email = models.EmailField(max_length=50, help_text='Entrez votre Email   Ex: xxxx@gmail.com')
    Password = models.CharField(max_length=128, verbose_name="Mot de passe")
    ROLE_PARAMS = (
        ('a', 'Administrateur'),
        ('s', 'Secrétaire'),
        ('u', 'Utilisateur'),)
    Role = models.CharField(max_length=1, choices=ROLE_PARAMS, blank=True, default='u')

    def __str__(self):
        return f'{self.Username} ({self.ID_USER})'
        
    def get_absolute_url(self) :
        return reverse("user-details", args=[str(self.id)])

    def save(self, *args, **kwargs):
        if self.Role == 'a':
            prefix = 'ADMIN'
        elif self.Role == 's':
            prefix = 'SECR'
        else: 
            prefix = 'USER'
        count = User.objects.filter(Role=self.Role).count() + 1
        self.ID_USER = f'{prefix}{count:05d}'
        super().save(*args, **kwargs)


class Profile(models.Model):
    User = models.OneToOneField('User', on_delete=models.CASCADE)

    ID_Profile = models.CharField(primary_key=True, max_length=24, editable=False)
    First_Name = models.CharField(max_length=20, help_text='Entrez votre prénom...')
    Last_Name = models.CharField(max_length=20, help_text='Entrez votre nom...')
    Bio = models.TextField(max_length=1000, help_text='Entrez votre biographie')
    Date_Joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['Last_Name', 'First_Name']

    @classmethod
    def get_by_username(cls, username):
        return cls.objects.get(User__Username=username)

    def __str__(self):
        return f'{self.Last_Name} {self.First_Name}'  

    def save(self, *args, **kwargs):
        self.ID_Profile=f'{self.First_Name}{self.User.ID_USER}'

        super().save(*args, **kwargs)