from django.db import models
from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.dispatch import receiver


class Oauth(models.Model):
    client_id = models.CharField(max_length=255, help_text='Client ID.')
    client_secret = models.CharField(max_length=255, help_text='Client Secret.')
    redirect_uri = models.URLField(help_text='Redirect URL')
    response_type = models.CharField(max_length=255, help_text='This should almost always be: code')
    grant_type = models.CharField(max_length=255, help_text='This should almost always be: authorization_code')
    scope = models.CharField(max_length=255, help_text='You at least need: user_read')

    def __str__(self):
        return 'Oauth Settings'

    class Meta:
        verbose_name = 'Oauth'
        verbose_name_plural = 'Oauth'


# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     email_verified = models.BooleanField(max_length=80, default=False)
#     twitch_id = models.IntegerField(blank=True, default=0)
#     logo_url = models.URLField(blank=True, default='')
#
#     def __str__(self):
#         return '{} - {}'.format(self.user, self.twitch_id)
#
#
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
