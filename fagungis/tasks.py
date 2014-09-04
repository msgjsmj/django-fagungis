#!/usr/bin/env python
# -*- coding: utf-8 -*-
from copy import copy
from datetime import datetime
from os.path import basename, abspath, dirname, isfile, join
from fabric.api import env, puts, abort, cd, hide, task
from fabric.operations import sudo, settings, run
from fabric.contrib import console
from fabric.contrib.files import upload_template
from fabric.contrib.console import confirm
from fabric.context_managers import prefix, shell_env

from fabric.colors import _wrap_with, green

green_bg = _wrap_with('42')
red_bg = _wrap_with('41')
fabungis_path = dirname(abspath(__file__))


##########################
## START Fagungis tasks ##
##########################

@task
def setup():
    puts(green_bg('Start setup...'))
    start_time = datetime.now()

    _verify_sudo()
    _install_dependencies()
    _create_rails_user()
    _setup_directories()
    _git_clone()
    _install_rvm()
    _install_require_gems()
    _asset_precompile()
    _upload_nginx_conf()
    _upload_unicorn_rb()
    _upload_rununicorn_script()
    _upload_supervisord_conf()


    end_time = datetime.now()
    finish_message = '[%s] Correctly finished in %i seconds' % \
    (green_bg(end_time.strftime('%H:%M:%S')), (end_time - start_time).seconds)
    puts(finish_message)


@task
def update():
    puts(green_bg('Start setup...'))
    start_time = datetime.now()

    _verify_sudo()
    _git_pull()
    _install_require_gems()
    _asset_precompile()
    _supervisor_restart()


    end_time = datetime.now()
    finish_message = '[%s] Correctly finished in %i seconds' % \
    (green_bg(end_time.strftime('%H:%M:%S')), (end_time - start_time).seconds)
    puts(finish_message)

@task
def setup_old():
    #  test configuration start
    if not test_configuration():
        if not confirm("Configuration test %s! Do you want to continue?" % red_bg('failed'), default=False):
            abort("Aborting at user request.")
    #  test configuration end
    if env.ask_confirmation:
        if not confirm("Are you sure you want to setup %s?" % red_bg(env.project.upper()), default=False):
            abort("Aborting at user request.")
    puts(green_bg('Start setup...'))
    start_time = datetime.now()

    # _verify_sudo
    # _install_dependencies()
    # _create_rails_user()
    # _setup_directories()
    # _hg_clone()
    # _install_virtualenv()
    # _create_virtualenv()
    # _install_gunicorn()
    # # _install_requirements()
    # _upload_nginx_conf()
    # _upload_rungunicorn_script()
    # _upload_supervisord_conf()

    end_time = datetime.now()
    finish_message = '[%s] Correctly finished in %i seconds' % \
    (green_bg(end_time.strftime('%H:%M:%S')), (end_time - start_time).seconds)
    puts(finish_message)


@task
def deploy():
    #  test configuration start
    if not test_configuration():
        if not confirm("Configuration test %s! Do you want to continue?" % red_bg('failed'), default=False):
            abort("Aborting at user request.")
    #  test configuration end
    _verify_sudo()
    if env.ask_confirmation:
        if not confirm("Are you sure you want to deploy in %s?" % red_bg(env.project.upper()), default=False):
            abort("Aborting at user request.")
    puts(green_bg('Start deploy...'))
    start_time = datetime.now()

    # hg_pull()
    # # _install_requirements()
    # _upload_nginx_conf()
    # _upload_rungunicorn_script()
    # _upload_supervisord_conf()
    # _prepare_rails_project()
    # _prepare_media_path()
    # _supervisor_restart()

    end_time = datetime.now()
    finish_message = '[%s] Correctly deployed in %i seconds' % \
    (green_bg(end_time.strftime('%H:%M:%S')), (end_time - start_time).seconds)
    puts(finish_message)


@task
def git_pull():
    with cd(env.code_root):
        sudo('git pull', user=env.rails_user)


