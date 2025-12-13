
# 🚀 Helm Commands Cheat Sheet  
*A quick reference for essential Helm operations: installation, upgrades, dry runs, template rendering, and value overrides.*

---

## 📌 Table of Contents
1. Setup & Repo Management
2. Install a Chart
3. Dry Run & Debug
4. Render Templates Locally
5. Show Chart Defaults
6. List & Inspect Releases
7. Upgrade a Release
8. Rollback
9. Uninstall
10. Common Overrides
11. Helm Best Practices
12. Troubleshooting Tips

---

## ✅ 1. Setup & Repo Management
```bash
# Add a Helm repo (register a chart source)
helm repo add bitnami https://charts.bitnami.com/bitnami

# Update all repos (refresh chart list)
helm repo update

# Search for charts in repos
helm search repo nginx
```

---

## ✅ 2. Install a Chart
```bash
# Install a chart (deploy an application)
helm install <release-name> <chart>
helm install my-nginx bitnami/nginx
```

**With overrides:**
```bash
# Install with custom values (override defaults)
helm install my-nginx bitnami/nginx \
  --set service.type=NodePort \
  --set service.nodePort=30080
```

---

## ✅ 3. Dry Run & Debug
```bash
# Simulate installation without applying changes
helm install my-nginx bitnami/nginx --dry-run --debug
```

---

## ✅ 4. Render Templates Locally
```bash
# Generate Kubernetes manifests without installing
helm template my-nginx bitnami/nginx > output.yaml
```

---

## ✅ 5. Show Chart Defaults
```bash
# Display default values for a chart
helm show values bitnami/nginx
```

---

## ✅ 6. List & Inspect Releases
```bash
# List all installed releases
helm list

# Check status of a specific release
helm status my-nginx

# View applied values for a release
helm get values my-nginx

# View full manifest applied to cluster
helm get manifest my-nginx
```

---

## ✅ 7. Upgrade a Release
```bash
# Update an existing release with new chart or values
helm upgrade my-nginx bitnami/nginx --set replicaCount=3
```

---

## ✅ 8. Rollback
```bash
# Revert a release to a previous revision
helm rollback my-nginx 1
```

---

## ✅ 9. Uninstall
```bash
# Remove a release and its resources
helm uninstall my-nginx
```

---

## ✅ 10. Common Overrides
```yaml
replicaCount=3
image.repository=nginx
image.tag=alpine
service.type=NodePort
service.nodePort=30080
fullnameOverride=beta
```

---

## ✅ 11. Helm Best Practices
- **Always use `--dry-run` before applying changes** to avoid surprises.
- **Pin chart versions** for stability:
  ```bash
  helm install my-nginx bitnami/nginx --version 15.0.0
  ```
- **Use `values.yaml` for complex overrides** instead of multiple `--set` flags.
- **Enable rollback strategy** in CI/CD pipelines.
- **Regularly update repos** with `helm repo update`.
- **Validate charts** before deploying:
  ```bash
  helm lint ./my-chart
  ```
- **Namespace isolation**: Always specify `--namespace` for clarity.

---


## ✅ 12. Troubleshooting Tips (TBS)
- **Check Helm client & server versions**:
  ```bash
  helm version
  ```
- **Debug failed installs/upgrades**:
  ```bash
  helm install my-nginx bitnami/nginx --dry-run --debug
  ```
- **View Kubernetes events**:
  ```bash
  kubectl describe pod <pod-name>
  ```
- **Clear failed releases**:
  ```bash
   helm uninstall <release-name>
  ```
- **If CRDs fail**: Apply CRDs first, then install chart.

---

🔥 **Pro Tip:** Combine Helm with GitOps tools like ArgoCD or Flux for production-grade deployments.


---

## ✅ 13. Working with `values.yaml`

### 📌 What is `values.yaml`?
- The **configuration file for Helm charts**.
- Defines **default values** used by chart templates.
- You can **override these defaults** during install or upgrade using:
  - `--set key=value` flags (quick overrides).
  - `-f custom-values.yaml` (recommended for complex configs).

---

### ✅ Example `values.yaml` (Basic)
```yaml
replicaCount: 2

image:
  repository: nginx
  tag: latest
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 80

resources: {}
nodeSelector: {}
tolerations: []
affinity: {}
```

---

### ✅ How to Use It
```bash
# Install using custom values.yaml
helm install demo ./demo -f values.yaml

# Upgrade using custom values.yaml
helm upgrade demo ./demo -f values.yaml
```

---

### ✅ Override Multiple Files (Merging)
```bash
# Merge multiple values files (later files override earlier ones)
helm install demo ./demo -f base-values.yaml -f prod-values.yaml
```

---

### ✅ Combine File and Inline Overrides
```bash
helm install demo ./demo -f values.yaml --set replicaCount=5 --set service.type=NodePort
```

---

### ✅ Best Practices for `values.yaml`
- **Keep environment-specific files** (e.g., `dev-values.yaml`, `prod-values.yaml`).
- **Use `helm show values <chart>`** to see all available keys before customizing.
- **Avoid too many `--set` flags**; prefer a file for clarity and version control.
- **Document overrides** in your repo for reproducibility.
- **Validate your file**:
  ```bash
  helm lint ./demo
  ```

---

🔥 **Pro Tip:** Store your `values.yaml` files in Git for traceability and use them in CI/CD pipelines.



---

## ✅ 14. Publishing Helm Charts to Artifact Hub

### 📌 Why Publish?
Artifact Hub is a central repository for Helm charts, making it easy to share and discover charts publicly or within your organization.

---

### ✅ Steps to Package and Publish

#### 1. **Create or Prepare Your Chart**
If you don’t have a chart yet:
```bash
helm create demo
```
This generates a basic chart in `./demo`.

---

#### 2. **Update Chart Metadata**
Edit `Chart.yaml`:
```yaml
apiVersion: v2
name: demo
description: A simple Helm chart example
type: application
version: 0.1.0
appVersion: "1.0"
```

---

#### 3. **Package the Chart**
```bash
helm package ./demo
```
This creates a `.tgz` file like:
```
demo-0.1.0.tgz
```

---

#### 4. **Generate an Index (for a Helm repo)**
If you want to host your own repo:
```bash
helm repo index .
```
This creates `index.yaml` for your chart repository.

---

#### 5. **Upload to Artifact Hub**
- Go to Artifact Hub.
- Sign in with GitHub or another provider.
- Create a **repository** (Helm type).
- Upload your `.tgz` chart or link to your Helm repo.

---

### ✅ Best Practices Before Publishing
- Run:
  ```bash
  helm lint ./demo
  ```
- Add a **README.md** with usage instructions.
- Include **values.yaml** with clear defaults.
- Add **LICENSE** and **annotations** in `Chart.yaml` for Artifact Hub metadata:
  ```yaml
  annotations:
    artifacthub.io/changes: |
      - Initial release
    artifacthub.io/license: Apache-2.0
    artifacthub.io/links: |
      - name: Documentation
        url: https://github.com/your-repo
  ```

---

🔥 **Pro Tip:** Automate publishing with GitHub Actions using:
[helm/chart-releaser-action](https://github.com/helm

