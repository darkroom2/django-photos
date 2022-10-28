from django.conf import settings
from django.db import models


class Photo(models.Model):
    title = models.CharField(max_length=100)
    album_id = models.PositiveIntegerField()
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    color = models.CharField(max_length=7)
    image = models.ImageField(upload_to=settings.IMAGES_DIR)

    remote_url = models.URLField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']
