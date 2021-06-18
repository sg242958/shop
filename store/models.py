from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class SignUp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=12)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['id']
        verbose_name_plural = 'SignUp'

class Category(models.Model):
    category = models.CharField(max_length=20)

    def __str__(self):
        return self.category

    class Meta:
        ordering = ["id"]
        verbose_name_plural = "Categories"

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    Description = models.CharField(max_length=100)
    image = models.ImageField(upload_to='img/')

    def __str__(self):
        return self.product_name

    class Meta:
        ordering = ["id"]
        verbose_name_plural = "Products"

class Feedback(models.Model):
    user = models.CharField(max_length=20)
    feedback = models.CharField(max_length=1000)
    datetimefield = models.DateTimeField(default=datetime.now(), blank=True)

    def __str__(self):
        return self.feedback

    class Meta:
        ordering = ["id"]
        verbose_name_plural = "Feedback"

class Cart(models.Model):
    user = models.CharField(max_length=20, default="")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.product_name

    class Meta:
        ordering = ['id']
        verbose_name_plural = 'Cart'

class Buy(models.Model):
    prod = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_no = models.CharField(max_length=10, default="")
    address = models.CharField(max_length=500)
    user = models.CharField(max_length=20, default="")
    status = models.CharField(max_length=100, default="")
    payment = models.CharField(max_length=100)
    name = models.CharField(max_length=50, default="")
    email = models.EmailField(default="")
    datetimefield = models.DateTimeField(default=datetime.now(), blank=True)
    mobile = models.CharField(max_length=12, default="")

    def __str__(self):
        return self.datetimefield

    class Meta:
        ordering = ['datetimefield']
        verbose_name_plural = 'Buy'
