from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import MedicalRecord
from .serializers import MedicalRecordSerializer

class MedicalRecordService:
    @staticmethod
    def create_medical_record(user, dob, diagnosis, treatment, doctor, treatment_date):
        data_to_serialize = {
            'user': user.id,
            'patient_name': user.username,
            'date_of_birth': dob,
            'diagnosis': diagnosis,
            'treatment': treatment,
            'doctor': doctor,
            'treatment_date': treatment_date
        
        }

        serializer = MedicalRecordSerializer(data=data_to_serialize)
        if serializer.is_valid():
            serializer.save(user=user)
            return serializer.data
        else:
            return serializer.errors

    
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
