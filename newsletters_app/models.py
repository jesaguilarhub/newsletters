from django.db import models
from django.contrib.auth import get_user_model
from tags.models import Tag

class Newsletter(models.Model):
    name = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=255, null=False)
    image = models.CharField(max_length=300, null=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='newsletters_created', null=True)
    admins = models.ManyToManyField(get_user_model(), related_name='newsletters_editors')  
    subs = models.ManyToManyField(get_user_model(), through='SubscriptionsNewsletter', blank=True)
    tags = models.ManyToManyField(Tag, related_name='newsletters_tagged')
    votes = models.ManyToManyField(get_user_model(), related_name='Votes', blank=True)
    target = models.PositiveIntegerField(null=False)
    frequency = models.PositiveIntegerField(null=False)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class SubscriptionsNewsletter(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    newsletter = models.ForeignKey(Newsletter, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'newsletter'], name='unique_user_subscription')
        ]


