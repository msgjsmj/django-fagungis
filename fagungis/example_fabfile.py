#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import join
from fabric.api import env, task
from fagungis.tasks import *


@task
def project():
    #  name of your project - no spaces, no special chars
    env.project = 'PROJECT'
    #  hg repository of your project
    env.repository = 'GIT_URL'
    env.branch = 'GIT_BRANCH'
    env.rails_env = 'RAILS_ENV'
    #  hosts to deploy your project, users must be sudoers
    # env.hosts = ['root@172.16.252.132', ]
    env.hosts = ['USER@SERVER_URL', ]
    # additional packages to be installed on the server
    env.additional_packages = [
        "mysql",
        "mysql-devel",
        "mysql-libs",
        "libxml2",
        "libxml2-devel",
        "libxslt",
        "libxslt-devel",
        "memcached",
        "ruby",
        "ruby-devel",
        "ruby-rdoc",
        "rubygems",
        "ImageMagick",
    ]
    #  system user, owner of the processes and code on your server
    #  the user and it's home dir will be created if not present
    env.rails_user = 'DEPLOY_USER'
    # user group
    env.rails_user_group = env.rails_user
    #  the code of your project will be located here
    env.rails_user_home = join('/home', env.rails_user)
    #  projects path
    env.projects_path = join(env.rails_user_home, 'projects')
    #  the root path of your project
    env.code_root = join(env.projects_path, env.project)
    #  the path where manage.py of this project is located
    env.rails_project_root = env.code_root
    #  the Python path to a rails settings module.
    env.rails_project_settings = 'settings'
    # # rails media dir
    # env.rails_media_path = join(env.code_root, 'media')
    # #  rails static dir
    # env.rails_static_path = join(env.code_root, 'static')
    # #  rails media url and root dir
    # env.rails_media_url = '/site_media/media/'
    # env.rails_media_root = env.code_root
    # #  rails static url and root dir
    # env.rails_static_url = '/site_media/static/'
    # env.rails_static_root = env.code_root
    # #  do you use south in your rails project?
    # env.south_used = False
    # #  virtualenv root
    # env.virtenv = join(env.rails_user_home, 'envs', env.project)
    # #  some virtualenv options, must have at least one
    # env.virtenv_options = ['distribute', 'no-site-packages', ]
    # #  location of your pip requirements file
    # #  http://www.pip-installer.org/en/latest/requirements.html#the-requirements-file-format
    # #  set it to None to not use
    # env.requirements_file = join(env.code_root, 'requirements.txt')
    # #  always ask user for confirmation when run any tasks
    # env.ask_confirmation = True

    env.ruby_version = '1.9.3-p545'
    env.rails_version = '3.2.18'

    ### START gunicorn settings ###
    #  be sure to not have anything running on that port
    env.unicorn_bind = "127.0.0.1:8100"
    env.unicorn_logfile = '%(rails_user_home)s/logs/projects/unicorn_%(project)s.log' % env
    env.unicorn_rb = '%(rails_user_home)s/configs/unicorn/unicorn_%(project)s.rb' % env
    env.rununicorn_script = '%(rails_user_home)s/scripts/rununicorn_%(project)s.sh' % env
    env.unicorn_workers = 1
    env.unicorn_worker_class = "eventlet"
    env.unicorn_loglevel = "info"
    env.unicorn_pids = '%(rails_user_home)s/pids' % env
    # END gunicorn settings ###

    ### START nginx settings ###
    env.nginx_server_name = 'example.com'  # Only domain name, without 'www' or 'http://'
    env.nginx_conf_file = '%(rails_user_home)s/configs/nginx/%(project)s.conf' % env
    env.nginx_client_max_body_size = 10  # Maximum accepted body size of client request, in MB
    env.nginx_htdocs = '%(rails_user_home)s/htdocs' % env
    # will configure nginx with ssl on, your certificate must be installed
    # more info here: http://wiki.nginx.org/HttpSslModule
    env.nginx_https = False
    ### END nginx settings ###

    ### START supervisor settings ###
    # http://supervisord.org/configuration.html#program-x-section-settings
    # default: env.project
    env.supervisor_program_name = env.project
    env.supervisorctl = '/usr/bin/supervisorctl'  # supervisorctl script
    env.supervisor_autostart = 'true'  # true or false
    env.supervisor_autorestart = 'true'  # true or false
    env.supervisor_redirect_stderr = 'true'  # true or false
    env.supervisor_stdout_logfile = '%(rails_user_home)s/logs/projects/supervisord_%(project)s.log' % env
    env.supervisord_conf_file = '%(rails_user_home)s/configs/supervisord/%(project)s.conf' % env
    ### END supervisor settings ###
