a complete, simple, beginner-friendly example of using a Helm chart from a public repository, including every step and the purpose behind it.

We will:

Add a chart repository

Search for a chart

Install the chart

Check the installation

Customize values (basic)

Upgrade deployment

Uninstall and cleanup

We will use Bitnami’s NGINX chart, since it's a common example.

########################################################

Step 1 — Add the Helm Repository

Purpose: Helm needs a list of places (repositories) to download charts from.
$ helm repo add bitnami https://charts.bitnami.com/bitnami
$ helm repo list
$ helm repo update # Optional: Update repositories (pull latest metadata):

Step 2 — Search for Available Charts ( or check using the GUI )
$ helm search repo nginx

You will see something like:
bitnami/nginx    X.X.X   NGINX Open Source web server


Step 3 — Install the Chart
Purpose: Deploy the NGINX application into Kubernetes.
$ helm install my-nginx bitnami/nginx

Explanation:

helm install means deploy
my-nginx = release name (you choose this)
bitnami/nginx = chart you want to deploy


Step 4 — Verify What Was Installed
Check deployment, service, pods using kubectl:

You should see something like:

Deployment/nginx
Pod/my-nginx-xxxxx
Service/my-nginx

```
$ kubectl get all
NAME                            READY   STATUS    RESTARTS   AGE
pod/my-nginx-6cf9955df7-fnhdl   1/1     Running   0          15m

NAME                 TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
service/kubernetes   ClusterIP      10.96.0.1       <none>        443/TCP                      19d
service/my-nginx     LoadBalancer   10.103.43.222   <pending>     80:32530/TCP,443:32202/TCP   15m

NAME                       READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/my-nginx   1/1     1            1           15m

NAME                                  DESIRED   CURRENT   READY   AGE
replicaset.apps/my-nginx-6cf9955df7   1         1         1       15m

```


Step 5 — View Chart Default Values
Purpose: To know what configuration you can change.

$ helm show values bitnami/nginx
( we can >> to a temp file )


Step 6 — Customize the Installation (Basic Example)

Let’s change the port and service type:
Create a file called custom-values.yaml:
```
service:
  type: LoadBalancer
  ports:
    http: 8090
```

Now upgrade the existing release:
$ helm upgrade my-nginx bitnami/nginx -f custom-values.yaml

Explanation:

upgrade modifies the running deployment without reinstalling
The chart now exposes port 8090 through a LoadBalancer

$ kubectl get svc  # to confirm



Step 7 — Uninstall and Cleanup
When finished:

$ helm uninstall my-nginx
$ kubect get all  # to confirm


*********************************************************

Few important notes :

View the effective values used in the release:
$ helm get values my-nginx # This will show only the values you changed via custom-values.yaml or command flags.

If you want to see all values (defaults + your overrides merged):
$ helm get values my-nginx --all


