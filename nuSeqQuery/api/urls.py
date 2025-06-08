
from django.urls import path
from . import views
urlpatterns = [
    path('sequence/fetch/', views.sequence_fetch, name='sequence_fetch'),
    path('sequence/analysis/', views.sequence_analysis, name='sequence_analysis'),
    path('sequence/analysis/results/', views.sequence_analysis_results, name='sequence_analysis_results'),
    path('sequence/analysis/results/pattern/<str:id>/', views.sequence_analysis_pattern_result, name='sequence_analysis_pattern_result'),
    path('sequence/task/', views.task_status_check, name='task_status_check'),

    #path('sequence/system/taskclean/', views.task_clean, name='task_clean'),
    #path('sequence/system/syscacheclean/', views.sys_cache_clean, name='sys_cache_clean'),
    #path('sequence/system/dbcacheclean/', views.db_cache_clean, name='db_cache_clean'),
    
   
]