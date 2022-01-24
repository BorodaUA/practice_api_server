#!/bin/sh

# Reading variables from .env file.
if [ -f .env ] && [ -s .env ]
then
    export $(xargs <.env)
    # Run alembic migrations on project startup.
    cd /usr/src/app/db && alembic upgrade head
    # Check for RUN_FOR_EVER env variable
    if [ $RUN_FOR_EVER = "True" ]
    then
        tail -f /dev/null
    elif [  $RUN_FOR_EVER = "False" ]
    then
        cd /usr/src/app && python run.py
    fi
fi
