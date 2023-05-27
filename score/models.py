from django.db import models
from django.utils import timezone
from datetime import datetime

class Quiz(models.Model):
    question = models.CharField(max_length=255)
    options = models.JSONField()
    right_answer = models.IntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=10, default='inactive')

    def save(self, *args, **kwargs):
        current_time = timezone.now()

        if isinstance(self.start_date, str):
            self.start_date = timezone.make_aware(datetime.strptime(self.start_date, "%Y-%m-%dT%H:%M:%S"))
        
        if isinstance(self.end_date, str):
            self.end_date = timezone.make_aware(datetime.strptime(self.end_date, "%Y-%m-%dT%H:%M:%S"))

        if self.start_date <= current_time < self.end_date:
            self.status = 'active'
        elif current_time >= self.end_date:
            self.status = 'finished'

        super().save(*args, **kwargs)
