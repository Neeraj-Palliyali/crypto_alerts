from django.utils.decorators import method_decorator
from django.views.decorators.vary import vary_on_cookie
from django.core.cache import cache

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from utils.pagination import AlertsListPagination

from .models import UserAlert

from .serializers import AlertCreateSerializer, AlertListSerializer, FilterStatusSerializer

# Create your views here.

class AlertsViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = AlertListSerializer
    pagination_class = AlertsListPagination

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
            cache.set('alerts_0',None)
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

    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        pagenum = self.request.query_params.get('page', None)
        if not pagenum:
            pagenum = 0
        cached_data = cache.get(f'alerts_{str(pagenum)}')
        if cached_data:
            return Response(
                    cached_data
                )

        alerts = UserAlert.objects.filter(user_id = request.user.id).order_by('created_at')
        if alerts:
            page = self.paginate_queryset(alerts)
            if page is not None:
                serializer = self.serializer_class(page, many = True)
                page_data = self.get_paginated_response(serializer.data).data
                response = {
                            "success":True,
                            "message":"The list is returned",
                            "data":page_data
                        }
                cache.set(f'alerts_{str(pagenum)}',response)
                cache.set(f'alerts_{str(pagenum)+1}',None)
                return Response(
                    response
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

    @action(detail=False, url_path="filter-status", methods=["POST"])
    def filter_by_status(self, request, *args, **kwargs):

        pagenum = self.request.query_params.get('page', None)

        serializer = FilterStatusSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        status = serializer.data['status']
        if not pagenum:
            pagenum = 0
        cached_data = cache.get(f'alerts_{status}_{str(pagenum)}')
        if cached_data:
            return Response(
                    cached_data
                )


        alerts = UserAlert.objects.filter(user_id = request.user.id, status = serializer.data['status'])
        if alerts:
            page = self.paginate_queryset(alerts)
            if page is not None:
                serializer = self.serializer_class(page, many = True)
                data = self.get_paginated_response(serializer.data).data
                response = {
                            "success":True,
                            "message":"The list is returned",
                            "data":data
                        }
                cache.set(f'alerts_{status}_{str(pagenum)}',response)
                cache.set(f'alerts_{status}_{str(pagenum)+1}',None)
                return Response(
                    response
                )

        return Response(
            {
                "success":False,
                "message":"No alerts exists" 
                }
        )