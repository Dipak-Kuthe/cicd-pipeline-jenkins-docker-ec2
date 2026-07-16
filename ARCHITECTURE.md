# Architecture — CI/CD Pipeline (GitHub, Jenkins, Docker, EC2)

Automated pipeline: every push to GitHub triggers Jenkins to build, test, containerize and deploy to EC2.

```mermaid
flowchart LR
    DEV[Developer] -->|git push| GH[GitHub]
    GH -->|webhook| JEN[Jenkins Pipeline]
    JEN --> B[Build]
    B --> T[Test]
    T --> D[Docker Build]
    D --> R[(Docker Registry)]
    R --> DEP[Deploy to EC2]
    DEP --> APP[Container :5000 - Flask + Gunicorn]
```

## How it works

- A developer pushes code to GitHub which fires a webhook to Jenkins.
- Jenkins runs the declarative pipeline stages: build, test, then build a Docker image.
- The image is pushed to a container registry.
- Jenkins deploys the container to an Amazon EC2 host, serving the app on port 5000.
