# -*- coding: utf-8 -*-
from django.core.mail import EmailMessage
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from collector.utilities.scripts.callCheckStatusApi import checkUserStatusApi
from ..serializers.tasks_serializer import CollectionSerializer
from ..models.collections_model import Collection
from django.db.models import Prefetch
from rest_framework import status
from datetime import datetime
import logging
logger = logging.getLogger(__name__)

@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        tags=["TASKS"],
        responses={200: CollectionSerializer()},
    ),
)
class UserDoneTasks(APIView):
   def get(self, request , user_id):
     
     queryset = Collection.objects.filter(user =user_id).exclude(status= 'pending')  
     print(queryset)
     serialized_data = CollectionSerializer(queryset, many=True)
     return Response(serialized_data.data)


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        tags=["TASKS"],
        responses={200: CollectionSerializer()},
    ),
)

class UserNextTask(APIView):
   def get(self, request , user_id):
     
     queryset = Collection.objects.filter(user =user_id).filter(status= 'pending').order_by('dueDate')
     serialized_data = CollectionSerializer(queryset, many=True)
     return Response(serialized_data.data[0])


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        tags=["TASKS"],
        responses={200: CollectionSerializer()},
    ),
)

class CollectTask(APIView):
   def post(self, request , task_id):
     
    try:
        collection = Collection.objects.get(pk=task_id)
    except Collection.DoesNotExist:
        return Response({'error': 'Collection Item not found'}, status=status.HTTP_404_NOT_FOUND)


    checkedStatus=checkUserStatusApi(collection.user)

    if (checkedStatus ==  406):
        return Response({
            'message': 'account is Frozen!'
        }, status=status.HTTP_406_NOT_ACCEPTABLE)
    

    elif (checkedStatus ==  202) :
    
        setattr(collection, 'status', 'collected')
        setattr(collection, 'collectionDate', datetime.now())
        

        collection.save()  

        serializer = CollectionSerializer(collection)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    

@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        tags=["TASKS"],
        responses={200: CollectionSerializer()},
    ),
)
class payTask(APIView):
   def post(self, request , task_id):
     
    try:
        collection = Collection.objects.get(pk=task_id)
    except Collection.DoesNotExist:
        return Response({'error': 'Collection Item not found'}, status=status.HTTP_404_NOT_FOUND)

    
    setattr(collection, 'status', 'delivered')
    setattr(collection, 'deliveryDate', datetime.now())
    

    collection.save()  

    serializer = CollectionSerializer(collection)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


    