from django.db import models
from django.utils import timezone
# Create your models here.
class signup(models.Model):
    name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    mobile=models.BigIntegerField()
    password=models.CharField(max_length=255)
    photo=models.ImageField(upload_to='user_photo')
    address=models.TextField()

class user_order(models.Model):
    user_name=models.CharField(max_length=255)
    user_emailid=models.CharField(max_length=255)
    product_id=models.CharField(max_length=255)
    pname=models.CharField(max_length=255,default="NA")
    ptype=models.CharField(max_length=255)
    pprice=models.CharField(max_length=255)
    p_photo=models.TextField()
    pdescription=models.TextField()
    qunatity=models.IntegerField()
    total_price=models.IntegerField()
    order_shipped_status=models.TextField(default="Not Now")
    order_date = models.DateTimeField(default=timezone.now)

class contact(models.Model):
    name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    subject=models.CharField(max_length=255)
    message=models.TextField()
    reply=models.TextField(default="Na")
    