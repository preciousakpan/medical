from django.urls import path
from . import views

urlpatterns = [
    path('create-medical-record/', views.create_medical_record_view),
    path('get-medical-records/', views.get_medical_records_for_user_view),
    path('update-medical-record/<int:record_id>/', views.update_medical_record_view),
    path('delete-medical-record/<int:record_id>/', views.delete_medical_record_view),
]
