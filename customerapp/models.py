from django.db import models


class Customer(models.Model):
    user_id = models.ForeignKey("sellerapp.user",on_delete=models.CASCADE)
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    contactno = models.CharField(max_length=20)
    dob = models.DateField(null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    picture = models.FileField(upload_to="images/",default="images/default.jpg")

    def __str__(self):
        return self.firstname+" "+self.lastname