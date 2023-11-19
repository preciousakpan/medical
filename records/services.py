from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from datetime import date, datetime
from .models import MedicalRecord
from .serializers import MedicalRecordSerializer
from cryptography.fernet import Fernet
import base64

key = b'uY4PvQu-uFT-1K000FwJ5jK_Ds21rokzIvlI6f5AImM='
cipher_suite = Fernet(key)

def encrypt_field(field):
    encrypted_field = cipher_suite.encrypt(field.encode())
    return base64.b64encode(encrypted_field).decode()

def decrypt_field(encrypted_field):
    encrypted_field = base64.b64decode(encrypted_field)
    decrypted_field = cipher_suite.decrypt(encrypted_field).decode()
    return decrypted_field


class MedicalRecordService:
    @staticmethod
    def create_medical_record(user_id, dob, diagnosis, treatment, doctor, treatment_date):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return False, f"User does not exist with ID: {user_id}"
        
        treatment_date_obj = datetime.strptime(treatment_date, '%Y-%m-%d').date()
        if treatment_date_obj <= date.today():
            return False, "Treatment date must be a future date"

        data_to_serialize = {
            'user': user.id,
            'patient_name': user.username,
            'date_of_birth': dob,
            'diagnosis': diagnosis,
            'treatment': treatment,
            'doctor': doctor,
            'treatment_date': treatment_date
        
        }

        encrypted_patient_name = encrypt_field(data_to_serialize['patient_name'])
        encrypted_doctor_name = encrypt_field(data_to_serialize['doctor'])

        data_to_serialize['patient_name'] = encrypted_patient_name
        data_to_serialize['doctor'] = encrypted_doctor_name

        serializer = MedicalRecordSerializer(data=data_to_serialize)
        if serializer.is_valid():
            medical_record = MedicalRecord.objects.create(
                user=user,
                patient_name=encrypted_patient_name,
                date_of_birth=dob,
                diagnosis=diagnosis,
                treatment=treatment,
                doctor=encrypted_doctor_name,
                treatment_date=treatment_date
            )
            serialized_record = MedicalRecordSerializer(medical_record).data
            return True, serialized_record
        else:
            return False, serializer.errors
    
    @staticmethod
    def get_medical_records_for_user(user_id):
        user = get_object_or_404(User, id=user_id)
        medical_records = MedicalRecord.objects.filter(user=user)
        serializer = MedicalRecordSerializer(medical_records, many=True)
        serialized_data = serializer.data

        decrypted_records = []
        for record in serialized_data:
            try:
                decrypted_patient_name = decrypt_field(record['patient_name'])
                decrypted_doctor_name = decrypt_field(record['doctor'])

                record['patient_name'] = decrypted_patient_name
                record['doctor'] = decrypted_doctor_name

                decrypted_records.append(record)
            except Exception as e:
                return(f"Error decoding record: {record}. Error: {e}")

        return decrypted_records
    
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

        encrypted_doctor_name = encrypt_field(data_to_update['doctor'])

        data_to_update['doctor'] = encrypted_doctor_name

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