@task
def test_configuration(verbose=True):
    errors = []
    parameters_info = []
    if 'project' not in env or not env.project:
        errors.append('Project name missing')
    elif verbose:
        parameters_info.append(('Project name', env.project))
    if 'repository' not in env or not env.repository:
        errors.append('Repository url missing')
    elif verbose:
        parameters_info.append(('Repository url', env.repository))
    if 'hosts' not in env or not env.hosts:
        errors.append('Hosts configuration missing')
    elif verbose:
        parameters_info.append(('Hosts', env.hosts))
    if 'rails_user' not in env or not env.rails_user:
        errors.append('rails user missing')
    elif verbose:
        parameters_info.append(('rails user', env.rails_user))
    if 'rails_user_group' not in env or not env.rails_user_group:
        errors.append('rails user group missing')
    elif verbose:
        parameters_info.append(('rails user group', env.rails_user_group))
    if 'rails_user_home' not in env or not env.rails_user_home:
        errors.append('rails user home dir missing')
    elif verbose:
        parameters_info.append(('rails user home dir', env.rails_user_home))
    if 'projects_path' not in env or not env.projects_path:
        errors.append('Projects path configuration missing')
    elif verbose:
        parameters_info.append(('Projects path', env.projects_path))
    if 'code_root' not in env or not env.code_root:
        errors.append('Code root configuration missing')
    elif verbose:
        parameters_info.append(('Code root', env.code_root))
    if 'rails_project_root' not in env or not env.rails_project_root:
        errors.append('rails project root configuration missing')
    elif verbose:
        parameters_info.append(('rails project root', env.rails_project_root))
    if 'rails_project_settings' not in env or not env.rails_project_settings:
        env.rails_project_settings = 'settings'
    if verbose:
        parameters_info.append(('rails_project_settings', env.rails_project_settings))
    if 'rails_media_path' not in env or not env.rails_media_path:
        errors.append('rails media path configuration missing')
    elif verbose:
        parameters_info.append(('rails media path', env.rails_media_path))
    if 'rails_static_path' not in env or not env.rails_static_path:
        errors.append('rails static path configuration missing')
    elif verbose:
        parameters_info.append(('rails static path', env.rails_static_path))
    if 'south_used' not in env:
        errors.append('"south_used" configuration missing')
    elif verbose:
        parameters_info.append(('south_used', env.south_used))
    if 'virtenv' not in env or not env.virtenv:
        errors.append('virtenv configuration missing')
    elif verbose:
        parameters_info.append(('virtenv', env.virtenv))
    if 'virtenv_options' not in env or not env.virtenv_options:
        errors.append('"virtenv_options" configuration missing, you must have at least one option')
    elif verbose:
        parameters_info.append(('virtenv_options', env.virtenv_options))
    if 'requirements_file' not in env or not env.requirements_file:
        env.requirements_file = join(env.code_root, 'requirements.txt')
    if verbose:
        parameters_info.append(('requirements_file', env.requirements_file))
    if 'ask_confirmation' not in env:
        errors.append('"ask_confirmation" configuration missing')
    elif verbose:
        parameters_info.append(('ask_confirmation', env.ask_confirmation))
    if 'gunicorn_bind' not in env or not env.gunicorn_bind:
        errors.append('"gunicorn_bind" configuration missing')
    elif verbose:
        parameters_info.append(('gunicorn_bind', env.gunicorn_bind))
    if 'gunicorn_logfile' not in env or not env.gunicorn_logfile:
        errors.append('"gunicorn_logfile" configuration missing')
    elif verbose:
        parameters_info.append(('gunicorn_logfile', env.gunicorn_logfile))
    if 'rungunicorn_script' not in env or not env.rungunicorn_script:
        errors.append('"rungunicorn_script" configuration missing')
    elif verbose:
        parameters_info.append(('rungunicorn_script', env.rungunicorn_script))
    if 'gunicorn_workers' not in env or not env.gunicorn_workers:
        errors.append('"gunicorn_workers" configuration missing, you must have at least one worker')
    elif verbose:
        parameters_info.append(('gunicorn_workers', env.gunicorn_workers))
    if 'gunicorn_worker_class' not in env or not env.gunicorn_worker_class:
        errors.append('"gunicorn_worker_class" configuration missing')
    elif verbose:
        parameters_info.append(('gunicorn_worker_class', env.gunicorn_worker_class))
    if 'gunicorn_loglevel' not in env or not env.gunicorn_loglevel:
        errors.append('"gunicorn_loglevel" configuration missing')
    elif verbose:
        parameters_info.append(('gunicorn_loglevel', env.gunicorn_loglevel))
    if 'nginx_server_name' not in env or not env.nginx_server_name:
        errors.append('"nginx_server_name" configuration missing')
    elif verbose:
        parameters_info.append(('nginx_server_name', env.nginx_server_name))
    if 'nginx_conf_file' not in env or not env.nginx_conf_file:
        errors.append('"nginx_conf_file" configuration missing')
    elif verbose:
        parameters_info.append(('nginx_conf_file', env.nginx_conf_file))
    if 'nginx_client_max_body_size' not in env or not env.nginx_client_max_body_size:
        env.nginx_client_max_body_size = 10
    elif not isinstance(env.nginx_client_max_body_size, int):
        errors.append('"nginx_client_max_body_size" must be an integer value')
    if verbose:
        parameters_info.append(('nginx_client_max_body_size', env.nginx_client_max_body_size))
    if 'nginx_htdocs' not in env or not env.nginx_htdocs:
        errors.append('"nginx_htdocs" configuration missing')
    elif verbose:
        parameters_info.append(('nginx_htdocs', env.nginx_htdocs))

    if 'nginx_https' not in env:
        env.nginx_https = False
    elif not isinstance(env.nginx_https, bool):
        errors.append('"nginx_https" must be a boolean value')
    elif verbose:
        parameters_info.append(('nginx_https', env.nginx_https))

    if 'supervisor_program_name' not in env or not env.supervisor_program_name:
        env.supervisor_program_name = env.project
    if verbose:
        parameters_info.append(('supervisor_program_name', env.supervisor_program_name))
    if 'supervisorctl' not in env or not env.supervisorctl:
        errors.append('"supervisorctl" configuration missing')
    elif verbose:
        parameters_info.append(('supervisorctl', env.supervisorctl))
    if 'supervisor_autostart' not in env or not env.supervisor_autostart:
        errors.append('"supervisor_autostart" configuration missing')
    elif verbose:
        parameters_info.append(('supervisor_autostart', env.supervisor_autostart))
    if 'supervisor_autorestart' not in env or not env.supervisor_autorestart:
        errors.append('"supervisor_autorestart" configuration missing')
    elif verbose:
        parameters_info.append(('supervisor_autorestart', env.supervisor_autorestart))
    if 'supervisor_redirect_stderr' not in env or not env.supervisor_redirect_stderr:
        errors.append('"supervisor_redirect_stderr" configuration missing')
    elif verbose:
        parameters_info.append(('supervisor_redirect_stderr', env.supervisor_redirect_stderr))
    if 'supervisor_stdout_logfile' not in env or not env.supervisor_stdout_logfile:
        errors.append('"supervisor_stdout_logfile" configuration missing')
    elif verbose:
        parameters_info.append(('supervisor_stdout_logfile', env.supervisor_stdout_logfile))
    if 'supervisord_conf_file' not in env or not env.supervisord_conf_file:
        errors.append('"supervisord_conf_file" configuration missing')
    elif verbose:
        parameters_info.append(('supervisord_conf_file', env.supervisord_conf_file))

    if errors:
        if len(errors) == 29:
            ''' all configuration missing '''
            puts('Configuration missing! Please read README.rst first or go ahead at your own risk.')
        else:
            puts('Configuration test revealed %i errors:' % len(errors))
            puts('%s\n\n* %s\n' % ('-' * 37, '\n* '.join(errors)))
            puts('-' * 40)
            puts('Please fix them or go ahead at your own risk.')
        return False
    elif verbose:
        for parameter in parameters_info:
            parameter_formatting = "'%s'" if isinstance(parameter[1], str) else "%s"
            parameter_value = parameter_formatting % parameter[1]
            puts('%s %s' % (parameter[0].ljust(27), green(parameter_value)))
    puts('Configuration tests passed!')
    return True


