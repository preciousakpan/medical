from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import MedicalRecord
from .services import MedicalRecordService
from .serializers import MedicalRecordSerializer
from medical.response_handler import ResponseHandler
from users.permissions import IsAdmin



# TODO: make all views and services unifrom with try and except and put error messages within services not views
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdmin])
def create_medical_record_view(request):
    if request.method == GET:
        data = request.data
        user = request.user  

        dob = data.get('dob')
        diagnosis = data.get('diagnosis')
        treatment = data.get('treatment')
        doctor = data.get('doctor')
        treatment_date = data.get('treatment_date')

        created_record = MedicalRecordService.create_medical_record(
            user=user,
            dob=dob,
            diagnosis=diagnosis,
            treatment=treatment,
            doctor=doctor,
            treatment_date=treatment_date
        )

        return ResponseHandler.success(created_record)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_medical_records_for_user_view(request, user_id):
    if request.method == 'GET':
        if request.user.id != int(user_id):
            return ResponseHandler.error("Unauthorized access", status_code=403)
        records = MedicalRecordService.get_medical_records_for_user(user_id)
        
        return ResponseHandler.success(records)


# TODO: Check all status codes
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated, IsAdmin])
def update_medical_record_view(request, record_id):
    if request.method in ['PUT', 'PATCH']:
        data = request.data
        user = request.user  

        diagnosis = data.get('diagnosis')
        treatment = data.get('treatment')
        doctor = data.get('doctor')
        treatment_date = data.get('treatment_date')

        success, message = MedicalRecordService.update_medical_record(
            record_id=record_id,
            diagnosis=diagnosis,
            treatment=treatment,
            doctor=doctor,
            treatment_date=treatment_date
        )
        
        if success:
            return ResponseHandler.success(message)
        else:
            return ResponseHandler.error(message)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdmin])
def delete_medical_record_view(request, record_id):
    if request.method == 'DELETE':
        success, message = MedicalRecordService.delete_medical_record(record_id)
        if success:
            return ResponseHandler.success(message)
        else:
            return ResponseHandler.error(message)
