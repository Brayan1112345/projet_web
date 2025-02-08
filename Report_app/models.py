from django.db import models
import uuid
from django.core.files.storage import FileSystemStorage

# Create your models here.


class Report(models.Model):
    ID_Report = models.UUIDField(primary_key=True)
    Generated_At = models.DateTimeField(auto_now_add=True)
    Report_File = models.FileField(upload_to='lien', storage=FileSystemStorage(location='lien'))

    EconomicIndicator = models.ForeignKey('Form_app.EconomicIndicator', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.EconomicIndicator.Countryname}, {self.Generated_At}'
