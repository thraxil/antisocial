env.TAG = 'build-' + env.BUILD_NUMBER
env.APP = 'antisocial'
env.HOSTS = 'dublin.thraxil.org cobra.thraxil.org'
env.CELERY_HOSTS = 'condor.thraxil.org'
env.BEAT_HOSTS = 'condor.thraxil.org'
node {
   stage 'Checkout'
//   checkout([$class: 'GitSCM', branches: [[name: '*/master']], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[credentialsId: 'c8d31910-a178-474d-ba78-a5584dc61c6e', url: 'git@github.com:thraxil/antisocial.git']]])
   checkout scm
   stage "Build"
   sh "make build" 
   stage "Docker Push"
   sh '''#!/bin/bash
n=0
until [ $n -ge 5 ]
do
   docker push thraxil/antisocial:$TAG && break  # substitute your command here
   n=$[$n+1]
   sleep $n
done'''
}
node {
    stage "Deploy"
    sh '''#!/bin/bash
hosts=(${HOSTS})
chosts=(${CELERY_HOSTS})
bhosts=(${BEAT_HOSTS})

for h in "${hosts[@]}"
do
    ssh $h docker pull ${REPOSITORY}thraxil/$APP:$TAG
done

for h in "${chosts[@]}"
do
    ssh $h docker pull ${REPOSITORY}thraxil/$APP:$TAG
done

for h in "${bhosts[@]}"
do
    ssh $h docker pull ${REPOSITORY}thraxil/$APP:$TAG
done

h=${hosts[0]}

ssh $h cp /var/www/$APP/TAG /var/www/$APP/REVERT || true
ssh $h "echo export TAG=$TAG > /var/www/$APP/TAG"

ssh $h /usr/local/bin/docker-runner $APP migrate
ssh $h /usr/local/bin/docker-runner $APP collectstatic
ssh $h /usr/local/bin/docker-runner $APP compress

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
		withCredentials([[$class : 'StringBinding', credentialsId : 'antisocial-opbeat', variable: 'OPBEAT_TOKEN']]) {
       sh '''curl https://intake.opbeat.com/api/v1/organizations/68fbae23422f4aa98cb810535e54c5f1/apps/edc70f3770/releases/ \
       -H "Authorization: Bearer ${OPBEAT_TOKEN}" \
       -d rev=`git log -n 1 --pretty=format:%H` \
       -d branch=`git rev-parse --abbrev-ref HEAD` \
       -d status=completed'''
		}
}
