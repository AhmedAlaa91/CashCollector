# -*- coding: utf-8 -*-
from django.core.mail import EmailMessage
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..serializers.users_serializer import UserSerializer
from ..serializers.tasks_serializer import CollectionSerializer
from ..models.user_model import CustomUser
from ..models.collections_model import Collection
from django.utils import timezone
from datetime import timedelta
from django.db.models import Prefetch
from django.db.models import Sum, F
from rest_framework import status
from django.conf import settings
import logging
logger = logging.getLogger(__name__)

@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        tags=["USERS"],
        responses={200: UserSerializer()},
    ),
)
class UserStatus(APIView):
   def get(self, request , user_id):
     
     queryset = CustomUser.objects.get(pk =user_id)
     serialized_data = UserSerializer(queryset)
     return Response(serialized_data.data)
   

@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        tags=["USERS"],
        responses={200: CollectionSerializer()},
    ),
)
class CheckStatus(APIView):
   def get(self, request , user_id ):
    minAmount = settings.MIN_AMOUNT
    minhours = settings.MIN_HOURS

    
    min_datetime = timezone.now() - timedelta(hours=minhours)

    # Get tasks where status is collected 
    queryset = Collection.objects.filter(
            collectionDate__lte=min_datetime,
            status='collected',
            user = user_id
        )
    
    # Get user object 
    userObj = CustomUser.objects.get(pk =user_id)
    
    if (queryset):
        queryset = queryset if (queryset.aggregate(total_sum=Sum('amount'))['total_sum'] >= minAmount)  else []
        
    if (queryset):
       setattr(userObj, 'status', 'frozen')
       userObj.save()
       serialized_data = CollectionSerializer(queryset, many = True)
       return Response({
            'message': 'account is Frozen!',
            'data': serialized_data.data,
        }, status=status.HTTP_406_NOT_ACCEPTABLE)
    
    else :
      setattr(userObj, 'status', 'active')
      userObj.save()
    
      serialized_data = CollectionSerializer(queryset, many = True)
      return Response({
            'message': 'account is Active!',
            'data': serialized_data.data,
        }, status=status.HTTP_202_ACCEPTED)
    


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        tags=["USERS"],
        responses={200: CollectionSerializer()},
    ),
)
class CheckAllUsersStatus(APIView):
    def get(self, request):
        minAmount = settings.MIN_AMOUNT
        minhours = settings.MIN_HOURS

        min_datetime = timezone.now() - timedelta(hours=minhours)

        # Get tasks where status is collected
        queryset = Collection.objects.filter(
            collectionDate__lte=min_datetime,
            status='collected'
        )

        # Get all unique users from the queryset
        user_ids = queryset.values_list('user', flat=True).distinct()
        users = CustomUser.objects.filter(pk__in=user_ids)

        responses = []

        for user in users:
            user_queryset = queryset.filter(user=user)
            total_sum = user_queryset.aggregate(total_sum=Sum('amount'))['total_sum']

            if total_sum >= minAmount:
                user.status = 'frozen'
                message = 'account is Frozen!'
            else:
                user.status = 'active'
                message = 'account is Active!'

            user.save()

            serialized_data = CollectionSerializer(user_queryset, many=True)

            responses.append({
                'user_id': user.id,
                'message': message,
                'data': serialized_data.data,
            })

        usersNot = CustomUser.objects.exclude(pk__in=user_ids)

        for user in usersNot:
            user.status = 'active'
            message = 'account is Active!'

            user.save()

            responses.append({
                'user_id': user.id,
                'message': message,
                'data': [],
            })
            

        return Response(responses, status=status.HTTP_200_OK)