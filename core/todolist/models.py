from django.db import models

# Create your models here.

class Task(models.Model):
    user = models.ForeignKey('accounts.User' , on_delete=models.CASCADE) 
    title = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True )
