from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, mixins
from todo.models import Task
from todo.serializers import TaskSerializer
from .permissions import IsOwner


class TaskListView(GenericAPIView, mixins.ListModelMixin):
    serializer_class = TaskSerializer
    queryset = Task.objects.filter()
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class TaskCreateView(GenericAPIView, mixins.CreateModelMixin):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = (IsAuthenticated,)


    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TaskDetailView(GenericAPIView, mixins.RetrieveModelMixin):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)


    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
        

class TaskUpdateView(GenericAPIView, mixins.UpdateModelMixin):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = (IsAuthenticated, IsOwner) 
    
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class TaskDeleteView(GenericAPIView, mixins.DestroyModelMixin):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = (IsAuthenticated, IsOwner) 
    
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)