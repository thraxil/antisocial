env.TAG = 'build-' + env.BUILD_NUMBER
env.APP = 'antisocial'
env.REPO = 'thraxil'

def hosts = ['dublin.thraxil.org', 'cobra.thraxil.org']
def celery_hosts = ['condor.thraxil.org']
def beat_hosts = ['condor.thraxil.org']

//def all_hosts = (hosts + celery_hosts + beat_hosts).unique()

def all_hosts = ['dublin.thraxil.org', 'cobra.thraxil.org', 'condor.thraxil.org']

env.OPBEAT_ORG = '68fbae23422f4aa98cb810535e54c5f1'
env.OPBEAT_APP = 'edc70f3770'
// OPBEAT_TOKEN comes out of credential store


def create_pull_exec(int i, String host) {
    cmd = { 
        stage "Docker Pull parallel- #"+i
        node {
    			   sh """
echo "docker pull on ${host}"
ssh ${host} docker pull \${REPOSITORY}\$REPO/\$APP:\$TAG
ssh ${host} cp /var/www/\$APP/TAG /var/www/\$APP/REVERT || true
ssh ${host} "echo export TAG=\$TAG > /var/www/\$APP/TAG"
					 """
            }
    }
    return cmd
}

def create_restart_web_exec(int i, String host) {
    cmd = { 
        stage "Restart Gunicorn parallel- #"+i
        node {
    			   sh """
echo "restarting gunicorn on ${host}"
ssh ${host} sudo stop \$APP || true
ssh ${host} sudo start \$APP
					 """
            }
    }
    return cmd
}

def create_restart_celery_exec(int i, String host) {
    cmd = { 
        stage "Restart Worker parallel- #"+i
        node {
    			   sh """
echo "restarting celery worker on ${host}"
ssh ${host} sudo stop \$APP-worker || true
ssh ${host} sudo start \$APP-worker
					 """
            }
    }
    return cmd
}

def create_restart_beat_exec(int i, String host) {
    cmd = { 
        stage "Restart Beat parallel- #"+i
        node {
    			   sh """
echo "restarting beat worker on ${host}"
ssh ${host} sudo stop \$APP-beat || true
ssh ${host} sudo start \$APP-beat
					 """
            }
    }
    return cmd
}


node {
   stage 'Checkout'
   checkout scm
  stage "Build"
  sh "make build" 
  stage "Docker Push"
  sh '''#!/bin/bash
n=0
until [ $n -ge 5 ]
do
   docker push $REPO/$APP:$TAG && break
   n=$[$n+1]
   sleep $n
done'''
}

node {
    def branches = [:]
    for (int i = 0; i < all_hosts.size(); i++) {
      branches["pull-${i}"] = create_pull_exec(i, all_hosts[i])
    }
    parallel branches
	
    stage "Migrate"
		env.h = all_hosts[0]
    sh '''
echo "migrate on $h"
ssh $h /usr/local/bin/docker-runner $APP migrate
'''
    stage "Collectstatic/Compress"
		sh '''
echo "collectstatic/compress on $h"
ssh $h /usr/local/bin/docker-runner $APP collectstatic
ssh $h /usr/local/bin/docker-runner $APP compress
'''
}


node {
    def branches = [:]
    for (int i = 0; i < hosts.size(); i++) {
		  int n = i
      branches["web-restart-${i}"] = create_restart_web_exec(i, hosts[i])
    }
    parallel branches
}


node {
    def branches = [:]
    for (int i = 0; i < celery_hosts.size(); i++) {
		  int n = i
      branches["host-celery-${i}"] = create_restart_celery_exec(i, celery_hosts[i])
    }
    parallel branches
}


node {
    def branches = [:]
    for (int i = 0; i < beat_hosts.size(); i++) {
		  int n = i
      branches["host-beat-${i}"] = create_restart_beat_exec(i, beat_hosts[i])
    }
    parallel branches
}

node {
    stage "Opbeat"
		withCredentials([[$class: 'StringBinding', credentialsId : env.APP + '-opbeat', variable: 'OPBEAT_TOKEN', ]]) {
       sh '''curl https://intake.opbeat.com/api/v1/organizations/${OPBEAT_ORG}/apps/${OPBEAT_APP}/releases/ \
       -H "Authorization: Bearer ${OPBEAT_TOKEN}" \
       -d rev=`git log -n 1 --pretty=format:%H` \
       -d branch=`git rev-parse --abbrev-ref HEAD` \
       -d status=completed'''
		}
}
