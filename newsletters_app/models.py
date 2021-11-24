from django.db import models
from django.contrib.auth import get_user_model
from tags.models import Tag

class Newsletter(models.Model):
    name = models.CharField(max_length=100, null=False)
    description = models.CharField(null=False)
    image = models.ImageField(blank=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='newsletters')
    admins = models.ManyToManyField(get_user_model(), related_name='newsletters', null=True)  
    subscriptions = models.ManyToManyField(get_user_model(), through='Subscriptions')
    tags = models.ManyToManyField(Tag, on_delete=models.SET_NULL, null=True, related_name='newsletters')
    votes = models.ManyToManyField(get_user_model(), through='Votes')
    target = models.PositiveIntegerField(null=False)
    frequency = models.PositiveIntegerField(null=False)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Subscriptions(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    newsletter = models.ForeignKey(Newsletter, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'newsletter'], name='unique_user_subscription')
        ]

class Votes(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    newsletter = models.ForeignKey(Newsletter, on_delete=models.SET_NULL, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'newsletter'], name='unique_user_vote')
        ]
