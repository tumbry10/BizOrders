from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    USER_ROLE_TYPE_CHOICES = (
        (1, 'SystAdmin'),
        (2, 'SalesRep'),
        (3, 'Customer'),
    )
    email = models.EmailField(unique=True)
    user_role = models.PositiveSmallIntegerField(choices=USER_ROLE_TYPE_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Use email as the username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Remove 'email' from here since it's now the USERNAME_FIELD

    class Meta:
        db_table = 'users'
    
    def __str__(self):
        return self.username

GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
) 

class SystAdmin(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender = models.CharField(choices=GENDER_CHOICES, null=True, blank=True, max_length=10)
    bio = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'system_admins'
    
    def __str__(self):
        return f"System Admin {self.user.username}'s Profile"

class SalesRep(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender = models.CharField(choices=GENDER_CHOICES, null=True, blank=True, max_length=10)
    bio = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sales_reps'
    
    def __str__(self):
        return f"Sales Rep {self.user.username}'s Profile"

class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender = models.CharField(choices=GENDER_CHOICES, null=True, blank=True, max_length=10)
    bio = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'customers'
    
    def __str__(self):
        return f"Customer {self.user.username}'s Profile"