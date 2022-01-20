#!/bin/sh

# Reading variables from .env file.
if [ -f .env ] && [ -s .env ]
then
    export $(xargs <.env)
    # Check for RUN_FOR_EVER env variable
    if [ $RUN_FOR_EVER = "True" ]
    then
        tail -f /dev/null
    elif [  $RUN_FOR_EVER = "False" ]
    then
        python run.py
    fi
fi
