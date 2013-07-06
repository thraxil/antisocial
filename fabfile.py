from fabric.api import run, sudo, local, cd, env

env.hosts = ['oolong.thraxil.org', 'maru.thraxil.org', 'tardar.thraxil.org']
env.user = 'anders'

def restart_gunicorn():
    sudo("restart antisocial")

def prepare_deploy():
    local("./manage.py test")

def deploy():
    code_dir = "/var/www/antisocial/antisocial"
    with cd(code_dir):
        run("git pull origin master")
        run("./bootstrap.py")
        run("./manage.py migrate")
    restart_gunicorn()
