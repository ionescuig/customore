from django.db import models
from django.urls import reverse


class Quote(models.Model):
    quote   = models.CharField(max_length=50)
    results = models.IntegerField(default=100)
    date    = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.results

    def get_absolute_url(self):
        return reverse('quote', kwargs={'pk': self.pk})
