from django.db import models


class Raport(models.Model):
    data = models.DateField()
    time_start = models.TimeField()
    time_end = models.TimeField()
    description = models.CharField(max_length=70)

    def __str__(self):
        return f'{self.data} {self.time_start} {self.time_end} {self.description}'
