from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from utils.pagination import PlanListPagination

from .models import UserAlert

from .serializers import AlertCreateSerializer, AlertListSerializer, FilterStatusSerializer

# Create your views here.

class AlertsViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = AlertListSerializer
    pagination_class = PlanListPagination

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

    @method_decorator(cache_page(60*60*2))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        
        alerts = UserAlert.objects.filter(user_id = request.user.id)
        if alerts:
            page = self.paginate_queryset(alerts)
            if page is not None:
                serializer = self.serializer_class(alerts, many = True)
                data = self.get_paginated_response(serializer.data).data
                return Response(
                    {
                        "success":True,
                        "message":"The list is returned",
                        "data":data
                    }
                )
        return Response(
            {
                "success":False,
                "message":"No alerts exists" 
            }
        )

    def destroy(self, request, pk,*args, **kwargs, ):
        try:
            alert = UserAlert.objects.get(id = pk, user_id = request.user.id)
            alert.delete()
            return Response(
                {
                    "success":True,
                    "message":"Deleted"
                },
                status=status.HTTP_204_NO_CONTENT
            )
        except UserAlert.DoesNotExist:
            return Response(
                {
                "success":False,
                "message":"A alert with such a index is not available for this user."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    @method_decorator(cache_page(60*60*2))
    @method_decorator(vary_on_cookie)
    @action(detail=False, url_path="filter-status", methods=["POST"])
    def filter_by_status(self, request, *args, **kwargs):

        serializer = FilterStatusSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        alerts = UserAlert.objects.filter(user_id = request.user.id, status = serializer.data['status'])
        if alerts:
            page = self.paginate_queryset(alerts)
            if page is not None:
                serializer = self.serializer_class(alerts, many = True)
                data = self.get_paginated_response(serializer.data).data
                return Response(
                    {
                        "data":data
                    }
                )

        return Response(
            {
                "success":False,
                "message":"No alerts exists" 
                }
        )