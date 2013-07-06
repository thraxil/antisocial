from fabric.api import run, sudo, local, cd, env, roles, execute

env.hosts = ['oolong.thraxil.org', 'maru.thraxil.org', 'tardar.thraxil.org']
env.user = 'anders'

env.roledefs = {
    'celery': ['tardar.thraxil.org'],
    'web': ['maru.thraxil.org', 'oolong.thraxil.org'],
}


@roles('web')
def restart_gunicorn():
    sudo("restart antisocial")

@roles('celery')
def restart_celery():
    sudo("restart antisocial-celery")

@roles('celery')
def restart_celerybeat():
    sudo("restart antisocial-beat")

def prepare_deploy():
    local("./manage.py test")

def deploy():
    code_dir = "/var/www/antisocial/antisocial"
    with cd(code_dir):
        run("git pull origin master")
        run("./bootstrap.py")
        run("./manage.py migrate")
    execute(restart_gunicorn)
    execute(restart_celery)
    execute(restart_celerybeat)
