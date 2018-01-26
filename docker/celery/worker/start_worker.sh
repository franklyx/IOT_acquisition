#!/bin/bash

# Front Pattern
celery worker -A schedule -B -Q default,feed_tasks -E -l info --autoscale=6,3

# Daemon Pattern
celery multi start schedule -A schedule -B -l info -Q default,feed_tasks -E -l info --autoscale=6,3  \
 --pidfile=/tmp/%n%I.pid --logfile=/var/log/celery/%n%I.log
