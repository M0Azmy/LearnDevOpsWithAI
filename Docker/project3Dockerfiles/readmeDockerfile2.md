# Dockerfile Guide: Flask Hello-World App

This README explains how to build a Docker image for a simple Flask application called **"hello-world"**, following best practices such as multi-stage builds, non-root user execution, and minimal image size.

---

## **Step 1: Use an Official Base Image**
Start with the official lightweight Python image:

```dockerfile
FROM python:3.10-slim AS builder
```

**Why?** Using an official image ensures security and compatibility.

**Multi-stage build:** The first stage (`builder`) installs dependencies, keeping the final image clean and small.

---

## **Step 2: Set Working Directory**
Define a working directory inside the container:

```dockerfile
WORKDIR /app
```

This is where your application files will reside.

---

## **Step 3: Install Dependencies**
Copy the `requirements.txt` file and install dependencies without caching:

```dockerfile
COPY ./app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
```

**Best practice:** `--no-cache-dir` reduces image size by avoiding unnecessary cache files.

---

## **Step 4: Create the Final Image**
Start the second stage for the final image:

```dockerfile
FROM python:3.10-slim AS final
WORKDIR /app
```

This stage will contain only what’s needed to run the app.

---

## **Step 5: Copy Dependencies from Builder**
Instead of reinstalling, copy the installed packages from the builder stage:

```dockerfile
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
```

---

## **Step 6: Add a Non-Root User**
For security, create a non-root user:

```dockerfile
RUN adduser --disabled-password --gecos '' appuser
```

---

## **Step 7: Copy Application Code**
Bring in your application files:

```dockerfile
COPY ./app/app.py .
```

Change ownership to the non-root user:

```dockerfile
RUN chown -R appuser:appuser /app
```

Switch to that user:

```dockerfile
USER appuser
```

---

## **Step 8: Expose Port and Run App**
Expose Flask’s default port and set the command:

```dockerfile
EXPOSE 5000
CMD ["python", "app.py"]
```

---

## **Summary of Best Practices Used**
✔ Multi-stage build for smaller image  
✔ Official base image for security  
✔ Non-root user for safety  
✔ No cache during dependency installation  
✔ Minimal layers and clear structure  

---

### **How to Build and Run**
1. Build the image:
   ```bash
   docker build -t flask-hello-world .
   ```
2. Run the container:
   ```bash
   docker run -p 5000:5000 flask-hello-world
   ```

Your Flask app will be available at `http://localhost:5000`.
