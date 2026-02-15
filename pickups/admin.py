from django.contrib import admin
from .models import PickupRequest


# Register your models here.
@admin.register(PickupRequest)
class PickupRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'citizen', 'collector', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('citizen__username', 'collector__username')
