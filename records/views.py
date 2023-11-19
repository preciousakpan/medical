from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import MedicalRecord
from .services import MedicalRecordService
from .serializers import MedicalRecordSerializer
from medical.response_handler import ResponseHandler
from users.permissions import IsAdmin
from django.http import JsonResponse

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdmin])
def create_medical_record_view(request):
    if request.method == 'POST':
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

        return JsonResponse(ResponseHandler.success(created_record), status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_medical_records_for_user_view(request, user_id):
    if request.method == 'GET':
        if request.user.id != int(user_id):
            return JsonResponse(ResponseHandler.error("Unauthorized access"), status=403)
        records = MedicalRecordService.get_medical_records_for_user(user_id)
        
        return JsonResponse(ResponseHandler.success(records), status=200)

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
            return JsonResponse(ResponseHandler.success(message), status=200)
        else:
            return JsonResponse(ResponseHandler.error(message), status=400)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdmin])
def delete_medical_record_view(request, record_id):
    if request.method == 'DELETE':
        success, message = MedicalRecordService.delete_medical_record(record_id)
        if success:
            return JsonResponse(ResponseHandler.success(message), status=200)
        else:
            return JsonResponse(ResponseHandler.error(message), status=400)
