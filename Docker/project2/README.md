# DockerWithGemini
Docker labs using Gemini ( AI tools generally )

Markdown

# 🚀 DevOps Lab: Multi-Service Echo App

This project demonstrates a standard Docker Compose setup for a two-tier application, focusing on **internal networking**, **environment variable management**, and the **container build process**—all key skills for any DevOps role.

---

## 🏗️ Project Components

| Component | Technology | Service Name | Host Port |
| :--- | :--- | :--- | :--- |
| **App** | Python (Flask) | `app` | `8888` |
| **Cache** | Redis | `cache` | Internal Only |

---

## 📁 File Structure

The complete structure you've assembled includes:

. ├── app/ │ ├── app.py │ ├── Dockerfile │ └── requirements.txt ├── .env <-- Your custom configuration file ├── docker-compose.yml <-- The orchestration file └── README.md <-- This file


---

## 🛠️ Step 1: Configure Environment Variables

The application reads a custom greeting message from the environment. You must create a file named **`.env`** in the root directory and define the `GREETING_MESSAGE`.

### `.env` Content:

GREETING_MESSAGE="Welcome to the DevOps Lab!"


## 📝 Step 2: Create the Orchestration File
This file defines the two services, builds the custom app, sets up the network, and configures the connection between the services.

docker-compose.yml Content:
```

version: '3.8'

services:
  # 1. Define the Redis cache service
  cache:
    image: redis:alpine
    networks:
      - app-network

  # 2. Define the custom application service
  app:
    # Use the local Dockerfile for building the image
    build: ./app 
    # Map host port 8888 to the container's internal port 5000 (Flask default)
    ports:
      - "8888:5000" 
    
    # CRITICAL: This allows app.py to resolve the 'cache' service host on the network.
    environment:
      REDIS_HOST: cache 
    
    # Inject variables from the .env file (like GREETING_MESSAGE)
    env_file:
      - .env

    networks:
      - app-network

# 3. Define the custom network 
networks:
  app-network:
    driver: bridge
```
## 🏃 Step 3: Build and Run (The Validation Command)
Execute the following command to force a build of the custom image and start both services in detached mode (-d). This is the standard DevOps deployment command for a build-based service.

 

docker compose up -d --build


## ✅ Step 4: Verification
1. Check Service Status
Verify both containers are running and healthy:

 

docker compose ps
2. Test Connectivity and Configuration
Access the running application via curl to confirm it sees the custom environment variable and successfully connects to the internal Redis instance:

 

curl http://localhost:8888
Expected Success Output:
JSON

{
  "hostname": "...",
  "message": "Welcome to the DevOps Lab!",
  "redis_status": "Database is reachable!"
}
##  🛑 Clean Up
To stop and remove the containers and networks:
docker compose down
