from fabric.api import run, sudo, local, cd, env, roles, execute, runs_once

env.hosts = ['orlando.thraxil.org', 'condor.thraxil.org']
env.user = 'anders'
nginx_hosts = ['lolrus.thraxil.org']

env.roledefs = {
    'celery': ['condor.thraxil.org'],
    'web': ['orlando.thraxil.org'],
}
code_dir = "/var/www/antisocial/antisocial"


@roles('web')
def restart_gunicorn():
    sudo("restart antisocial")

@roles('celery')
def restart_celery():
    sudo("restart antisocial-celery")

@roles('celery')
def restart_celerybeat():
    sudo("restart antisocial-beat")

@roles('web')
def staticfiles():
    with cd(code_dir):
        run("make collectstatic")
        for n in nginx_hosts:
            run(("rsync -avp --delete media/ "
                 "%s:/var/www/antisocial/antisocial/media/") % n)


def prepare_deploy():
    local("make test")

@runs_once
def migrate():
    with cd(code_dir):
        run("make migrate")

def deploy():
    code_dir = "/var/www/antisocial/antisocial"
    with cd(code_dir):
        run("git pull origin master")
        migrate()
        staticfiles()
    execute(restart_gunicorn)
    execute(restart_celery)
    execute(restart_celerybeat)
