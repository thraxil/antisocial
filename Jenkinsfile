env.TAG = 'build-' + env.BUILD_NUMBER
env.APP = 'antisocial'
env.REPO = 'thraxil'

def hosts = ['dublin.thraxil.org', 'cobra.thraxil.org']
def celery_hosts = ['condor.thraxil.org']
def beat_hosts = ['condor.thraxil.org']

def all_hosts = (hosts + celery_hosts + beat_hosts).unique()

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

node {
		def n = all_hosts.size() - 1
    def branches = [:]
    for (int i = 0; i < n; i++) {
      branches["host-${i}"] = {
        stage "Docker Pull parallel- #"+i
			  env.h = all_hosts[i]
        node {
			     sh '''
ssh $h docker pull ${REPOSITORY}$REPO/$APP:$TAG
ssh $h cp /var/www/$APP/TAG /var/www/$APP/REVERT || true
ssh $h "echo export TAG=$TAG > /var/www/$APP/TAG"
					 '''
        }
      }
    }
    parallel branches
	
    stage "Migrate"
		env.h = all_hosts[0]
    sh '''

ssh $h /usr/local/bin/docker-runner $APP migrate
'''
    stage "Collectstatic/Compress"
		sh '''
ssh $h /usr/local/bin/docker-runner $APP collectstatic
ssh $h /usr/local/bin/docker-runner $APP compress
'''

    def n = hosts.size() - 1
    def branches = [:]
    for (int i = 0; i < n; i++) {
      branches["host-${i}"] = {
        stage "Restart parallel- #"+i
			  env.h = hosts[i]
        node {
			     sh '''
ssh $h sudo stop $APP || true
ssh $h sudo start $APP
'''
        }
      }
    }
    parallel branches

    def n = celery_hosts.size() - 1
    def branches = [:]
    for (int i = 0; i < n; i++) {
      branches["host-${i}"] = {
        stage "Restart Worker parallel- #"+i
			  env.h = celery_hosts[i]
        node {
			     sh '''
ssh $h sudo stop $APP-worker || true
ssh $h sudo start $APP-worker
'''
        }
      }
    }
    parallel branches

    def n = beat_hosts.size() - 1
    def branches = [:]
    for (int i = 0; i < n; i++) {
      branches["host-${i}"] = {
        stage "Restart Worker parallel- #"+i
			  env.h = beat_hosts[i]
        node {
			     sh '''
ssh $h sudo stop $APP-worker || true
ssh $h sudo start $APP-worker
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
