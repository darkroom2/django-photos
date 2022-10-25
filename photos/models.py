from django.db import models


class Photo(models.Model):
    title = models.CharField(max_length=100)
    album_ID = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    dominant_color_hex = models.CharField(max_length=7)
    url = models.CharField(max_length=100)

    image = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
