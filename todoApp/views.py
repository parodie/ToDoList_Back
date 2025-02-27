from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Category, Task
from .serializers import CategorySerializer, TaskSerializer
import uuid


class CategoryViewSet(viewsets.ModelViewSet):
    # ModelViewSet: Provides complete CRUD operations (list, create, retrieve, update, delete) for the Category model automatically.
    # queryset: Initially sets all categories as available, but this is overridden by get_queryset()
    # serializer_class: Specifies which serializer converts Category models to/from JSON.
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    # get_queryset(): Overrides the default queryset to filter categories by user_id.
    def get_queryset(self):
        user_id = self.request.headers.get('user_id')
        return Category.objects.filter(user_id=user_id)
    
    def perform_create(self, serializer):
        user_id = self.request.headers.get('user_id')
        serializer.save(user_id=user_id)

    # @action decorator: Creates a custom endpoint beyond the standard CRUD operations.
    # detail=False: Makes this a collection-level action (operates on multiple records).
    @action(detail=False, methods=['post'])
    def initialize_user(self, request):
        user_id = uuid.uuid4()  
        default_categories = ["Work", "Personal", "Shopping"]

        for category_name in default_categories:
            Category.objects.get_or_create(user_id=user_id, name=category_name)

        return Response({"user_id": str(user_id)})
    

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        user_id = self.request.headers.get('user_id')
        return Task.objects.filter(user_id=user_id)

    def perform_create(self, serializer):
        user_id = self.request.headers.get('user_id')
        serializer.save(user_id=user_id)