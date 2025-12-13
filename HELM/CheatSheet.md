Helm Commands Cheat Sheet
--------------------------

Quick reference for common Helm commands, including installation, upgrades, dry runs, template rendering, and
value overrides.

1) Install a Chart
$ helm install
$ helm install my-nginx bitnami/nginx

With overrides:
$ helm install my-nginx bitnami/nginx --set service.type=NodePort --set service.nodePort=30080

2) Dry Run & Debug
$ helm install my-nginx bitnami/nginx --dry-run --debug

3) Render Templates Locally
$ helm template my-nginx bitnami/nginx > output.yaml

4) Show Chart Defaults
$ helm show values bitnami/nginx

5) Upgrade a Release
$ helm upgrade my-nginx bitnami/nginx --set replicaCount=3

6) Rollback
$ helm rollback my-nginx 1

7) List & Status
$ helm list helm status my-nginx

8) Inspect Release
$ helm get values my-nginx helm get manifest my-nginx

9) Uninstall
$ helm uninstall my-nginx

Common Overrides
replicaCount=3 
image.repository=nginx 
image.tag=alpine 
service.type=NodePort
service.nodePort=30080 
fullnameOverride=beta
