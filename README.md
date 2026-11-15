# VLE-8: Blue-Green Deployment using DevOps Tools

## Objective

To implement Blue-Green Deployment using Docker, Jenkins,
Kubernetes, Terraform, Ansible, GitHub and Prometheus.

## Tools Used

- Git and GitHub
- Docker and Docker Hub
- Jenkins
- Kubernetes (K3s)
- Terraform
- Ansible
- Prometheus
- Grafana
- AWS EC2

## Architecture

GitHub -> Jenkins -> Docker Build -> Docker Hub
-> Kubernetes Blue/Green Deployments -> Kubernetes Service

## Deployment Strategy

Two independent Kubernetes Deployments are maintained:

- Blue: Current stable application version
- Green: New application version

The Kubernetes Service selects one environment at a time.
Traffic is switched by changing the Service selector.

## Application Endpoints

- `/` - Application interface
- `/version` - Deployment environment and version
- `/health` - Health check
- `/metrics` - Prometheus metrics

## Kubernetes Namespace

`vle8`

## Application Service

NodePort: `30082`

## Rollback

Change the Service selector from green to blue
to restore traffic to the previous stable version.