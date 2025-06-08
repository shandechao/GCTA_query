from celery.result import AsyncResult

from celery_tasks.tasks import sequence_fetch_task;
from celery_tasks.tasks import sequence_analysis_task;
from api.models import CompletedSequence, SequencePatternSearch;
import json;
#from asgiref.sync import sync_to_async


def sequence_fetch(db_name, rettype,queryid):
    seqtask = sequence_fetch_task.sequence_fetch.delay({"db_name": db_name, "rettype": rettype, "queryid": queryid});
    

    return {"status": "1","taskid":seqtask.id}



def sequence_loading_status_check(db_name, rettype, queryid, taskid):
    taskres = AsyncResult(taskid)
    celery_status = taskres.status;
    if celery_status == 'FAILURE':
        return {"status": "0", "message": "Task failed."}
    elif celery_status == 'SUCCESS':
        
        query_list = []
        for i in range(len(queryid)):
            query_list.append( f"{db_name}_{rettype}_{queryid[i]}");

        existing = CompletedSequence.objects.filter(id__in=query_list).values("id", "accession","tax_id","organism_name","description", "length");
        json_data =  list(existing)
        return {"status": "1",  "data": json_data}
    
    else:
        return ({"status": "2" ,"working_status": celery_status})



def get_sequence_pattern_location_by_ID(id):
    try:
        result = SequencePatternSearch.objects.filter(id=id).values_list("result", flat=True).first();
        
        result = result["result"]
        starts = result["starts"]
        ends = result["ends"];
        overlap_counts= result["overlap_counts"];
        csvstr="start,end,length,overlap";
        for i in range(len(starts)):
            csvstr+= f"\n{starts[i]},{ends[i]},{ends[i]-starts[i]},{overlap_counts[i]}"
        return csvstr;
    except:

        return "error";
        


def sequence_analysis_pattern_search_result(regex_pattern,analysis_ids):
    queryset = SequencePatternSearch.objects.filter(
        sequence_id__in=analysis_ids,
        pattern=regex_pattern
    ).values("id","sequence_id", "others")

    result={};
    for i in queryset:
        result[i["sequence_id"]] ={"id":str(i["id"]),"result":{},"plot":{}};
        try:
            
            result[i["sequence_id"]]["result"]= i["others"]["info"]
        except:
            pass;
        try:
            
            result[i["sequence_id"]]["plot"]= i["others"]["plot"]
        except:
            pass;


    return result;
#,
def sequence_analysis_pattern_search_status_check(taskid):
    taskres = AsyncResult(taskid)
    celery_status = taskres.status;
    if celery_status == 'FAILURE':
        return {"status": "0", "message": "Task failed."}
    elif celery_status == 'SUCCESS':
        
        return {"status": "1"}
    
    else:
        return ({"status": "2" ,"working_status": celery_status})


def sequence_analysis_pattern_search(regex_pattern, analysis_ids):
    
    seqatask = sequence_analysis_task.pattern_search.delay( regex_pattern, analysis_ids);
    return {"status": "1","taskid": seqatask.id}

def sequence_analysis_start(data):
    """
    Start the sequence analysis task.
    """
    # Here you would implement the logic to start the sequence analysis task
    # For now, we just return a success status
    return {"status": "1", "message": "Sequence analysis task started successfully."}