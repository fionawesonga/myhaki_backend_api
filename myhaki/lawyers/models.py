from django.db import models
from django.db.models import JSONField 

# Create your models here.

class User(models.Model):
    ROLE_CHOICES = [
        ('lawyer', 'Lawyer'),
        ('lsk_admin', 'LSK Admin'),
    ]
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=120, unique=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    image = models.ImageField(upload_to='profiles/', null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user'

class Case(models.Model):
    case_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'case'
    
class Lawyer(models.Model):
    lawyer_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role__in': ['lawyer', 'lsk_admin']})
    practice_number = models.CharField(max_length=50, unique=True)
    specialization = JSONField(default=list)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'lawyer'

class CPDPoint(models.Model):
    cpd_id = models.AutoField(primary_key=True)
    lawyer = models.ForeignKey(Lawyer, on_delete=models.CASCADE)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    points_earned = models.FloatField(default=1.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cpd_point'