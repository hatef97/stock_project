import time
import random
from celery import shared_task


@shared_task
def verify_user(user_id):
    time.sleep(random.randint(1, 100))
    return 0
