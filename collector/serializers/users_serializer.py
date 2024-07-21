from rest_framework import serializers
from ..models.user_model import CustomUser  

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields =  ['id', 'first_name','last_name','manager_id','status'] 
    
