# **Load-Balanced URL Shortener using Docker & Kubernetes**
## **Steps to run:**
***Week 1***
**Step 1:** Setup Docker : `sudo systemctl start docker`

**Step 2:** Navigate to the directory where Dockerfile is present and Build a Docker Image: `sudo docker build -t url-shortener .`

**Step 3:** Start the container: `sudo docker run -d -p 5000:5000 url-shortener`
or
**Step 4:**: if you have compose file: then `docker compose up --build`

**Step 4:** Ensure the container running : `sudo docker ps`

**Step 5:** Test the api using the request command: `curl -X POST http://localhost:5000/shorten -H "Content-Type: application/json" -d '{"url": "https://kubernetes.io/docs/concepts/architecture/control-plane-node-communication/"}'`
or you can use *POSTMAN*

**Expected output:** You should receive a shortened url for www.google.com , which when clicked redirects you to google page.

***Week 2***

Start minikube:

1. start minikube

```
minikube start
```

2. Use Minikube’s Docker Daemon

```
eval $(minikube docker-env)
```

3. Build the image:

```
docker build -t url-shortener .
```

4. Load the image into minikube:

```
 minikube image load url-shortener:latest
```

5. Check if Minikube has access to the image:

```
minikube image list | grep url-shortener
```

6. Deploy Redis Manifests:

```
kubectl apply -f redis-deployment.yaml
kubectl apply -f redis-service.yaml
```
7. Apply ConfigMaps & Secrets:

```
kubectl apply -f url-shortener-configmap.yaml
kubectl apply -f url-shortener-secret.yaml
```

8. Deploy our url-shortner-app:

```
kubectl apply -f url-shortener-deployment.yaml
kubectl apply -f url-shortener-service.yaml
```

9. Check if everything is running:

```
kubectl get pods
kubectl get services
```

10.  Get the Minikube Service URL

```
minikube service url-shortener
```

11. Test API

```
curl -X POST http://127.0.0.1:5000/shorten -H "Content-Type: application/json" -d '{"url": "https://www.google.com"}'
```
12. Check if url mapping is being stored in redis:
    (this command will open redis terminal inside the pod)
```
kubectl exec -it <redis-podname> -- redis-cli
```

for docker(WEEK 1):
```
docker ps
docker exec -it <container_name> redis-cli
```

13. Redis CLI command:
```
KEYS *
GET <Key>
```

14.🔄 Switching Back to Default Docker Daemon

```eval $(minikube docker-env --unset)```

15. Cleanup:
```
kubectl delete -f url-shortener-deployment.yaml
kubectl delete -f url-shortener-service.yaml
kubectl delete -f redis-deployment.yaml
kubectl delete -f redis-service.yaml
kubectl delete -f url-shortener-configmap.yaml
minikube stop
minikube delete
```


***Week 3***

Build the image
```
minikube start
docker build -t url-shortener .
minikube image load url-shortener:latest
```
Add all the addons for cpu metrics metrics-server, 

```
minikube addons enable metrics-server
```

Enable the load balancer Ingress
```
minikube addons enable ingress
```

Deploy Redis
```
kubectl apply -f redis-deployment.yaml
kubectl apply -f redis-service.yaml
```

Apply ConfigMap
```
kubectl apply -f url-shortener-configmap.yaml
```

Deploy URL Shortener
```
kubectl apply -f url-shortener-deployment.yaml
kubectl apply -f url-shortener-service.yaml
```

Apply HPA and Ingress
```
kubectl apply -f url-shortener-hpa.yaml
kubectl apply -f url-shortener-ingress.yaml
```

verify deployment
```
# Check if pods are running
kubectl get pods

# Check services
kubectl get services

# Check HPA status
kubectl get hpa

# Check ingress status
kubectl get ingress
```

Monitor the System
```
# Watch pod scaling
kubectl get pods -w

# Monitor CPU usage
kubectl top pods

# Check logs
kubectl logs -f -l app=url-shortener

# Monitor HPA
kubectl get hpa url-shortener-hpa --watch
```

Test the Application
```
# Get Minikube IP
minikube ip

# Test the API (replace IP_ADDRESS with Minikube IP)
curl -X POST http://127.0.0.1:38779/shorten -H "Content-Type: application/json" -d '{"url": "https://www.google.com"}'

# For stress testing (install apache bench first)
sudo apt-get install apache2-utils
ab -n 1000 -c 100 http://127.0.0.1:38779/Zf0Dl
```

Cleanup 
```
kubectl delete -f url-shortener-hpa.yaml
kubectl delete -f url-shortener-ingress.yaml
kubectl delete -f url-shortener-deployment.yaml
kubectl delete -f url-shortener-service.yaml
kubectl delete -f redis-deployment.yaml
kubectl delete -f redis-service.yaml
kubectl delete -f url-shortener-configmap.yaml
minikube stop
minikube delete
```


