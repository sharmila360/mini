from django.db import models
from django.contrib.auth.models import User  # Import the User model

# Contact model
class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    desc = models.TextField(max_length=500)
    phonenumber = models.IntegerField()

    def __str__(self):
        return self.name


# Product model
class Product(models.Model):
    product_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, default="")
    subcategory = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=300)
    image = models.ImageField(upload_to='images/images')

    def __str__(self):
        return self.product_name


# Orders model with ForeignKey to User
class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey to User
    items_json = models.CharField(max_length=5000)
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=90)
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)
    amountpaid = models.CharField(max_length=500, blank=True, null=True)
    paymentstatus = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.name


# OrderUpdate model
class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    update_desc = models.CharField(max_length=5000)
    delivered = models.BooleanField(default=False)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[:7] + "..."
