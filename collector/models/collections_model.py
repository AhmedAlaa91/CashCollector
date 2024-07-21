from django.db import models
from .user_model import CustomUser
from datetime import datetime
class Collection(models.Model):
    CURRENCY_CHOICES = [
        ('usd', 'USD'),
    ]
    STATUS_CHOICES = [
        ('collected', 'Collected'),
        ('pending', 'Pending'),
        ('delivered', 'Delivered'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='collections')
    customerName = models.CharField(max_length=20 , blank=True , null=True)
    dueDate = models.DateTimeField(blank=False , null=False ,  default=datetime.now())
    amount = models.FloatField() 
    currency= models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='usd')
    collectionDate = models.DateTimeField(blank=True , null=True)
    deliveryDate = models.DateTimeField(blank=True , null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    address = models.CharField(max_length=50,blank=True , null=True)

    def __str__(self):
        return str(self.pk) + ' '+str(self.customerName) + ' ' + str(self.amount) + ' ' + str(self.dueDate) + ' ' + str(self.status)