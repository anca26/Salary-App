from django.conf import settings
from django.db import models

#models for core entities

class Department(models.Model):
    name = models.CharField(max_length=120, unique=True)
    code = models.CharField(max_length=10, unique=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    
class Employee(models.Model):
    
    class Role(models.TextChoices):
        EMPLOYEE = "EMPLOYEE", "Employee"
        MANAGER = "MANAGER", "Manager"
        ADMIN = "ADMIN", "Admin"
        
    # user = models.OneToOneField(settings.AUTH_USER_MODEL, 
    #                             on_delete=models.CASCADE,
    #                             related_name="employee_profile")
    
    employee_id = models.CharField(max_length=20, unique=True, db_index=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.EMPLOYEE)
    
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.EmailField(unique=True)
    
    cnp = models.CharField(max_length=13, unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name="employees")
    manager = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="reports")
    
    base_salary = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=["department","role"]),
            models.Index(fields=["manager"]),
        ]

    def __str__(self):
        return f"{self.employee_id} - {self.first_name} {self.last_name} {self.email}"