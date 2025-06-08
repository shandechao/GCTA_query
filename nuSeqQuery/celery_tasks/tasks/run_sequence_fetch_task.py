from celery import shared_task;
from celery_tasks.logic.test import test_hello;
import time


@shared_task
def sequence_fetch():
    """
    Start the sequence fetch task.
    """
    print("Starting sequence fetch task...")
    
    time.sleep(3)
    test_hello("Celery Task")
    time.sleep(3)
    test_hello("Celery aaaaaaaaaaaaaaaaaaaa")
    time.sleep(3)