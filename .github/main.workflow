workflow "on pull request merge, delete the branch" {
  on = "pull_request"
  resolves = ["branch cleanup"]
}

action "branch cleanup" {
  uses = "jessfraz/branch-cleanup-action@master"
  secrets = ["GITHUB_TOKEN"]
}

workflow "run tests" {
  on = "push"
  resolves = ["docker push"]
}

action "Build docker image" {
  uses = "actions/docker/cli@master"
  args = "build -t thraxil/antisocial ."
}

action "Deploy branch filter" {
  needs = "Build docker image"
  uses = "actions/bin/filter@master"
  args = "branch master"
}

action "docker login" {
  needs = "Deploy branch filter"
  uses = "actions/docker/login@master"
  secrets = ["DOCKER_USERNAME", "DOCKER_PASSWORD"]
}

action "docker push" {
  needs = ["docker login"]
  uses = "actions/docker/cli@master"
  args = ["push", "thraxil/antisocial"]
}
