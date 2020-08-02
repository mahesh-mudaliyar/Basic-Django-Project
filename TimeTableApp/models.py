from django.db import models

class userfilepaths(models.Model):
    user_id = models.IntegerField(null=True)
    filepath = models.CharField(max_length = 50, null=True)
    date = models.CharField(max_length = 50, null=True)
