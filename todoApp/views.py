from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Category, Task
from .serializers import CategorySerializer, TaskSerializer
import uuid
from rest_framework import status



class CategoryViewSet(viewsets.ModelViewSet):
    # ModelViewSet: Provides complete CRUD operations (list, create, retrieve, update, delete) for the Category model automatically.
    # queryset: Initially sets all categories as available, but this is overridden by get_queryset()
    # serializer_class: Specifies which serializer converts Category models to/from JSON.
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    # get_queryset(): Overrides the default queryset to filter categories by user_id.
    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        print("user_id reçu:", user_id) 

        return Category.objects.filter(user_id=user_id)
    
    def perform_create(self, serializer):
        user_id = self.request.query_params.get('user_id')
        serializer.save(user_id=user_id)
    
    @action(detail=False, methods=['post'])
    def add_category(self, request):
        user_id = request.data.get('user_id')
        category_name = request.data.get('name')

        if not category_name or not user_id:
            return Response({"error": "Données manquantes"}, status=400)

        category = Category.objects.create(name=category_name, user_id=user_id)
        serializer = CategorySerializer(category)
        return Response({"category": serializer.data}, status=201)

    # @action decorator: Creates a custom endpoint beyond the standard CRUD operations.
    # detail=False: Makes this a collection-level action (operates on multiple records).
    @action(detail=False, methods=['post'])
    def initialize_user(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:  
            user_id = str(uuid.uuid4())       
        default_categories = ["Work", "Personal", "Shopping"]

        for category_name in default_categories:
            Category.objects.get_or_create(user_id=user_id, name=category_name)

        categories = Category.objects.filter(user_id=user_id)
        serializer = CategorySerializer(categories, many=True)

        return Response({"user_id": user_id, "categories": serializer.data})
    

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id:
            return Task.objects.filter(user_id=user_id)
        return Task.objects.all()

    def perform_create(self, serializer):
        user_id = self.request.data.get('user_id')
        category = serializer.validated_data.get('category')  
        serializer.save(user_id=user_id, category=category)

    def retrieve(self, request, *args, **kwargs):
        task = self.get_object()  
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id')
        task = self.get_object()
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

        