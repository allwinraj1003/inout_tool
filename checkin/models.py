from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser,BaseUserManager, PermissionsMixin
from django.conf import settings

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, role=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        if not role:
            raise ValueError("Users must have a role")

        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, role='SuperAdmin', **extra_fields)

      
class CustomUser(AbstractUser):
    
    ROLE_CHOICES = [
         (' ', '  '),
        ('Fullstack_developer', 'Fullstack_developer'),
        ('manager', 'Manager'),
        ('admin','Admin'),
        ('Associate','Associate'),
        ('intern', 'intern'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='SBS_RESOURCE')
    email= models.EmailField(unique=True)
    username = None 

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} ({self.role if self.role else 'No Role'})"

class Attendance(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    role = models.CharField(max_length=50, blank=True)  
    check_in_time = models.DateTimeField()
    check_out_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.user.id}) - {self.check_in_time} to {self.check_out_time or 'Still Checked In'}"


