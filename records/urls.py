from django.urls import path
from . import views

urlpatterns = [
    path('create-medical-record/', views.create_medical_record_view, name='create_medical_record'),
    path('get-medical-records/', views.get_medical_records_for_user_view, name='get_medical_records'),
    path('update-medical-record/<int:record_id>/', views.update_medical_record_view, name='update_medical_record'),
    path('delete-medical-record/<int:record_id>/', views.delete_medical_record_view, name='delete_medical_record'),
]
