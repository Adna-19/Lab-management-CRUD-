from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
	list_display = ('first_name', 'last_name', 'marital_status', 'slug','cnic', 'image','gender', 'address', 'contact','email', 'date_of_birth', 'surgery_date', 'recovery_date','surgery')
	search_fields = ('gender', 'first_name', 'cnic')
	list_filter = ('gender','surgery')