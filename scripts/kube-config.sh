#!/bin/bash

aws eks --region ${AWS_DEFAULT_REGION} update-kubeconfig --name ${CLUSTER_NAME} --kubeconf ${KUBECONFIG}