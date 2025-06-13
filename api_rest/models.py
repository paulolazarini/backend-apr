from django.db import models

class User(models.Model):
    user_name = models.CharField(max_length=30)
    user_age = models.IntegerField()

    def __str__(self):
        return self.user_name
