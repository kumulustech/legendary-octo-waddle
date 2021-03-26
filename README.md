# A demo of auto-remediation in a K8s "Cloud"

This demostration puts together a number of key elements of a basic auto-remediation engine in a Cloud service.  It does this by leveraging a number of current "Cloud Native" projects and implementing statically defined automation against common signals.  Thanks to the availabile K8s APIs, Prometheus, and the Prometheus Alert manager, and a little webhook implemetned remediator, we can see how this sort of service can be put together, and could be easily extedned to support any sort of autoremediation.

While the basic demo follows the following "sequence", it would be trivial to automatically register new alerts and remediation hooks through the API enabled alert manager service, or a new alert service could be developed to support more advanced auto-remediation by managing the metrics searches for delivering new alerts and then resolving the issues exposed by the metrics discovery.

## Demo Sequence

  Day0 - Developer deploys base application.  All is well (no alerts triggered, application is working "normally")
  App Update - A code update is pushed which breaks the application (thanks to the "smarts" of kubernetes, this break doesn't actually disable the application, but the new code is stuck). This is a common situation.
  Alert Manager - discovers the alert state, and sends the alert details to the configured service.
  Alert "rollback" service - recieves the request, and reverts the broken service to the previously deployed version

## Setup

To enable the demostration, bring up a k8s cluster (note that for the bofa test app, 5x 2c/4Gi machines seems to be about the minimum), use Helm 3 to install prometheus along with the alertmanager-values.yaml (add it as a values file with the helm install) to the monitoring namespace, apply the bofa app (bofa namespace) and deploy the rollout.yaml manifest to the bofa namespace.

Deeper dive instructions are in the helm-prometheus and rollback directories README files.