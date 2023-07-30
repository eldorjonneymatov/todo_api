from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, mixins, generics
from todo.models import Task
from todo.serializers import TaskSerializer
from .permissions import IsOwner


class TaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.filter()
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class TaskCreateView(generics.CreateAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = (IsAuthenticated,)


    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TaskDetailView(generics.RetrieveAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)


class TaskUpdateView(generics.UpdateAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = (IsAuthenticated, IsOwner) 
    

class TaskDeleteView(generics.DestroyAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = (IsAuthenticated, IsOwner) 