from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=300)
    slug = models.SlugField(null=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):              
        return self.name
