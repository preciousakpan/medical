from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from .models import MedicalRecord
from .services import MedicalRecordService
from .serializers import MedicalRecordSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_medical_record_view(request):
    if request.method == 'POST':
        user = request.user
        data = request.data
        
        serializer = MedicalRecordSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=user)
            return JsonResponse({'status': 'success', 'message': 'Medical record created successfully'})
        else:
            return JsonResponse({'status': 'error', 'message': serializer.errors})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_medical_records_for_user_view(request):
    if request.method == 'GET':
        user = request.user
        
        medical_records = MedicalRecord.objects.filter(user=user)
        serializer = MedicalRecordSerializer(medical_records, many=True)
        
        return JsonResponse(serializer.data, safe=False)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_medical_record_view(request, record_id):
    if request.method in ['PUT', 'PATCH']:
        data = request.data
        
        medical_record = MedicalRecord.objects.get(pk=record_id)
        serializer = MedicalRecordSerializer(medical_record, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'status': 'success', 'message': 'Medical record updated successfully'})
        else:
            return JsonResponse({'status': 'error', 'message': serializer.errors})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_medical_record_view(request, record_id):
    if request.method == 'DELETE':
        success, message = MedicalRecordService.delete_medical_record(record_id)
        if success:
            return JsonResponse({'status': 'success', 'message': message})
        else:
            return JsonResponse({'status': 'error', 'message': message})
