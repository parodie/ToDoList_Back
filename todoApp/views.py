from django.shortcuts import render
from django.http import JsonResponse
from .models import Category
import uuid

@csrf_exempt
@require_http_methods(["POST"])
def initialize_user(request):    
    try:
        user_id = uuid.uuid4()
    except ValueError:
        return JsonResponse({"error": "Invalid user_id"}, status=400)
    
    default_categories = ["Work", "Personal", "Shopping"]
    for category_name in default_categories:
        Category.objects.get_or_create(user_id=user_id, name=category_name)
    
    return JsonResponse({"user_id": str(user_id)})
    

@require_http_methods(["GET"])
def get_categories(request):
    user_id = request.headers.get('user_id')
    
    categories = Category.objects.filter(user_id=user_id)
    category_list = [{"id": str(category.id), "name": category.name} for category in categories]
    
    return JsonResponse({"categories": category_list})

@require_http_methods(["GET"])
def get_tasks(request):
    user_id = request.headers.get('user_id')
    
    tasks = Task.objects.filter(user_id=user_id).values(
        "id", "title", "description", "priority", "category", "created_at", "completed"
    )
    
    return JsonResponse({"tasks": list(tasks)})