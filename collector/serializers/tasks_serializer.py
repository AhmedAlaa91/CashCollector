from rest_framework import serializers
from ..models.collections_model import Collection 

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields =  ['customerName', 'dueDate','amount','collectionDate','deliveryDate','status']  