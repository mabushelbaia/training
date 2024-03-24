from django.contrib import admin
from .models import Flight, Passenger, Airport
# Register your models here.


class FLightAdmin(admin.ModelAdmin):
    list_display = ("id", "origin", "destination", "duration")
    list_filter = ("origin", "destination")
    search_fields = ("origin", "destination")
class PassengerAdmin(admin.ModelAdmin):
    filter_horizontal = ("flights",)

admin.site.register(Airport)
admin.site.register(Flight, FLightAdmin)
admin.site.register(Passenger, PassengerAdmin)

