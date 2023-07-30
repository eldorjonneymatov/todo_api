from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from todo.models import Task
from todo.serializers import TaskSerializer


@api_view(['GET'])
def task_list_view(request):
    current_user = request.user
    if current_user.is_authenticated:
        user_tasks = Task.objects.filter(owner=request.user)
        serializer = TaskSerializer(user_tasks, many=True)
        return Response(serializer.data)
    else:
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(['GET', 'PUT', 'DELETE'])    
def task_detail_view(request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except:
        return Response({'Not found'}, status=status.HTTP_404_NOT_FOUND)

    current_user = request.user
    if not current_user.is_authenticated:
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        if task.owner != current_user:
            return Response({'No permission'}, status=status.HTTP_403_FORBIDDEN)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TaskSerializer(data=request.data, instance=task)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        task.delete()
        return Response({'Deleted successfully'})


@api_view(['POST'])
def task_create_view(request):
    current_user = request.user
    if current_user.is_authenticated:
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=current_user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)