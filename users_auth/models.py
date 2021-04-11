from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

USER_ROLES = (
    (1, 'Admin'),
    (2, 'User')
)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    details = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='users', null=True, blank=True)
    role = models.IntegerField(choices=USER_ROLES, default=1, null=True, blank=True)
    last_logout = models.DateTimeField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.get_full_name()

    @property
    def image_url(self):
        url = ''
        if self.image:
            url = self.image.url
        return url


# Creating UserProfile when an User is created.
@receiver(post_save, sender=User)
def create_user_information(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
