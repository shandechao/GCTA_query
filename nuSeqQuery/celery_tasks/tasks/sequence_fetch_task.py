from celery import shared_task;
from celery_tasks.logic import sequence_handler;
import time
from django.conf import settings


@shared_task(bind=True,queue='sequence',rate_limit='2/s')
def sequence_fetch(self,data):
    
    queryid = data['queryid']
    db_name = data['db_name']
    rettype = data['rettype']

    query_list = []
    for i in range(len(queryid)):
        query_list.append( f"{db_name}_{rettype}_{queryid[i]}");
    
    search_res = sequence_handler.search_existing_sequences(query_list);

    missing_ids = search_res['missing_ids']
    if len(missing_ids) == 0:
        return 
    
    sequence_handler.download_sequences(missing_ids);

    return 


