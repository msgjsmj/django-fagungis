#!/bin/bash
set -e
# start unicorn with all options earlier declared in fabfile.py
source ~/.profile
source ~/.rvm/scripts/rvm

RESQUE_TERM_TIMEOUT=%(resque_term_timeout)s TERM_CHILD=%(resque_term_child)s INTERVAL=%(resque_interval)s QUEUE=%(resque_queue)s RAILS_ENV=%(rails_env)s bundle exec rake resque:work