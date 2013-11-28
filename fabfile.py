from fabric.api import run, sudo, local, cd, env, roles, execute, runs_once

env.hosts = ['oolong.thraxil.org', 'maru.thraxil.org', 'tardar.thraxil.org']
env.user = 'anders'
nginx_hosts = ['lilbub.thraxil.org', 'lolrus.thraxil.org']

env.roledefs = {
    'celery': ['tardar.thraxil.org'],
    'web': ['maru.thraxil.org', 'oolong.thraxil.org'],
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
        run("./manage.py collectstatic --noinput --settings=antisocial.settings_production")
        for n in nginx_hosts:
            run(("rsync -avp --delete media/ "
                 "%s:/var/www/antisocial/antisocial/media/") % n)


def prepare_deploy():
    local("./manage.py test")

@runs_once
def migrate():
    with cd(code_dir):
        run("./manage.py migrate")

def deploy():
    code_dir = "/var/www/antisocial/antisocial"
    with cd(code_dir):
        run("git pull origin master")
        run("./bootstrap.py")
    migrate()
    staticfiles()
    execute(restart_gunicorn)
    execute(restart_celery)
    execute(restart_celerybeat)
