from rest_framework import serializers
from .models import Patient

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = (
            'first_name', 'last_name', 'image', 
            'cnic', 'gender', 'contact', 'address', 
            'email', 'marital_status', 'surgery_date',
            'recovery_date', 'date_of_birth', 'surgery',
            'surgery_details'
        )
