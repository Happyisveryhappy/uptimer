from django.db import models


class Monitor(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'), ('up','Up'), ('down','Down')]

    name = models.CharField(max_length=255)
    url = models.URLField(max_length=2083)
    interval = models.PositiveIntegerField(default=120) # default time to check in seconds
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='pending') #'up','down','pending'
    created_at = models.DateTimeField(auto_now_add=True)
    last_checked = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.url})"


class PingLog(models.Model):

    # url = models.ForeignKey(Monitor, on_delete=models.CASCADE) | this is wrong (figure out why or ask google)
    monitor = models.ForeignKey(Monitor, on_delete=models.CASCADE, related_name='logs') # cascade = deletes the url
    run_timestamp = models.DateTimeField(auto_now_add=True)
    response_code = models.IntegerField(null=True, blank=True)
    response_time = models.IntegerField() # in milliseconds
    success = models.BooleanField()
    error_message = models.TextField(blank=True, default='') 
    # null = db related, allows blank values to be *stored* or no
    # blank = ui related, allows forms to leave blank values or no
