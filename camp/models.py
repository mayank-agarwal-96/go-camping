# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from .utils import unique_slug_generator


def upload_location(instance, filename):
    return "%s/%s" % (instance.slug, filename)


class Camp(models.Model):
    name = models.CharField(max_length=256)
    image = models.ImageField(upload_to=upload_location,
    	    null=True,
    	    blank=True,
    	    width_field="width_field",
    	    height_field="height_field")
    height_field = models.IntegerField(default=0, blank=True, null=True)
    width_field = models.IntegerField(default=0, blank=True, null=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    city = models.CharField(max_length=256)
    state = models.CharField(max_length=256)
    country = models.CharField(max_length=256)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

# def create_camp_slug(instance, new_slug=None):
#     slug = slugify(instance.name)
#     if new_slug is not None:
#         slug = new_slug

#     qs = Camp.objects.filter(slug=slug).order_by("-id")
#     exists = qs.exists()

#     if exists:
#         new_slug = "%s-%s" %(slug, qs.first().id)
#         return create_camp_slug(instance, new_slug)
#     return slug

def pre_save_camp_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(pre_save_camp_receiver, sender=Camp)



class Rate(models.Model):
    camp = models.ForeignKey(Camp)
    user = models.ForeignKey(User)
    rating = models.IntegerField(
    	    validators=[
                MaxValueValidator(5),
                MinValueValidator(1)
            ])
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-created']

    def __str__(self):
        return str(self.camp)