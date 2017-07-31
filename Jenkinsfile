// Sandbox approvals that you will need (at least):
// staticMethod org.codehaus.groovy.runtime.DefaultGroovyMethods plus java.lang.Object[]
// staticMethod org.codehaus.groovy.runtime.DefaultGroovyMethods getAt java.lang.Iterable int
// java.lang.Object[]
// staticMethod org.codehaus.groovy.runtime.DefaultGroovyMethods plus java.util.List java.lang.Object

TAG = 'build-' + env.BUILD_NUMBER
env.TAG = TAG

// check for required parameters. assign them to the env for
// convenience and make sure that an exception is raised if any
// are missing as a side-effect

env.APP = APP
env.REPO = REPO
env.ADMIN_EMAIL = ADMIN_EMAIL

def hosts = HOSTS.split(" ")

// optional (not all apps use celery/beat)
def celery_hosts = [:]
def beat_hosts = [:]
try {
    celery_hosts = CELERY_HOSTS.split(" ")
} catch (hostsErr) {
    celery_hosts = []
}
try {
    beat_hosts = BEAT_HOSTS.split(" ")
} catch (beatserr) {
    beat_hosts = []
}

def all_hosts = hosts + celery_hosts + beat_hosts as Set

def opbeat = true

try {
    env.OPBEAT_ORG = OPBEAT_ORG
    env.OPBEAT_APP = OPBEAT_APP
    // OPBEAT_TOKEN comes out of credential store
} catch (opbeatErr) {
    println "opbeat not configured"
    opbeat = false
}

def err = null
currentBuild.result = "SUCCESS"

try {
    node {
        stage 'Checkout'
        checkout scm
        stage "Build"
        retry_backoff(5) { sh "docker pull ${REPO}/${APP}:latest" }				
        sh "make build" 
        stage "Docker Push"
        retry_backoff(5) { sh "docker push ${REPO}/${APP}:${TAG}" }
    }

    node {
        def branches = [:]
        for (int i = 0; i < all_hosts.size(); i++) {
            branches["pull-${i}"] = create_pull_exec(i, all_hosts[i])
        }
        parallel branches
  
        stage "Migrate"
        def host = all_hosts[0]
        sh "ssh ${host} /usr/local/bin/docker-runner ${APP} migrate"

        stage "Collectstatic"
        sh "ssh ${host} /usr/local/bin/docker-runner ${APP} collectstatic"

				stage "Compress"
				sh "ssh ${host} /usr/local/bin/docker-runner ${APP} compress"
    }

    node {
        def branches = [:]
        for (int i = 0; i < hosts.size(); i++) {
            branches["web-restart-${i}"] = create_restart_web_exec(i, hosts[i])
        }
        parallel branches
    }

    node {
        def branches = [:]
        for (int i = 0; i < celery_hosts.size(); i++) {
            branches["celery-restart-${i}"] = create_restart_celery_exec(i, celery_hosts[i])
        }
        parallel branches
    }

    node {
        def branches = [:]
        for (int i = 0; i < beat_hosts.size(); i++) {
            branches["beat-restart-${i}"] = create_restart_beat_exec(i, beat_hosts[i])
        }
        parallel branches
    }

    if (opbeat) {
        node {
            stage "Opbeat"
            withCredentials([[$class: 'StringBinding', credentialsId : 'opbeat-secret', variable: 'OPBEAT_TOKEN', ]]) {
                sh '''curl https://intake.opbeat.com/api/v1/organizations/${OPBEAT_ORG}/apps/${OPBEAT_APP}/releases/ \
       -H "Authorization: Bearer ${OPBEAT_TOKEN}" \
       -d rev=`git log -n 1 --pretty=format:%H` \
       -d branch=`git rev-parse --abbrev-ref HEAD` \
       -d status=completed'''
            }
        }
    }

} catch (caughtError) {
    err = caughtError
    currentBuild.result = "FAILURE"
} finally {
    (currentBuild.result != "ABORTED") && node {
        step([$class: 'Mailer',
              notifyEveryUnstableBuild: true,
              recipients: ADMIN_EMAIL,
              sendToIndividuals: true])
    }

    /* Must re-throw exception to propagate error */
    if (err) {
        throw err
    }
}

// -------------------- helper functions ----------------------

def create_pull_exec(int i, String host) {
    cmd = { 
        node {
            stage "Docker Pull - "+i
            sh """
ssh ${host} docker pull \${REPOSITORY}\$REPO/${APP}:\$TAG
ssh ${host} cp /var/www/${APP}/TAG /var/www/${APP}/REVERT || true
ssh ${host} "echo export TAG=\$TAG > /var/www/${APP}/TAG"
"""
        }
    }
    return cmd
}

def create_restart_web_exec(int i, String host) {
    cmd = { 
        node {
            stage "Restart Gunicorn - "+i
            sh """
ssh ${host} sudo stop ${APP} || ssh ${host} sudo systemctl stop ${APP}.service || true
ssh ${host} sudo start ${APP} || ssh ${host} sudo systemctl start ${APP}.service
"""
        }
    }
    return cmd
}

def create_restart_celery_exec(int i, String host) {
    cmd = { 
        node {
            stage "Restart Worker - "+i
            sh """
ssh ${host} sudo stop ${APP}-worker || true
ssh ${host} sudo start ${APP}-worker
"""
            }
    }
    return cmd
}

def create_restart_beat_exec(int i, String host) {
    cmd = { 
        node {
            stage "Restart Beat - "+i
            sh """
ssh ${host} sudo stop ${APP}-beat || true
ssh ${host} sudo start ${APP}-beat
"""
        }
    }
    return cmd
}

// retry with exponential backoff
def retry_backoff(int max_attempts, Closure c) {
    int n = 0
    while (n < max_attempts) {
        try {
            c()
            return
        } catch (err) {
            if ((n + 1) >= max_attempts) {
                // we're done. re-raise the exception
                throw err
            }
            sleep(2**n)
            n++
        }
    }
    return
}
