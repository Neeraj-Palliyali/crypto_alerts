from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import UserAlert

from .serializers import AlertCreateSerializer

# Create your views here.

class AlertsViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = AlertCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = AlertCreateSerializer(data = request.data)
        serializer.is_valid(raise_exception= True)
        data = serializer.data
        try:
            UserAlert.objects.create(
                user = request.user,
                limit = data['limit'],
                alert_on = data['alert_on'],
            )
            return Response(
                {
                    "success":True,
                    "message":"Alert has been set"
                    }, 
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {
                    "success":False,
                    "message":"Something went wrong",
                    "debug":str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
