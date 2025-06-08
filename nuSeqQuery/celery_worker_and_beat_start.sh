#!/bin/bash

APP="nuSeqQuery"
WORKER1="nuSeqQuery_pattern_search_worker1"
WORKER2="nuSeqQuery_pattern_search_worker2"

BEAT="nuSeqQuery_pattern_search_beat"

echo "🚀 Start $WORKER1..."
celery -A $APP worker -l info --concurrency=1 --hostname=$WORKER1 &
echo "🚀 Start $WORKER2..."
celery -A $APP worker -l info --concurrency=1 --hostname=$WORKER2 &

#echo "🚀 Start $BEAT..."
#celery -A $APP beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler --detach --pidfile=celerybeat.pid

echo "✅ All workers and beat started successfully."