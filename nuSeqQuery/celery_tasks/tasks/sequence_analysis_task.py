from celery import shared_task;
from celery_tasks.logic import sequence_handler;
import time
from django.conf import settings
import json


@shared_task(bind=True,queue='analysis')
def pattern_search(self, regex_pattern,analysis_ids):
    
    for i in analysis_ids:
        sequence_handler.do_patterns_search(regex_pattern, i);
