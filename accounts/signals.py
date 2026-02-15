from django.db.models.signals import post_migrate, post_save
from django.contrib.auth.models import Group, Permission
from django.dispatch import receiver

from django.apps import apps
from accounts.models import User

@receiver(post_migrate)
def create_default_groups(sender, **Kwargs):
    if sender.name != 'accounts': 
        return

    collector_group, _ = Group.objects.get_or_create(name='collector')
    citizen_group, _ = Group.objects.get_or_create(name='citizen')
    admin_group, _ = Group.objects.get_or_create(name='admin')

    citizen_permissions = Permission.objects.filter(codename__in=['can_request_pickup'])
    collector_permissions = Permission.objects.filter(codename__in=['can_collect_waste'])
    admin_permissions = Permission.objects.filter(codename__in=['can_manage_system','can_verify_dump'])  

    citizen_group.permissions.set(citizen_permissions)  
    collector_group.permissions.set(collector_permissions)
    admin_group.permissions.set(admin_permissions)

@receiver(post_save, sender=User)
def assign_user_group(sender, instance, created, **kwargs):
    if not created:
        print(f"User updated, checking for role change...")
        return
    
    instance.groups.clear()  # Clear existing groups

    #Now assign group based on role
    if instance.role == User.Role.CITIZEN:
        instance.groups.add(Group.objects.get(name='citizen'))
    elif instance.role == User.Role.COLLECTOR:
        instance.groups.add(Group.objects.get(name='collector'))
    elif instance.role == User.Role.ADMIN:
        instance.groups.add(Group.objects.get(name='admin'))


