from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, SystAdmin, SalesRep, Customer


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create corresponding profile when a new user is created
    """
    if created:
        if instance.user_role == 1:  # SystAdmin
            SystAdmin.objects.create(user=instance)
        elif instance.user_role == 2:  # SalesRep
            SalesRep.objects.create(user=instance)
        elif instance.user_role == 3:  # Customer
            Customer.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    """
    Handle profile updates when user role changes
    This is more complex as it involves deleting old profile and creating new one
    """
    # Only handle role changes for existing users (not newly created ones)
    if not kwargs.get('created', False):
        # Get the user's current profile
        current_profiles = []
        
        try:
            if hasattr(instance, 'systadmin'):
                current_profiles.append(('systadmin', instance.systadmin, 1))
        except SystAdmin.DoesNotExist:
            pass
            
        try:
            if hasattr(instance, 'salesrep'):
                current_profiles.append(('salesrep', instance.salesrep, 2))
        except SalesRep.DoesNotExist:
            pass
            
        try:
            if hasattr(instance, 'customer'):
                current_profiles.append(('customer', instance.customer, 3))
        except Customer.DoesNotExist:
            pass
        
        # Check if user role has changed
        expected_role = instance.user_role
        current_role = None
        
        if current_profiles:
            current_role = current_profiles[0][2]
        
        # If role has changed, delete old profile and create new one
        if current_role and current_role != expected_role:
            # Delete old profile
            for profile_name, profile_obj, role_id in current_profiles:
                profile_obj.delete()
            
            # Create new profile based on new role
            if expected_role == 1:
                SystAdmin.objects.create(user=instance)
            elif expected_role == 2:
                SalesRep.objects.create(user=instance)
            elif expected_role == 3:
                Customer.objects.create(user=instance)