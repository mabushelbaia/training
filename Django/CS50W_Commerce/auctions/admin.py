from django.contrib import admin

# Register your models here.

from .models import Listing, User, wishlist

admin.site.register(Listing)
admin.site.register(User)
admin.site.register(wishlist)
