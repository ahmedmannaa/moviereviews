from django.db import models

# Create your models here.
class News(models.Model):
    class Meta:
        verbose_name_plural = "news"

    headline = models.CharField(max_length=200)
    body = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.headline[:30] + '...'
