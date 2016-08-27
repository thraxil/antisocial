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

def create_execution(int i, String host) {
        cmd = { 
            stage "Docker Pull parallel- #"+i
    				println host
    			  env.h = host
            node {
    			     sh '''
echo "docker pull on $h"
ssh $h docker pull ${REPOSITORY}$REPO/$APP:$TAG
ssh $h cp /var/www/$APP/TAG /var/www/$APP/REVERT || true
ssh $h "echo export TAG=$TAG > /var/www/$APP/TAG"
					 '''
            }
        }
        return cmd
}


node {
		stage "Docker Pull All"
    def branches = [:]
    for (int i = 0; i < all_hosts.size(); i++) {
      branches["pull-${i}"] = create_execution(i, all_hosts[i])
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
		 stage "Restart Web Workers"
    def branches = [:]
    for (int i = 0; i < hosts.size(); i++) {
		  int n = i
      branches["web-restart-${i}"] = {
        stage "Restart Gunicorn parallel- #"+n
				println hosts[n]
			  env.h = hosts[n]
        node {
			     sh '''#!/bin/bash
echo "restarting gunicorn on $h"
ssh $h sudo stop $APP || true
ssh $h sudo start $APP
'''
        }
      }
    }
    parallel branches
}

node {
    def branches = [:]
    for (int i = 0; i < celery_hosts.size(); i++) {
		  int n = i
      branches["host-celery-${i}"] = {
        stage "Restart Worker parallel- #"+n
			  env.h = celery_hosts[n]
        node {
			     sh '''
echo "restart celery worker on $h"
ssh $h sudo stop $APP-worker || true
ssh $h sudo start $APP-worker
'''
        }
      }
    }
    parallel branches
}

node {
    def branches = [:]
    for (int i = 0; i < beat_hosts.size(); i++) {
		  int n = i
      branches["host-beat-${i}"] = {
        stage "Restart Beat parallel- #"+n
			  env.h = beat_hosts[n]
        node {
			     sh '''
echo "restart beat worker on $h"
ssh $h sudo stop $APP-beat || true
ssh $h sudo start $APP-beat
'''
        }
      }
    }
    parallel branches
}

node {
    stage "Opbeat"
		withCredentials([[$class: 'StringBinding', credentialsId : env.APP + '-opbeat', variable: 'OPBEAT_TOKEN', ]]) {
       sh '''curl https://intake.opbeat.com/api/v1/organizations/${OPBEAT_ORG}/apps/{OPBEAT_APP}/releases/ \
       -H "Authorization: Bearer ${OPBEAT_TOKEN}" \
       -d rev=`git log -n 1 --pretty=format:%H` \
       -d branch=`git rev-parse --abbrev-ref HEAD` \
       -d status=completed'''
		}
}
