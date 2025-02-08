from django.contrib import admin
from Form_app.models import EconomicIndicator 
from Report_app.models import Report

# Register your models here.


class ReportAdmin(admin.ModelAdmin):
    list_display = ('ID_Report', 'Generated_At', 'EconomicIndicator')

admin.site.register(Report, ReportAdmin)