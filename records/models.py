from django.db import models
from django.contrib.auth.models import User

class MedicalRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=1000)
    date_of_birth = models.DateField()
    diagnosis = models.TextField()
    treatment = models.TextField()
    doctor = models.CharField(max_length=1000)
    treatment_date = models.DateField()

    def __str__(self):
        return f"{self.patient_name}'s Medical Record"
