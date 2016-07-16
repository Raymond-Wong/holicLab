from django.db import models

TICKET_TYPE = ((1, 'access'), (2, 'js'))
class Ticket(models.Model):
  ticket_type = models.CharField(max_length=6, choices=TICKET_TYPE, default=1)
  content = models.CharField(max_length=600)
  start_time = models.DateTimeField(auto_now=True)
  end_time = models.DateTimeField()
