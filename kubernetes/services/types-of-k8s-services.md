
# **Types of Kubernetes Services**

---

### **ClusterIP**
- **Default type**
- Accessible **only inside the cluster**
- Used for **internal communication between microservices**

---

### **NodePort**
- Exposes service on a **static port** on each node
- Accessible externally via:  
  `http://<NodeIP>:<NodePort>`

---

### **LoadBalancer**
- Integrates with **cloud provider**
- Exposes service externally with a **public IP**

---

### **ExternalName**
- Maps a service to an **external DNS name**

---

## **Basic Flow**
```
Client → Service → Selects Pod(s) → Pod responds
```

---

## **Quick Notes & Tips**
- ✅ **Labels must match**: Services route only to Pods matching their selector  
  *(e.g., `app: myapp`)*
- 🔒 **ClusterIP range**: Allocated by Kubernetes; reachable only inside the cluster
- 🔑 **NodePort range**: Usually `30000–32767`  
  *(If omitted, Kubernetes auto-assigns one)*
- ⚠️ **Security**: NodePort exposes your app on every node  
  → Consider **network policies** or **Ingress/LoadBalancer** for production

---

### **Troubleshooting**
```bash
kubectl describe svc myapp-nodeport   # Check endpoints
kubectl get endpoints myapp-clusterip # Should list Pod IPs/ports
# If empty → labels don’t match or Pods aren’t ready
```

---

## **External Access Flow**
```
External Client → NodeIP:31080 → NodePort Service → ClusterIP Service → Pod:targetPort (80)
```

---

### ✅ **Meaning of the fields**
- **port (8888)** → Service’s internal port (ClusterIP)  
- **targetPort (80)** → Actual port on the container inside the Pod  
- **nodePort (31080)** → External port exposed on each node  

**Inside cluster:**  
`myapp-nodeport:8888` (DNS name)  

**Outside cluster:**  
`NodeIP:31080`

---

## 🧭 **Quick Decision Guide**
- Internal microservice-to-microservice access → **ClusterIP**
- External access in Minikube quickly → **NodePort** or  
  `minikube service myapp-nodeport`
- Test from laptop without creating a Service → **port-forward**
