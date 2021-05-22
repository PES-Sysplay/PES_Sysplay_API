from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.db import models

from activity.models import Activity
from user.models import Client


class Chat(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return '%s - %s' % (str(self.activity), str(self.client))

    @property
    def last_message(self):
        return self.messages.order_by('-date')[0]

    class Meta:
        unique_together = ('activity', 'client')


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return '%s - %s - %s' % (str(self.chat), str(self.user), str(self.date))

    @property
    def day(self):
        if self.date.today():
            return 'Hoy'
        elif self.date.date() + timedelta(days=1) > datetime.today():
            return 'Ayer'
        return self.date.strftime('%-d %b')

    @property
    def hour(self):
        return self.date.strftime('%H:%M')

    class Meta:
        unique_together = ('chat', 'user', 'date')