########################
## END Fagungis tasks ##
########################


def _verify_sudo():
    ''' we just check if the user is sudoers '''
    sudo('cd .')


def _install_dependencies():
    ''' Ensure those Debian/Ubuntu packages are installed '''
    packages = [
        "gcc-c++",
        "curl",
        "libcurl-devel",
        "libcurl",
        "patch",
        "readline",
        "readline-devel",
        "zlib",
        "zlib-devel",
        "libyaml-devel",
        "libffi-devel",
        "openssl-devel",
        "make",
        "bzip2",
        "autoconf",
        "automake",
        "libtool",
        "bison",
        "git-core",
        "sqlite",
        "sqlite-devel",
        "python-pip",
    ]

    _add_yum_repos()

    sudo("yum -y update")
    sudo("yum -y groupinstall 'Development Tools'")
    sudo("yum -y install %s" % " ".join(packages))
    sudo("yum -y --enablerepo=rpmforge-extras upgrade git")
    if "additional_packages" in env and env.additional_packages:
        sudo("yum -y install %s" % " ".join(env.additional_packages))

    _install_nginx()
    _install_supervisor()

    if confirm('Do you want to install Redis at target server?'):
        _install_redis()


def _add_yum_repos():
    sudo('rpm --import http://dl.fedoraproject.org/pub/epel/RPM-GPG-KEY-EPEL-6')
    try:
        sudo('rpm -Uvh http://download.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm')
    except:
        if not confirm("%s! Do you want to continue?" % red_bg('failed'), default=False):
            abort("Aborting at user request.")

    sudo('rpm --import http://apt.sw.be/RPM-GPG-KEY.dag.txt')
    try:
        sudo('rpm -ivh http://pkgs.repoforge.org/rpmforge-release/rpmforge-release-0.5.3-1.el6.rf.x86_64.rpm')
    except:
        if not confirm("%s! Do you want to continue?" % red_bg('failed'), default=False):
            abort("Aborting at user request.")


