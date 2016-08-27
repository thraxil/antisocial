env.TAG = 'build-' + env.BUILD_NUMBER
env.APP = 'antisocial'
env.REPO = 'thraxil'

// space separate hosts
env.HOSTS = 'dublin.thraxil.org cobra.thraxil.org'
env.CELERY_HOSTS = 'condor.thraxil.org'
env.BEAT_HOSTS = 'condor.thraxil.org'

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
    stage "Docker Pull"
    sh '''#!/bin/bash
hosts=(${HOSTS})
chosts=(${CELERY_HOSTS})
bhosts=(${BEAT_HOSTS})

for h in "${hosts[@]}"
do
    ssh $h docker pull ${REPOSITORY}$REPO/$APP:$TAG
done

for h in "${chosts[@]}"
do
    ssh $h docker pull ${REPOSITORY}$REPO/$APP:$TAG
done

for h in "${bhosts[@]}"
do
    ssh $h docker pull ${REPOSITORY}$REPO/$APP:$TAG
done'''
    stage "Migrate"
    sh '''#!/bin/bash
hosts=(${HOSTS})
h=${hosts[0]}

ssh $h cp /var/www/$APP/TAG /var/www/$APP/REVERT || true
ssh $h "echo export TAG=$TAG > /var/www/$APP/TAG"

ssh $h /usr/local/bin/docker-runner $APP migrate
'''
    stage "Collectstatic/Compress"
		sh '''#!/bin/bash
hosts=(${HOSTS})
h=${hosts[0]}
ssh $h /usr/local/bin/docker-runner $APP collectstatic
ssh $h /usr/local/bin/docker-runner $APP compress
'''
    stage "Restart"
		sh '''#!/bin/bash
hosts=(${HOSTS})
chosts=(${CELERY_HOSTS})
bhosts=(${BEAT_HOSTS})

for h in "${hosts[@]}"
do
    ssh $h cp /var/www/$APP/TAG /var/www/$APP/REVERT || true
    ssh $h "echo export TAG=$TAG > /var/www/$APP/TAG"
    ssh $h sudo stop $APP || true
    ssh $h sudo start $APP
done

for h in "${chosts[@]}"
do
    echo $h
    ssh $h cp /var/www/$APP/TAG /var/www/$APP/REVERT || true
    ssh $h "echo export TAG=$TAG > /var/www/$APP/TAG"
    ssh $h sudo stop $APP-worker || true
    ssh $h sudo start $APP-worker
done

for h in "${bhosts[@]}"
do
    echo $h
    ssh $h cp /var/www/$APP/TAG /var/www/$APP/REVERT || true
    ssh $h "echo export TAG=$TAG > /var/www/$APP/TAG"
    ssh $h sudo stop $APP-beat || true
    ssh $h sudo start $APP-beat
done'''
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
