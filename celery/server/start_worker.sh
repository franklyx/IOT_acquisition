#!/bin/bash

# Front Pattern
celery worker -A schedule -B -Q default,feed_tasks -E -c 2 -l info --autoscale=6,3"

# Daemon Pattern
celery multi start schedule -A schedule -B -l info -Q default,feed_tasks -E -c 2 -l info --autoscale=6,3  \
--pidfile=/tmp/schedule%I.pid --logfile=/var/log/celery/schedule%I.log
