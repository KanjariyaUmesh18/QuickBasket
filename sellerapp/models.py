from django.db import models


class user(models.Model):
    email = models.EmailField(max_length=30,unique=True)
    password = models.CharField(max_length=30)
    role = models.CharField(max_length=30)
    otp = models.CharField(default=456)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class seller(models.Model):
    user_id = models.ForeignKey(user,on_delete=models.CASCADE)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    contactno = models.CharField(max_length=30)
    seller_stock_name = models.CharField(max_length=30,null=True,blank=True)
    city = models.CharField(max_length=30,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    gstno = models.CharField(max_length=30,null=True,blank=True)
    picture = models.FileField(upload_to="images/",default="images/default.jpg")

    def __str__(self):
        return self.firstname +" " + self.lastname

class product(models.Model):
    user_id = models.ForeignKey(user,on_delete=models.CASCADE, blank=True, null=True)
    product_name = models.CharField(max_length=50)
    product_category = models.CharField(max_length=50)
    product_price = models.IntegerField()
    stock_qty = models.IntegerField()
    picture = models.FileField(upload_to="images/",default="images/default.jpg")
    description = models.TextField()
    discount = models.IntegerField()
    badge_text = models.CharField(max_length=50)
    weight_unit = models.CharField(max_length=50)
    brand = models.CharField(max_length=30)

    def __str__(self):
        return self.product_name

class categories(models.Model):
    user_id = models.ForeignKey(user,on_delete=models.CASCADE)
    categories_name = models.CharField(max_length=20)
    category_picture = models.FileField(upload_to="images/",default="images/default.jpg")
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.categories_name

class Cart(models.Model):
    from customerapp.models import Customer
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer.firstname
    
class Cartitem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    Product = models.ForeignKey(product,on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)

    def productPrice(self):
        return self.Product.product_price * self.qty

class Order(models.Model):
    from customerapp.models import Customer
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10,decimal_places=2)
    status = models.CharField(max_length=20,default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer.firstname

class Orderitem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(product,on_delete=models.CASCADE)
    qty = models.IntegerField()
    price = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return self.order.customer.firstname


    




