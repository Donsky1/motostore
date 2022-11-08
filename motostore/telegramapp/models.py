from django.db import models


# Create your models here.
class TelegramUser(models.Model):
    telegram_id = models.PositiveIntegerField()
    first_name = models.CharField(max_length=50, blank=True, null=True)
    username = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    language_code = models.CharField(max_length=2, blank=True, null=True)

    def __str__(self):
        if self.username:
            return self.username
        else:
            return self.telegram_id


class TelegramRequest(models.Model):
    chat_id = models.CharField(max_length=50)
    uuid = models.CharField(max_length=300, unique=True)
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    motorcycle_ids = models.CharField(max_length=500)

    def __str__(self):
        return str(self.user) + ": " + str(self.motorcycle_ids)

