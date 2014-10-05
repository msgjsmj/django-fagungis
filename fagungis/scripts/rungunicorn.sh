#!/bin/bash
set -e
# go in your project root
cd %(code_root)s
# activate the virtualenv
source %(virtenv)s/bin/activate
# start gunicorn with all options earlier declared in fabfile.py
exec gunicorn -w %(gunicorn_workers)s %(project)s.wsgi \
    --user=%(django_user)s \
    --bind=%(gunicorn_bind)s --log-level=%(gunicorn_loglevel)s \
    --log-file=%(gunicorn_logfile)s