from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(user)
admin.site.register(seller)
admin.site.register(product)
admin.site.register(categories)
admin.site.register(Cart)
admin.site.register(Cartitem)