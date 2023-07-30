from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from todo.models import Task
from todo.serializers import TaskSerializer
from .permissions import IsOwner


class TaskListView(APIView):
    permission_classes = (IsAuthenticated, )


    def get(self, request):
        user = request.user
        tasks = Task.objects.filter(owner=user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


class TaskCreateView(APIView):
    permission_classes = (IsAuthenticated,)


    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailView(APIView):
    permission_classes = (IsAuthenticated, IsOwner)


    def get(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        except:
            return Response('Not found', status=status.HTTP_404_NOT_FOUND)
        

class TaskUpdateView(APIView):
    permission_classes = (IsAuthenticated, IsOwner) 
    
    
    def put(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except:
            return Response('Not found', status=status.HTTP_404_NOT_FOUND)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDeleteView(APIView):
    permission_classes = (IsAuthenticated, IsOwner)
  
  
    def delete(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except:
            return Response('Not found', status=status.HTTP_404_NOT_FOUND)
        task.delete()
        return Response('Deleted successfully')