from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from datetime import date, datetime
from .models import MedicalRecord
from .serializers import MedicalRecordSerializer

class MedicalRecordService:
    @staticmethod
    def create_medical_record(user, dob, diagnosis, treatment, doctor, treatment_date):
        
        treatment_date_obj = datetime.strptime(treatment_date, '%Y-%m-%d').date()
        if treatment_date_obj <= date.today():
            return False, "Treatment date must be a future date"

        hashed_doctor = make_password(doctor)
        hashed_diagnosis = make_password(diagnosis)
        hashed_treatment = make_password(treatment)
        data_to_serialize = {
            'user': user.id,
            'patient_name': user.username,
            'date_of_birth': dob,
            'diagnosis': hashed_diagnosis,
            'treatment': hashed_treatment,
            'doctor': hashed_doctor,
            'treatment_date': treatment_date
        
        }

        serializer = MedicalRecordSerializer(data=data_to_serialize)
        if serializer.is_valid():
            serializer.save(user=user)
            return True, serializer.data
        else:
            return False, serializer.errors

    
    @staticmethod
    def get_medical_records_for_user(user_id):
        user = get_object_or_404(User, id=user_id)
        medical_records = MedicalRecord.objects.filter(user=user)
        serializer = MedicalRecordSerializer(medical_records, many=True)
        return serializer.data
    
    @staticmethod
    def update_medical_record(record_id, diagnosis, treatment, doctor, treatment_date):
        try:
            medical_record = MedicalRecord.objects.get(pk=record_id)
        except MedicalRecord.DoesNotExist:
            return False, "Medical record not found"
        
        
        treatment_date_obj = datetime.strptime(treatment_date, '%Y-%m-%d').date()
        if treatment_date_obj <= date.today():
            return False, "Treatment date must be a future date"

        data_to_update = {
            'diagnosis': diagnosis,
            'treatment': treatment,
            'doctor': doctor,
            'treatment_date': treatment_date
        }

        serializer = MedicalRecordSerializer(instance=medical_record, data=data_to_update, partial=True)

        if serializer.is_valid():
            serializer.save()
            return True, serializer.data
        else:
            return False, serializer.errors
        
    @staticmethod
    def delete_medical_record(record_id):
        try:
            medical_record = MedicalRecord.objects.get(pk=record_id)
            medical_record.delete()
            return True, "Medical record deleted successfully"
        except MedicalRecord.DoesNotExist:
            return False, "Medical record not found"