def _install_nginx():
    sudo("yum -y install nginx")
    sudo("chkconfig nginx on")
    sudo("service nginx start")


def _install_supervisor():
    sudo("pip install supervisor")
    try:
        sudo('mkdir /etc/supervisord.d')
    except:
        if not confirm("%s! Do you want to continue?" % red_bg('failed'), default=False):
            abort("Aborting at user request.")

    sudo("echo_supervisord_conf > /etc/supervisord.conf")
    sudo("echo [include] >> /etc/supervisord.conf")
    sudo("echo files = /etc/supervisord.d/*.conf >> /etc/supervisord.conf")

    if isfile('conf/supervisord'):
        ''' we use user defined supervisord template '''
        template = 'conf/supervisord'
    else:
        template = '%s/conf/supervisord' % fabungis_path
    upload_template(template, '/etc/init.d/supervisord',
                    context=env, backup=False, use_sudo=True)

    sudo('chmod +x /etc/init.d/supervisord')

    sudo("chkconfig --add supervisord")
    sudo("chkconfig supervisord on")

    try:
        sudo("service supervisord restart")
    except:
        if not confirm("%s! Do you want to continue?" % red_bg('failed'), default=False):
            abort("Aborting at user request.")


def _install_redis():
    sudo('rpm --import http://rpms.famillecollet.com/RPM-GPG-KEY-remi')

    try:
        sudo('rpm -Uvh http://rpms.famillecollet.com/enterprise/remi-release-6.rpm')
    except:
        if not confirm("%s! Do you want to continue?" % red_bg('failed'), default=False):
            abort("Aborting at user request.")

    sudo('yum -y --enablerepo=remi install redis')
    sudo('chkconfig redis on')
    sudo('service redis start')


