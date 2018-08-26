from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login, logout

from core.models import Task
from rest_framework import viewsets, status
from core.serializers import TaskSerializer
from rest_framework.response import Response

from core.tools import authenticate


class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, **kwargs):
        assignee = request.user.profile
        queryset = Task.objects.filter(assignee=assignee, organization=assignee.organiz_login)
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, **kwargs):
        assignee = request.user.profile
        queryset = Task.objects.filter(assignee=assignee, organization=assignee.organiz_login)
        task = get_object_or_404(queryset, pk=pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        assignee = request.user.profile
        organiz_login = assignee.organiz_login
        instance = self.get_object()
        if instance.assignee != assignee or instance.organization != organiz_login:
            return Http404
        self.perform_destroy(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def signin(request):
    """
    {"email": "root@test.com", "organiz":"TUSUR", "passw":"123qwe123"}
    """
    user_login = request.data.get('email')
    user_organiz = request.data.get('organiz')
    user_passw = request.data.get('passw')

    user = authenticate(email=user_login, organiz=user_organiz, password=user_passw)

    if user is not None:
        login(request, user)
        return Response(status=200)
    else:
        return Response(status=404)


@api_view(['GET'])
def signout(request):
    logout(request)
    return Response(status=200)
