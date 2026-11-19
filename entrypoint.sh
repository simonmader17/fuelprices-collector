#!/bin/sh
# busybox crond does not pass the container environment to jobs,
# so save it to a file that the crontab entry sources.
export -p > /collector/env
exec crond -f
