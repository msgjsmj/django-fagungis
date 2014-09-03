#!/bin/bash
set -e
# start unicorn with all options earlier declared in fabfile.py
source ~/.profile
source ~/.rvm/scripts/rvm

bundle exec unicorn_rails -c %(unicorn_rb)s