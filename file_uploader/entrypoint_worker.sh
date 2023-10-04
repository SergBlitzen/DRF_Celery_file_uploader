#!/bin/bash


if [[ "${1}" == "celery" ]]; then
  celery -A file_uploader worker --loglevel=info --concurrency 4 -E
elif [[ "${1}" == "flower" ]]; then
  celery -A file_uploader flower
 fi
