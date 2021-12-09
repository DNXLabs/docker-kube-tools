#!/bin/bash -e

if [[ ! -f "kube-job.tpl.yml" ]]; then
    echo "---> ERROR: kube-job.tpl.yml not found"
    exit 0
fi

ERROR=0
if [[ -z "$APP_NAME" ]];		then echo "---> ERROR: Missing variable APP_NAME"; ERROR=1; fi
if [[ -z "$KUBE_NAMESPACE" ]];	then echo "---> ERROR: Missing variable KUBE_NAMESPACE"; ERROR=1; fi
if [[ -z "$JOB_IMAGE_NAME" ]];  then echo "---> ERROR: Missing variable JOB_IMAGE_NAME"; ERROR=1; fi
if [[ -z "$COMMAND_ARGS" ]];    then echo "---> ERROR: Missing variable COMMAND_ARGS"; ERROR=1; fi
if [[ "$ERROR" == "1" ]];		then exit 1; fi

envsubst < kube-job.tpl.yml > kube-job.yml
echo "---> Kube job yaml"
cat kube-job.yml

function run_job {
    echo "Kube job for ${APP_NAME}"
    echo "Kube job ===== JobCreation"
    kubectl apply -f kube-job.yml
    echo "Kube job ===== Waiting for ${APP_NAME}-job"
    kubectl wait --for=condition=Complete job/${APP_NAME}-job -n ${KUBE_NAMESPACE}
    echo "Kube job ===== Logs"
    kubectl logs -f $(kubectl get pod --selector=job-name=${APP_NAME}-job -n ${KUBE_NAMESPACE} --sort-by=.metadata.creationTimestamp -o jsonpath="{.items[-1].metadata.name}") -n ${KUBE_NAMESPACE}
    echo "Kube job ===== processed"
}

run_job
