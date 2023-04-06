from django.contrib import admin
from .models import Cart,Cartitem

# Register your models here.
class cartadmin(admin.ModelAdmin):
    list_display=('cart_id','dated_added')


class cartitemAadmin(admin.ModelAdmin):
    list_display=('product','cart','quantity','is_active')

admin.site.register(Cart,cartadmin)
admin.site.register(Cartitem,cartitemAadmin)