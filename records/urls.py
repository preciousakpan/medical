from django.urls import path
from . import views

urlpatterns = [
    path('create-record/', views.create_medical_record_view),
    path('get-records/<int:user_id>/', views.get_medical_records_for_user_view),
    path('update-record/<int:record_id>/', views.update_medical_record_view),
    path('delete-record/<int:record_id>/', views.delete_medical_record_view),
]
