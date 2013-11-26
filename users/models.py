from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from data.models import Symbol


class Investor(models.Model):
    user = models.OneToOneField(User, related_name='investor')
    favourites = models.ManyToManyField(Symbol)

    def __unicode__(self):
        return "%s's investor profile" % self.user


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = Investor.objects.get_or_create(user=instance)


post_save.connect(create_user_profile, sender=User)
