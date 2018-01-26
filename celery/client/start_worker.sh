#!/bin/bash

# Front Pattern
celery worker -A schedule -B -Q default,crontab -E -l info -c 4

# Daemon Pattern
celery multi start schedule -A schedule -B -l info -Q default,crontab -E -l info -c 4 \
 --pidfile=/tmp/%n%I.pid --logfile=/var/log/celery/%n%I.log
