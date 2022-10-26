from django.db import models


class Photo(models.Model):
    title = models.CharField(max_length=100)
    album_id = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    color = models.CharField(max_length=7)
    remote_url = models.URLField()

    image = models.ImageField(upload_to='images/')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']
