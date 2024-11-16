```markdown
# Team Brainstorm Hub

**Team Brainstorm Hub** is a collaborative platform designed to facilitate idea submission, voting, and collective refinement among team members. Leveraging a scalable microservices architecture, it promotes creative thinking, structured feedback, and active participation within teams.

## Architecture

The application follows a microservices architecture, consisting of:

- **Frontend:** An HTML/CSS/JavaScript interface served by Nginx.
- **Idea Service:** A Flask-based REST API for managing idea submissions.
- **Voting Service:** A Flask-based REST API for handling votes.
- **PostgreSQL Database:** Stores ideas and vote counts.
- **Kubernetes:** Orchestrates container deployment, scaling, and management.

## Prerequisites

Before setting up Team Brainstorm Hub, ensure you have the following installed on your Windows 10 PC:

- **WSL (Windows Subsystem for Linux)**
- **Docker Desktop** with Kubernetes enabled
- **kubectl:** Kubernetes command-line tool
- **Docker Hub Account:** `nilsps`
- **Git:** For version control (optional but recommended)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/team-brainstorm-hub.git
cd team-brainstorm-hub
```

*Replace `yourusername` with your actual GitHub username if applicable.*

### 2. Set Up Docker Hub

Ensure you're logged in to Docker Hub and have the necessary repositories created:

- `nilsps/idea-service`
- `nilsps/voting-service`
- `nilsps/frontend`

### 3. Build and Push Docker Images

#### a. Idea Service

```bash
cd idea_service
docker build -t nilsps/idea-service:latest .
docker push nilsps/idea-service:latest
```

#### b. Voting Service

```bash
cd ../voting_service
docker build -t nilsps/voting-service:latest .
docker push nilsps/voting-service:latest
```

#### c. Frontend

```bash
cd ../frontend
docker build -t nilsps/frontend:latest .
docker push nilsps/frontend:latest
```

### 4. Deploy to Kubernetes

Navigate to the Kubernetes configuration directory and apply the manifests:

```bash
cd ../kubernetes
kubectl apply -f postgres-pvc.yaml
kubectl apply -f postgres-deployment.yaml
kubectl apply -f postgres-service.yaml

kubectl apply -f idea-service-deployment.yaml
kubectl apply -f idea-service-service.yaml

kubectl apply -f voting-service-deployment.yaml
kubectl apply -f voting-service-service.yaml

kubectl apply -f frontend-deployment.yaml
kubectl apply -f frontend-service.yaml

kubectl apply -f init-configmap.yaml
kubectl apply -f init-job.yaml
```

*Note: Ensure that all services are updated with the latest Docker images.*

## Usage

### Access the Frontend

Open your web browser and navigate to [http://localhost:80](http://localhost:80) or [http://localhost:30783](http://localhost:30783).

### Submit an Idea

1. Fill in the "Title" and "Description" fields.
2. Click the "Submit Idea" button.
3. The idea will appear in the "Ideas" section.

### Vote for an Idea

1. Click the "Vote" button next to an idea.
2. The vote count will increment accordingly.

### Real-time Updates

Open the application in multiple browser windows to see real-time synchronization of ideas and votes.

## Technologies Used

- **Frontend:** HTML, CSS, JavaScript, Nginx
- **Backend:** Python, Flask, Flask-RESTful, Flask-CORS
- **Database:** PostgreSQL
- **Containerization:** Docker
- **Orchestration:** Kubernetes
- **Version Control:** Git
- **Cloud:** Docker Hub
```