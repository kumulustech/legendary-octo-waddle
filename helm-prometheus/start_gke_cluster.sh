#!/bin/bash

PROJECT=${GOOGLE_CLOUD_PROJECT:-default-project}
CLUSTER=${CLUSTER:-default-cluster}
gcloud beta container --project "${PROJECT}" \
clusters create "${CLUSTER}" --zone "us-central1-c" --no-enable-basic-auth \
--cluster-version "1.18.12-gke.1210" --release-channel "regular" \
--machine-type "e2-medium" --image-type "COS" --disk-type "pd-standard" \
--disk-size "20" --metadata disable-legacy-endpoints=true --scopes \
"https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/logging.write",\
"https://www.googleapis.com/auth/monitoring","https://www.googleapis.com/auth/servicecontrol",\
"https://www.googleapis.com/auth/service.management.readonly","https://www.googleapis.com/auth/trace.append" \
--num-nodes "3" --enable-stackdriver-kubernetes --enable-ip-alias \
--network "projects/clouddeployments-kumulus/global/networks/default" \
--subnetwork "projects/clouddeployments-kumulus/regions/us-central1/subnetworks/default" \
--default-max-pods-per-node "110" --enable-autoscaling --min-nodes "0" --max-nodes "10" \
--no-enable-master-authorized-networks --addons HorizontalPodAutoscaling,HttpLoadBalancing,GcePersistentDiskCsiDriver \
--enable-autoupgrade --enable-autorepair --max-surge-upgrade 1 --max-unavailable-upgrade 0 \
--enable-shielded-nodes --node-locations "us-central1-c"


sleep 300

gcloud container clusters get-credentials ${CLUSTER} --zone us-central1-c --project ${PROJECT}

