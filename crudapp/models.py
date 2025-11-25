from django.db import models
# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(blank=True,null=True)
    
    def __str__(self):
        return self.name