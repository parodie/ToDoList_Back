from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Category, Task
from .serializers import CategorySerializer, TaskSerializer
import uuid


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        user_id = self.request.headers.get('user_id')
        return Category.objects.filter(user_id=user_id)

    @action(detail=False, methods=['post'])
    def initialize_user(self, request):
        user_id = uuid.uuid4()  # Generate a new user_id
        default_categories = ["Work", "Personal", "Shopping"]

        for category_name in default_categories:
            Category.objects.get_or_create(user_id=user_id, name=category_name)

        return Response({"user_id": str(user_id)})
    

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        user_id = self.request.headers.get('User-ID')
        return Task.objects.filter(user_id=user_id)

    def perform_create(self, serializer):
        user_id = self.request.headers.get('User-ID')
        serializer.save(user_id=user_id)