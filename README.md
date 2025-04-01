# **Load-Balanced URL Shortener using Docker & Kubernetes**
## **Steps to run:**

**Step 1:** Setup Docker : `sudo systemctl start docker`

**Step 2:** Navigate to the directory where Dockerfile is present and Build a Docker Image: `sudo docker build -t url-shortener .`

**Step 3:** Start the container: `sudo docker run -d -p 5000:5000 url-shortener`

**Step 4:** Ensure the container running : `sudo docker ps`

**Step 5:** Test the api using the request command: `curl -X POST http://localhost:5000/shorten -H "Content-Type: application/json" -d '{"url": "https://www.google.com"}'`
or you can use *POSTMAN*

**Expected output:** You should receive a shortened url for www.google.com , which when clicked redirects you to google page.