from django.db import models


class RateModel(models.Model):
    result = models.FloatField()

    def save(self, *args, **kwargs):
        self.result = round(self.result, 2)
        super(RateModel, self).save(*args, **kwargs)
