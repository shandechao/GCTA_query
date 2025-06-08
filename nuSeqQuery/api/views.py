#from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse

from . import services

#@csrf_exempt
@api_view(['POST'])
def sequence_fetch(request):
    data = request.data 

    db_name = data.get('dataSource', None);
    queryid = data.get('queryId', None);
    rettype = data.get('rettype', None);

    if not db_name or not queryid or not rettype:
        return Response({"status": "0", "message": "Missing required parameters: dataSource, queryId, or rettype."}, status=400);

    result = services.sequence_fetch(db_name, rettype,queryid);

    return Response(result, status=200);

@api_view(['POST'])
def sequence_analysis(request):
    
    
    data = request.data;
    method = data.get('method', None);

    if method == "pattern_search":
        
        regex_pattern = data.get('pattern', None);
        analysis_ids = data.get('ids', None);

        if (not regex_pattern) or (not analysis_ids) or (len(analysis_ids) == 0) or (len(regex_pattern) <3):
            return Response({"status": "0", "message": "Missing required parameters: regexPattern or analysisIds."}, status=400);
        result = services.sequence_analysis_pattern_search(regex_pattern, analysis_ids);
        return Response(result, status=200);
    elif method == "other analysis":
        #do regex search
        return ;
    
    return Response({"status": "0", "message": "Invalid method specified."}, status=400);
    

@api_view(['POST'])
def sequence_analysis_results(request):
    data = request.data;
    method = data.get('method', None);
    if method == "pattern_search_result":
        
        regex_pattern = data.get('pattern', None);
        analysis_ids = data.get('ids', None);
        task_id = data.get('taskid', None);
        if (not regex_pattern) or (not analysis_ids) or (len(analysis_ids) == 0) or (len(regex_pattern) <3) or (not task_id):
            return Response({"status": "0", "message": "Missing required parameters: regexPattern or analysisIds."}, status=400);

        result = services.sequence_analysis_pattern_search_result(regex_pattern,analysis_ids);
    elif method == "pattern_search_status":
        task_id = data.get('taskid', None);
        if  (not task_id):
            return Response({"status": "0", "message": "Missing required parameters: task id."}, status=400);

        result = services.sequence_analysis_pattern_search_status_check(task_id);
        if result["status"] =="1":
            regex_pattern = data.get('pattern', None);
            analysis_ids = data.get('ids', None);
            result_query = services.sequence_analysis_pattern_search_result(regex_pattern,analysis_ids);
            result["data"]=result_query
        return Response(result,status=200)
    
    return Response({"status":"0"},status=400)

@api_view(["GET"])
def sequence_analysis_pattern_result(request,id):
    
    content = services.get_sequence_pattern_location_by_ID(id);

    response = HttpResponse(content, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Pattern_locations.csv"'
    return response



@api_view(['POST'])
def task_status_check(request):
    data = request.data 

    db_name = data.get('dataSource', None);
    queryid = data.get('queryId', None);
    rettype = data.get('rettype', None);
    taskid = data.get('taskid', None);
    res = services.sequence_loading_status_check(db_name, rettype, queryid, taskid);
    return Response(res, status=200)

@api_view(['POST'])
def analysis_task_status_check(request):
    data = request.data 
    method = data.get('method', None);
    if method == "pattern_search":
        regex_pattern = data.get('pattern', None);
        analysis_ids = data.get('ids', None);
        taskid = data.get('taskid', None);

    res = ""#services.sequence_loading_status_check(db_name, rettype, queryid, taskid);
    return Response(res, status=200)

def task_clean(request):
   
    return ""


def sys_cache_clean(request):
   
    return ""

def db_cache_clean(request):
   
    return ""
