from django.db.models.signals import post_save, post_delete

from django.dispatch import receiver

from django.core.mail import send_mail

from .models import *

