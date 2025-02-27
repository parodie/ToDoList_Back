from django.db import models
import uuid

class Category(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    user_id = models.UUIDField() # User-specific identifier, typically generated or received from the frontend
    name = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.name


class Task(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False) 
    user_id = models.UUIDField() # User-specific identifier, typically generated or received from the frontend
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(
        max_length=20,
        choices=[('faible', 'Faible'), ('moyen', 'Moyen'), ('élevé', 'Élevé')],        
        default='moyen'
    )  
    
    def __srt__(self):
        return self.title