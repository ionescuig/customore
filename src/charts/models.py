from django.db import models
from django.urls import reverse


class Quote(models.Model):
    quote           = models.CharField(max_length=50)
    results         = models.IntegerField(default=10)
    date            = models.DateTimeField(auto_now=True)
    brands          = models.TextField()
    items_lazada    = models.IntegerField(default=0)
    items_shopee    = models.IntegerField(default=0)

    def __str__(self):
        return self.quote

    def get_absolute_url(self):
        return reverse('quote', kwargs={'pk': self.pk})