def _create_rails_user():
    with settings(hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        res = sudo('useradd -d %(rails_user_home)s -m -r %(rails_user)s' % env)
    if 'already exists' in res:
        puts('User \'%(rails_user)s\' already exists, will not be changed.' % env)
        return
    #  set password
    sudo('passwd %(rails_user)s' % env)


def _setup_directories():
    try:
        sudo('mkdir -p %(projects_path)s' % env)
    except:
        if not confirm("%s! Do you want to continue?" % red_bg('failed'), default=False):
            abort("Aborting at user request.")

        # sudo('mkdir -p %(rails_user_home)s/logs/nginx' % env)  # Not used
        # prepare gunicorn_logfile
    try:
        sudo('mkdir -p %s' % dirname(env.unicorn_logfile))
    except:
        if not confirm("%s! Do you want to continue?" % red_bg('failed'), default=False):
            abort("Aborting at user request.")

        # puts('chmod -R 775 %s' % dirname(env.unicorn_logfile))
    try:
        sudo('touch %s' % env.unicorn_logfile)
    except:
        if not confirm("%s! Do you want to continue?" % red_bg('failed'), default=False):
            abort("Aborting at user request.")

        # prepare supervisor_stdout_logfile
    try:
        sudo('mkdir -p %s' % dirname(env.supervisor_stdout_logfile))
    except:
        if not confirm("%s! Do you want to continue?" % red_bg('failed'), default=False):
            abort("Aborting at user request.")

        # puts('chmod -R 775 %s' % dirname(env.supervisor_stdout_logfile))
    try:
        sudo('touch %s' % env.supervisor_stdout_logfile)
    except:
        if not confirm("%s! Do you want to continue?" % red_bg('failed'), default=False):
            abort("Aborting at user request.")

    try:
        sudo('mkdir -p %s' % dirname(env.nginx_conf_file))
    except:
        if not confirm("%s! Do you want to continue?" % red_bg('failed'), default=False):
            abort("Aborting at user request.")

    try:
        sudo('mkdir -p %s' % dirname(env.supervisord_conf_file))
    except:
        if not confirm("%s! Do you want to continue?" % red_bg('failed'), default=False):
            abort("Aborting at user request.")

    try:
        sudo('mkdir -p %s' % dirname(env.rununicorn_script))
    except:
        if not confirm("%s! Do you want to continue?" % red_bg('failed'), default=False):
            abort("Aborting at user request.")

    try:
        sudo('mkdir -p %(nginx_htdocs)s' % env)
    except:
        if not confirm("%s! Do you want to continue?" % red_bg('failed'), default=False):
            abort("Aborting at user request.")

    try:
        sudo('mkdir -p %s' % dirname(env.unicorn_rb))
    except:
        if not confirm("%s! Do you want to continue?" % red_bg('failed'), default=False):
            abort("Aborting at user request.")

    try:
        sudo('mkdir -p %(unicorn_pids)s' % env)
    except:
        if not confirm("%s! Do you want to continue?" % red_bg('failed'), default=False):
            abort("Aborting at user request.")

    sudo('chown -R %s %s' % (env.rails_user, env.rails_user_home))


def _git_clone():
    try:
        sudo('git clone %s %s' % (env.repository, env.code_root))
    except:
        if not confirm("%s! Do you want to continue?" % red_bg('failed'), default=False):
            abort("Aborting at user request.")

    try:
        sudo('mkdir %s/tmp' % env.code_root)
    except:
        if not confirm("%s! Do you want to continue?" % red_bg('failed'), default=False):
            abort("Aborting at user request.")

    with cd(env.code_root):
        sudo('git checkout %s' % env.branch)

    sudo('chown -R %s %s' % (env.rails_user, env.code_root))


def _git_pull():
    with cd(env.code_root):
        sudo('git pull', user=env.rails_user)

    with cd(env.code_root):
        sudo('git checkout %s' % env.branch)

    with cd(env.code_root):
        sudo('git pull', user=env.rails_user)


def _install_rvm():
    with cd(env.rails_user_home):
        sudo('\curl -sSL https://get.rvm.io | bash -s stable', user=env.rails_user)
        sudo('rvm install %s' % env.ruby_version, user=env.rails_user)
        sudo('gem install rdoc-data; rdoc-data --install', user=env.rails_user)
        sudo('gem install rails -v %s' % env.rails_version, user=env.rails_user)


def _install_require_gems():
    run_with_production_mode('bundle')


def _asset_precompile():
    run_with_production_mode('rake assets:precompile')


def _upload_unicorn_rb():
    ''' upload rungunicorn conf '''
    if isfile('config/unicorn.rb'):
        # ''' we use user defined unicorn.rb file '''
        template = 'config/unicorn.rb'
    else:
        template = '%s/conf/unicorn.rb' % fabungis_path
    upload_template(template, env.unicorn_rb,
                    context=env, backup=False, use_sudo=True)
    sudo('chown %s %s' % (env.rails_user, env.unicorn_rb))


def _upload_rununicorn_script():
    ''' upload rungunicorn conf '''
    if isfile('scripts/rununicorn.sh'):
        ''' we use user defined rununicorn file '''
        template = 'scripts/rununicorn.sh'
    else:
        template = '%s/scripts/rununicorn.sh' % fabungis_path
    upload_template(template, env.rununicorn_script,
                    context=env, backup=False, use_sudo=True)
    sudo('chmod +x %s' % env.rununicorn_script)


def run_with_production_mode(command):
    with prefix('RAILS_ENV=%s' % env.rails_env), cd(env.rails_project_root):
        sudo(command, user=env.rails_user)


def _test_nginx_conf():
    with settings(hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        res = sudo('nginx -t -c /etc/nginx/nginx.conf')
    if 'test failed' in res:
        abort(red_bg('NGINX configuration test failed! Please review your parameters.'))


def _upload_nginx_conf():
    ''' upload nginx conf '''
    local_nginx_conf_file = 'nginx.conf'
    if env.nginx_https:
        local_nginx_conf_file = 'nginx_https.conf'
    if isfile('conf/%s' % local_nginx_conf_file):
        ''' we use user defined conf template '''
        template = 'conf/%s' % local_nginx_conf_file
    else:
        template = '%s/conf/%s' % (fabungis_path, local_nginx_conf_file)
    context = copy(env)

    # Template
    upload_template(template, env.nginx_conf_file,
                    context=context, backup=False, use_sudo=True)

    try:
        sudo('mv /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf.bak')
    except:
        if not confirm("%s! Do you want to continue?" % red_bg('failed'), default=False):
            abort("Aborting at user request.")

    sudo('ln -sf %s /etc/nginx/conf.d/%s' % (env.nginx_conf_file, basename(env.nginx_conf_file)))
    _test_nginx_conf()
    sudo('service nginx restart')


def _reload_supervisorctl():
    sudo('%(supervisorctl)s reread' % env)
    sudo('%(supervisorctl)s reload' % env)
    sudo('%(supervisorctl)s restart %(project)s' % env)


def _upload_supervisord_conf():
    ''' upload supervisor conf '''
    if isfile('conf/supervisord.conf'):
        ''' we use user defined supervisord.conf template '''
        template = 'conf/supervisord.conf'
    else:
        template = '%s/conf/supervisord.conf' % fabungis_path
    upload_template(template, env.supervisord_conf_file,
                    context=env, backup=False, use_sudo=True)
    sudo('ln -sf %s /etc/supervisord.d/%s' % (env.supervisord_conf_file, basename(env.supervisord_conf_file)))
    _reload_supervisorctl()


def _supervisor_restart():
    with settings(hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        res = sudo('%(supervisorctl)s restart %(supervisor_program_name)s' % env)
    if 'ERROR' in res:
        print red_bg("%s NOT STARTED!" % env.supervisor_program_name)
    else:
        print green_bg("%s correctly started!" % env.supervisor_program_name)
