#!/bin/bash

# Courtesy of: http://michal.karzynski.pl/blog/2013/06/09/django-nginx-gunicorn-virtualenv-supervisor/

NAME="DocDocGo"                                             # Name of the application
DJANGODIR=/home/ec2-user/DocDocGo-Server/Server_Modules     # Django project directory
SOCKFILE=/home/ec2-user/DocDocGo-Server/run/gunicorn.sock   # we will communicate using this unix socket
USER=ec2-user                                               # the user to run as
GROUP=ec2-user                                              # the group to run as
NUM_WORKERS=3                                               # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=ddg_core.settings                    # which settings file should Django use
DJANGO_WSGI_MODULE=ddg_core.wsgi                            # WSGI module name

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec /usr/local/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
  --log-file=-