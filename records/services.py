from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import MedicalRecord
from .serializers import MedicalRecordSerializer

class MedicalRecordService:
    @staticmethod
    def create_medical_record(user, name, dob, diagnosis, treatment, doctor, treatment_date):
        medical_record = MedicalRecord.objects.create(
            user=user,
            patient_name=f"{user.username}",
            date_of_birth=dob,
            diagnosis=diagnosis,
            treatment=treatment,
            doctor=doctor,
            treatment_date=treatment_date
        )
        return medical_record

    @staticmethod
    def get_medical_records_for_user(user_id):
        user = get_object_or_404(User, id=user_id)
        medical_records = MedicalRecord.objects.filter(user=user)
        serializer = MedicalRecordSerializer(medical_records, many=True)
        return serializer.data
    

# TODO: you should not be able to update the userId and name, name should be gotten from the user model
    @staticmethod
    def update_medical_record(record_id, **kwargs):
        try:
            medical_record = MedicalRecord.objects.get(pk=record_id)
            for key, value in kwargs.items():
                setattr(medical_record, key, value)
            medical_record.save()
            return True, "Medical record updated successfully"
        except MedicalRecord.DoesNotExist:
            return False, "Medical record not found"

    @staticmethod
    def delete_medical_record(record_id):
        try:
            medical_record = MedicalRecord.objects.get(pk=record_id)
            medical_record.delete()
            return True, "Medical record deleted successfully"
        except MedicalRecord.DoesNotExist:
            return False, "Medical record not found"
