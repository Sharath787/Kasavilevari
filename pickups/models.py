from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL
#Pickuprequest model to store pickup requests from citizens. It will have fields like:
# - citizen (ForeignKey to User)
# - collector (ForeignKey to User, nullable until assigned)
# - created_at (DateTimeField)
# - status (CharField with choices: REQUESTED, ASSIGNED, COMPLETED, DUMPED, CANCELLED)
# - assigned_at (DateTimeField, nullable)
# - collected_at (DateTimeField, nullable)
# - lattitude (DecimalField)
# - longitude (DecimalField)
# - waste_type (CharField with choices: WET, DRY, MIXED)
# - weight_estimate (DecimalField)

class PickupRequest(models.Model):
    class Status(models.TextChoices):
        REQUESTED = "requested"
        ASSIGNED = "assigned"
        COMPLETED = "completed"
        DUMPED = "dumped"
        CANCELLED = "cancelled"

    class WasteType(models.TextChoices):
        WET = "wet"
        DRY = "dry"
        MIXED = "mixed"

    citizen = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='pickup_requests')
    collector = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='collected_pickups')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.REQUESTED)
    assigned_at = models.DateTimeField(null=True, blank=True)
    collected_at = models.DateTimeField(null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    waste_type = models.CharField(max_length=10, choices=WasteType.choices)
    weight_estimate = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"PickupRequest {self.id} : {self.status}"

# Create your models here.
