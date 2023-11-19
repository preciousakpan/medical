from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import MedicalRecord
from .services import MedicalRecordService
from .serializers import MedicalRecordSerializer
from medical.response_handler import ResponseHandler



# TODO: make all views and services unifrom with try and except and put error messages within services not views
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_medical_record_view(request):
    if request.method == 'POST':
        user = request.user
        data = request.data
        
# TODO: Put serializer in service
        serializer = MedicalRecordSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=user)
            return ResponseHandler.success('Medical record created successfully')
        else:
            return ResponseHandler.error(serializer.errors)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_medical_records_for_user_view(request, user_id):
    if request.method == 'GET':
        if request.user.id != int(user_id):
            return ResponseHandler.error("Unauthorized access", status_code=403)
        records = MedicalRecordService.get_medical_records_for_user(user_id)
        
        return ResponseHandler.success(records)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_medical_record_view(request, record_id):
    if request.method in ['PUT', 'PATCH']:
        data = request.data
        
        medical_record = MedicalRecord.objects.get(pk=record_id)
        serializer = MedicalRecordSerializer(medical_record, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return ResponseHandler.success('Medical record updated successfully')
        else:
            return ResponseHandler.error(serializer.errors)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_medical_record_view(request, record_id):
    if request.method == 'DELETE':
        success, message = MedicalRecordService.delete_medical_record(record_id)
        if success:
            return ResponseHandler.success(message)
        else:
            return ResponseHandler.error(message)
