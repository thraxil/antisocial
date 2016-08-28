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
def celery_hosts = CELERY_HOSTS.split(" ")
def beat_hosts = BEAT_HOSTS.split(" ")
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

def create_pull_exec(int i, String host) {
    cmd = { 
        node {
						stage "Docker Pull - "+i
						sh """
echo "docker pull on ${host}"
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
echo "restarting gunicorn on ${host}"
ssh ${host} sudo stop ${APP} || true
ssh ${host} sudo start ${APP}
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
echo "restarting celery worker on ${host}"
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
echo "restarting beat worker on ${host}"
ssh ${host} sudo stop ${APP}-beat || true
ssh ${host} sudo start ${APP}-beat
"""
				}
    }
    return cmd
}

// retry with exponential backoff
// returns boolean for success
def retry_backoff(int max_retries, Closure c) {
		int n = 0
		while(n < max_retries) {
				try {
						c()
						return true
				} catch (err) {
						sleep(2**n)
						n++
				}
		}
		return false
}


def err = null
currentBuild.result = "SUCCESS"



try {

node {
		stage 'Checkout'
		checkout scm
		stage "Build"
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
    sh """
echo "migrate on ${host}"
ssh ${host} /usr/local/bin/docker-runner ${APP} migrate
"""
    stage "Collectstatic/Compress"
		sh """
echo "collectstatic/compress on ${host}"
ssh ${host} /usr/local/bin/docker-runner ${APP} collectstatic
ssh ${host} /usr/local/bin/docker-runner ${APP} compress
"""
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
				branches["host-celery-${i}"] = create_restart_celery_exec(i, celery_hosts[i])
    }
    parallel branches
}


node {
    def branches = [:]
    for (int i = 0; i < beat_hosts.size(); i++) {
				branches["host-beat-${i}"] = create_restart_beat_exec(i, beat_hosts[i])
    }
    parallel branches
}

if (opbeat) {
		node {
				stage "Opbeat"
				withCredentials([[$class: 'StringBinding', credentialsId : APP + '-opbeat', variable: 'OPBEAT_TOKEN', ]]) {
						sh '''curl https://intake.opbeat.com/api/v1/organizations/${OPBEAT_ORG}/apps/${OPBEAT_APP}/releases/ \
       -H "Authorization: Bearer ${OPBEAT_TOKEN}" \
       -d rev=`git log -n 1 --pretty=format:%H` \
       -d branch=`git rev-parse --abbrev-ref HEAD` \
       -d status=completed'''
				}
		}
}

} catch (caughtError) {
    println "caught an exception"
    err = caughtError
    currentBuild.result = "FAILURE"
} finally {
    println "in finally"
    (currentBuild.result != "ABORTED") && node {
        println "got to the end"
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
