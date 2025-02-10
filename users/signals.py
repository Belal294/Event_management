from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

User = get_user_model()

# 🎯 1️⃣ New User Registration হলে ইমেল পাঠানো হবে
@receiver(post_save, sender=User)
def send_activation_email(sender, instance, created, **kwargs):
    if created and instance.email:
        token = default_token_generator.make_token(instance)
        activation_url = f"{settings.FRONTEND_URL}/users/activate/{instance.id}/{token}/"

        subject = 'Activate Your Account'
        message = f'Hi {instance.username},\n\nPlease activate your account by clicking the link below:\n{activation_url}\n\nThank You!'
        recipient_list = [instance.email]

        try:
            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
            print(f"Activation email sent to {instance.email}")
        except Exception as e:
            print(f"Failed to send email to {instance.email}: {str(e)}")


@receiver(post_save, sender=User)
def assign_default_role(sender, instance, created, **kwargs):
    if created:
        default_group, _ = Group.objects.get_or_create(name='Participant')
        instance.groups.add(default_group)
        instance.save()
        print(f"User {instance.username} added to 'Participant' group")


def assign_user_role(instance):
    if instance.is_superuser:
        group, _ = Group.objects.get_or_create(name='Admin')
    elif hasattr(instance, 'is_organizer') and instance.is_organizer:
        group, _ = Group.objects.get_or_create(name='Organizer')
    else:
        group, _ = Group.objects.get_or_create(name='Participant')
    
    instance.groups.set([group])
    instance.save()
    print(f"User {instance.username} assigned to '{group.name}' group")
