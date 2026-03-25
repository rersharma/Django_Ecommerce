from django.db import models

# Create your models here.
class admin_user(models.Model):
    name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)


class product(models.Model):
    pname=models.CharField(max_length=255)
    ptype=models.CharField(max_length=255)
    pprice=models.CharField(max_length=255)
    p_photo=models.ImageField(upload_to='product_photo')
    pdescription=models.TextField()