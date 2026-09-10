import requests
import time
from django.utils import timezone
from .models import PingLog


def check_status(monitor):
    start_time = time.time()
    response_code = None
    response_time = None
    is_success = False
    error_message = ""

    try:
        response = requests.get(monitor.url, timeout=5)
        latency_seconds = time.time()-start_time
        response_time = int(latency_seconds*1000) # converts latency in milliseconds
        response_code = response.status_code
        is_success = (200 <= response_code < 400) # if response_code is betn 200 and 400, its success


    except requests.exceptions.RequestException as err:
        latency_seconds = time.time()-start_time
        response_time = int(latency_seconds*1000)
        is_success = False
        error_message = str(err)

    # Now create the Log Entry in the DB & update status
    
    PingLog.objects.create(
            monitor = monitor,
            response_code=response_code,
            response_time=response_time,
            success=is_success,
            error_message=error_message
    )
    
    monitor.status = "up" if is_success else "down"
    monitor.last_checked = timezone.now()
    monitor.save()