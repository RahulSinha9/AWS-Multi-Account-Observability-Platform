# AWS Multi-Account Observability Platform ☁️📊

> A production-oriented centralized observability platform for monitoring AWS workloads across multiple accounts and regions using **OpenTelemetry, Prometheus-compatible metrics, SLOs, Kubernetes, Terraform, Docker, and GitHub Actions**.

![AWS](https://img.shields.io/badge/AWS-Cloud-orange)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Production-green)
![OpenTelemetry](https://img.shields.io/badge/OpenTelemetry-OTel-purple)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Ready-326CE5)
![Terraform](https://img.shields.io/badge/Terraform-IaC-7B42BC)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED)
![CI](https://img.shields.io/badge/CI-GitHub%20Actions-black)

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Problem Statement](#-problem-statement)
- [Solution](#-solution)
- [Architecture](#-architecture)
- [Key Components](#-key-components)
- [Observability Model](#-observability-model)
- [SLO and Error Budget](#-slo-and-error-budget)
- [Multi-Account AWS Design](#-multi-account-aws-design)
- [Security Design](#-security-design)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Local Development](#-local-development)
- [API Endpoints](#-api-endpoints)
- [Prometheus Metrics](#-prometheus-metrics)
- [Docker Deployment](#-docker-deployment)
- [Kubernetes Deployment](#-kubernetes-deployment)
- [Helm Deployment](#-helm-deployment)
- [Terraform Deployment](#-terraform-deployment)
- [OpenTelemetry](#-opentelemetry)
- [CI/CD Pipeline](#-cicd-pipeline)
- [Testing](#-testing)
- [Security Scanning](#-security-scanning)
- [Operational Workflow](#-operational-workflow)
- [Production Architecture](#-production-architecture)
- [Troubleshooting](#-troubleshooting)
- [Future Enhancements](#-future-enhancements)
- [Resume Description](#-resume-description)
- [Learning Outcomes](#-learning-outcomes)
- [License](#-license)

---

# 🎯 Overview

Modern organizations rarely run everything inside a single AWS account.

A typical enterprise environment may contain:

- Development account
- QA/Staging account
- Production account
- Security account
- Shared-services account
- Central observability account
- Multiple AWS regions

When infrastructure grows, monitoring becomes difficult because metrics, logs, traces, alarms, and application telemetry are distributed across accounts and regions.

This project demonstrates how to build a **centralized observability platform** that provides a common monitoring architecture while keeping workload accounts isolated.

The platform combines:

- **AWS CloudWatch**
- **OpenTelemetry**
- **Prometheus-compatible metrics**
- **SLOs**
- **Error budgets**
- **Kubernetes**
- **Helm**
- **Terraform**
- **Docker**
- **GitHub Actions**
- **Trivy**

---

# 🚨 Problem Statement

Without centralized observability, DevOps teams often face problems such as:

### 1. Distributed monitoring

Every AWS account may have its own:

- CloudWatch metrics
- CloudWatch Logs
- Alarms
- Dashboards
- Application logs

Engineers have to switch between multiple accounts and regions during incidents.

### 2. No common SLO model

A service may be technically "up" while still violating its reliability objective.

For example:

```text
Target availability = 99.9%
Actual availability = 99.5%
```

The infrastructure may look healthy, but the service has already consumed its reliability budget.

### 3. High operational blast radius

A monitoring system should normally observe infrastructure without having unnecessary permissions to modify production resources.

### 4. Inconsistent telemetry

Different teams may expose different metric names, logging formats, and monitoring patterns.

### 5. Difficult incident investigation

During an incident, engineers need a single view of:

```text
Metrics + Logs + Traces + SLO + Infrastructure Health
```

---

# 💡 Solution

This project introduces a **Central Observability Account**.

Workload accounts expose telemetry to the central platform using controlled cross-account access.

High-level flow:

```text
                  AWS Organization
                         |
          +--------------+--------------+
          |              |              |
         DEV          STAGING          PROD
          |              |              |
     CloudWatch      CloudWatch      CloudWatch
     Logs/Metrics    Logs/Metrics    Logs/Metrics
          |              |              |
          +--------------+--------------+
                         |
                  Cross Account Role
                         |
                         v
             Central Observability Account
                         |
               OpenTelemetry Collector
                         |
              +----------+----------+
              |                     |
          Prometheus              Logs
              |
          Grafana / AMP
              |
         SLO & Alerting
```

---

# 🏗️ Architecture

## Logical Architecture

```text
+---------------------------------------------------------------+
|                    AWS Organization                           |
+---------------------------------------------------------------+
       |                    |                    |
       v                    v                    v
+-------------+      +-------------+      +-------------+
| DEV Account |      | QA Account  |      | PROD Account|
+-------------+      +-------------+      +-------------+
| EC2/ECS/EKS |      | EC2/ECS/EKS |      | EC2/ECS/EKS |
| CloudWatch  |      | CloudWatch  |      | CloudWatch  |
+------+------+      +------+------+      +------+------+
       |                    |                    |
       +--------------------+--------------------+
                            |
                     AssumeRole / Telemetry
                            |
                            v
              +-----------------------------+
              | Central Observability       |
              | Account                     |
              +-----------------------------+
                            |
                 +----------+----------+
                 |                     |
                 v                     v
       OpenTelemetry Collector    CloudWatch
                 |
        +--------+---------+
        |                  |
        v                  v
   Prometheus/AMP       Trace Backend
        |
        v
      Grafana
        |
        v
 Alerts / SLO / On-call
```

---

# 🧩 Key Components

| Component | Purpose |
|---|---|
| FastAPI | Demo application and telemetry endpoint |
| Prometheus Client | Application metrics |
| OpenTelemetry | Standard telemetry collection |
| CloudWatch | AWS infrastructure metrics/logs |
| Terraform | AWS IAM infrastructure as code |
| Kubernetes | Container orchestration |
| Helm | Kubernetes packaging |
| Docker | Application containerization |
| GitHub Actions | CI automation |
| Trivy | Security scanning |
| SLO Engine | Availability/error-budget calculations |

---

# 📊 Observability Model

The project follows the three major observability signals:

## Metrics

Metrics answer:

> "What is happening?"

Examples:

- Request rate
- Error rate
- CPU utilization
- Memory utilization
- Latency
- Availability

---

## Logs

Logs answer:

> "What happened?"

Examples:

```text
Application error
Authentication failure
Database connection failure
Deployment failure
Infrastructure event
```

---

## Traces

Traces answer:

> "Where did the request spend time?"

Example:

```text
Client
  |
  v
ALB
  |
  v
API
  |
  +--> Redis
  |
  +--> PostgreSQL
  |
  +--> External API
```

OpenTelemetry provides a common framework for collecting these signals.

---

# 🎯 SLO and Error Budget

The application exposes an SLO endpoint.

Availability is calculated as:

```text
Availability =
Successful Requests / Total Requests
```

For a 99.9% SLO:

```text
SLO Target = 99.9%
Allowed Error = 0.1%
```

Therefore:

```text
Error Budget = 1 - SLO Target
             = 1 - 0.999
             = 0.001
             = 0.1%
```

## Example

Suppose:

```text
Total requests      = 100,000
Successful requests = 99,950
Failed requests     = 50
```

Then:

```text
Availability = 99,950 / 100,000
             = 99.95%
```

The service is above the 99.9% objective.

---

# 🔥 Burn Rate

Burn rate tells us how quickly the service is consuming its error budget.

```text
Burn Rate =
Observed Error Rate / Allowed Error Rate
```

For example:

```text
SLO          = 99.9%
Allowed      = 0.1%
Observed     = 0.2%

Burn Rate = 0.2 / 0.1
          = 2x
```

A high burn rate can be used to trigger an alert before the entire error budget is exhausted.

---

# 🌎 Multi-Account AWS Design

The platform uses a **central observability account**.

Example:

```text
                 AWS Organization
                       |
        +--------------+--------------+
        |              |              |
       DEV          STAGING          PROD
    Account A       Account B       Account C
        |              |              |
        +--------------+--------------+
                       |
                 AssumeRole
                       |
                       v
             Observability Account
```

Each workload account can contain a dedicated IAM role.

The central account assumes that role to retrieve monitoring information.

## Why cross-account IAM?

Benefits:

- Centralized monitoring
- Least privilege
- Account isolation
- Easier auditing
- Reduced operational complexity
- No long-lived credentials

---

# 🔐 Security Design

Security is one of the main design principles of this project.

## IAM Least Privilege

The Terraform role provides monitoring-oriented permissions such as:

```text
cloudwatch:DescribeAlarms
cloudwatch:GetMetricData
cloudwatch:ListMetrics
logs:DescribeLogGroups
logs:DescribeLogStreams
logs:FilterLogEvents
ec2:DescribeInstances
ecs:DescribeServices
ecs:DescribeTasks
ecs:ListClusters
```

The role does **not** provide destructive operations such as:

```text
ec2:TerminateInstances
ec2:StopInstances
ecs:UpdateService
ssm:SendCommand
autoscaling:SetDesiredCapacity
```

This keeps the monitoring plane separate from the remediation plane.

---

# 🛡️ Kubernetes Security

The Kubernetes workload includes:

- Non-root container
- Read-only root filesystem
- Dropped Linux capabilities
- RuntimeDefault seccomp profile
- Disabled service-account token automounting
- Resource requests
- Resource limits
- Readiness probe
- Liveness probe
- PodDisruptionBudget
- NetworkPolicy
- HorizontalPodAutoscaler

Example:

```yaml
securityContext:
  runAsNonRoot: true
  allowPrivilegeEscalation: false
  readOnlyRootFilesystem: true
  capabilities:
    drop:
      - ALL
```

---

# 📁 Project Structure

```text
AWS-Multi-Account-Observability-Platform/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   ├── metrics.py
│   └── slo.py
│
├── config/
│   └── slos.yaml
│
├── demo/
│   └── dashboard.json
│
├── otel/
│   └── collector.yaml
│
├── tests/
│   ├── test_api.py
│   └── test_slo.py
│
├── k8s/
│   ├── deployment.yaml
│   ├── hpa.yaml
│   ├── namespace.yaml
│   ├── networkpolicy.yaml
│   ├── pdb.yaml
│   ├── service.yaml
│   └── serviceaccount.yaml
│
├── helm/
│   └── observability-demo/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
│
├── terraform/
│   ├── main.tf
│   ├── outputs.tf
│   ├── variables.tf
│   ├── versions.tf
│   └── README.md
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── requirements.txt
├── .env.example
└── README.md
```

---

# ⚙️ Prerequisites

Install the following tools:

- Python 3.12+
- Docker
- Docker Compose
- Kubernetes CLI
- Helm
- Terraform
- Git
- AWS CLI

Verify:

```bash
python3 --version
docker --version
kubectl version --client
helm version
terraform version
aws --version
git --version
```

---

# 🚀 Local Development

## 1. Clone repository

```bash
git clone https://github.com/RahulSinha9/AWS-Multi-Account-Observability-Platform.git
cd AWS-Multi-Account-Observability-Platform
```

## 2. Create virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:

```powershell
.venv\Scripts\activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Start application

```uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Application:

```text
http://localhost:8000
```

---

# 🔌 API Endpoints

## Health

```http
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

---

## SLO

```http
GET /slo
```

Example:

```json
{
  "target": 0.999,
  "availability": 1.0,
  "error_budget": 0.001,
  "total_requests": 10
}
```

---

## Metrics

```http
GET /metrics
```

Returns Prometheus-compatible metrics.

---

# 📈 Prometheus Metrics

The application exposes:

### HTTP request counter

```text
http_requests_total
```

Labels:

```text
method
path
status
```

### HTTP latency histogram

```text
http_request_duration_seconds
```

Labels:

```text
method
path
```

These metrics can be scraped by Prometheus or exported through the OpenTelemetry pipeline.

---

# 🐳 Docker Deployment

Build:

```bash
docker build -t aws-observability-demo:latest .
```

Run:

```bash
docker run --rm -p 8000:8000 aws-observability-demo:latest
```

Or use Compose:

```bash
docker compose up --build
```

Stop:

```bash
docker compose down
```

---

# ☸️ Kubernetes Deployment

Apply all Kubernetes resources:

```bash
kubectl apply -f k8s/
```

Verify:

```bash
kubectl get all -n observability-demo
```

Check pods:

```bash
kubectl get pods -n observability-demo
```

Check service:

```bash
kubectl get svc -n observability-demo
```

Check HPA:

```bash
kubectl get hpa -n observability-demo
```

Check PDB:

```bash
kubectl get pdb -n observability-demo
```

---

# 📦 Helm Deployment

Lint the chart:

```bash
helm lint helm/observability-demo
```

Render templates:

```bash
helm template observability-demo helm/observability-demo
```

Install:

```bash
helm install observability-demo helm/observability-demo
```

Upgrade:

```bash
helm upgrade observability-demo helm/observability-demo
```

Check:

```bash
helm list
kubectl get all
```

---

# 🏗️ Terraform Deployment

Move into Terraform directory:

```bash
cd terraform
```

Initialize:

```bash
terraform init
```

Format:

```bash
terraform fmt
```

Validate:

```bash
terraform validate
```

Create a plan:

```bash
terraform plan \
  -var="observability_account_id=123456789012"
```

Apply:

```bash
terraform apply \
  -var="observability_account_id=123456789012"
```

Get role ARN:

```bash
terraform output role_arn
```

---

# 🔭 OpenTelemetry

The OpenTelemetry Collector is configured to receive OTLP telemetry.

## OTLP gRPC

```text
0.0.0.0:4317
```

## OTLP HTTP

```text
0.0.0.0:4318
```

The collector pipeline contains:

```text
Receiver
   |
   v
Processor
   |
   v
Exporter
```

Current pipelines:

```text
Traces --> OTLP --> Batch --> Debug
Metrics --> OTLP --> Batch --> Prometheus
Logs --> OTLP --> Batch --> Debug
```

In a production deployment, the debug exporters can be replaced with managed or durable telemetry backends.

---

# 🔄 CI/CD Pipeline

GitHub Actions validates every push and pull request.

Pipeline:

```text
Git Push / Pull Request
          |
          v
     GitHub Actions
          |
   +------+-------+--------+---------+
   |              |        |         |
 Tests          Helm   Terraform   Security
   |              |        |         |
   +--------------+--------+---------+
                  |
             Docker Build
```

## CI stages

### Python

- Install dependencies
- Run pytest
- Compile Python source

### Helm

- Helm lint
- Helm template

### Terraform

- Terraform format check
- Terraform initialization
- Terraform validation

### Security

Trivy performs filesystem vulnerability scanning.

### Container

Docker image is built to verify container reproducibility.

---

# 🧪 Testing

Run all tests:

```bash
pytest -q
```

Run a specific test:

```pytest tests/test_slo.py -q
```

Run compilation:

```bash
python -m compileall app tests
```

The tests cover:

- Health endpoint
- SLO endpoint
- Prometheus metrics endpoint
- Availability calculation
- Error budget calculation
- Burn-rate calculation
- Invalid request-count handling

---

# 🔐 Security Scanning

The CI pipeline uses **Trivy** to identify HIGH and CRITICAL filesystem vulnerabilities.

Example local scan:

```bash
trivy fs --severity HIGH,CRITICAL .
```

Container scan:

```bash
trivy image aws-observability-demo:latest
```

---

# 🧭 Operational Workflow

A typical production incident can follow this workflow:

```text
Alert
  |
  v
Check SLO
  |
  v
Check Error Budget
  |
  v
Check Request/Error Rate
  |
  v
Check Latency
  |
  v
Check Application Logs
  |
  v
Check Distributed Trace
  |
  v
Identify Infrastructure Dependency
  |
  v
Remediate
  |
  v
Verify SLO Recovery
```

The goal is to move from:

```text
"I think the application is down"
```

to:

```text
"The API's 5-minute error rate increased to X%, the SLO burn rate is Yx, and traces show the latency increase originates from the database dependency."
```

---

# 🏢 Production Architecture

A larger production implementation can look like:

```text
                           AWS Organization
                                  |
          +-----------------------+-----------------------+
          |                       |                       |
       Dev Account           Staging Account          Prod Account
          |                       |                       |
      CloudWatch              CloudWatch              CloudWatch
      Logs/Metrics             Logs/Metrics            Logs/Metrics
          |                       |                       |
          +-----------------------+-----------------------+
                                  |
                         Cross Account IAM
                                  |
                                  v
                  +-------------------------------+
                  | Central Observability Account  |
                  +-------------------------------+
                                  |
                         OpenTelemetry
                            Collector
                                  |
              +-------------------+-------------------+
              |                   |                   |
              v                   v                   v
          Metrics              Logs                Traces
              |                   |                   |
              v                   v                   v
        Prometheus/AMP      OpenSearch/Loki       Tempo/Jaeger
              |                   |                   |
              +-------------------+-------------------+
                                  |
                                Grafana
                                  |
                           Alerting / On-call
```

---

# 📊 Recommended Production Dashboards

A production Grafana dashboard should include:

## Golden Signals

### Latency

```text
P50
P95
P99
```

### Traffic

```text
Requests/sec
Requests/min
```

### Errors

```text
4xx rate
5xx rate
Error percentage
```

### Saturation

```text
CPU
Memory
Connection pools
Queue depth
Disk
```

---

# 🚨 Recommended Alerts

Examples:

### High Error Rate

```text
5xx > 5% for 5 minutes
```

### High Latency

```text
P95 latency > 500ms
```

### SLO Burn Rate

```text
Burn rate > 2x
```

### Availability

```text
Availability < 99.9%
```

### Infrastructure

```text
CPU > 80%
Memory > 80%
Disk > 80%
Unhealthy targets > 0
```

---

# 💰 Cost Optimization Considerations

Centralized observability can become expensive if telemetry is not managed correctly.

Recommended practices:

- Define log retention periods
- Avoid unnecessary DEBUG logging in production
- Sample distributed traces
- Aggregate high-cardinality metrics carefully
- Use lifecycle policies
- Monitor CloudWatch ingestion costs
- Monitor Prometheus series count
- Compress long-term logs
- Separate hot and cold telemetry storage

Observability itself should be observable.

---

# 🛠️ Troubleshooting

## Application does not start

Check:

```bash
python --version
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## Kubernetes pod is not ready

Check:

```bash
kubectl describe pod -n observability-demo <pod-name>
kubectl logs -n observability-demo <pod-name>
```

---

## HPA has no metrics

Check:

```bash
kubectl get hpa -n observability-demo
kubectl top pods -n observability-demo
```

Make sure Metrics Server is available.

---

## Terraform fails validation

Run:

```bash
terraform fmt -check
terraform validate
terraform providers
```

---

## Cross-account AssumeRole fails

Verify:

1. Trust policy
2. Observability account ID
3. AWS account ID
4. IAM permissions
5. STS access
6. Active AWS credentials

Test:

```bash
aws sts get-caller-identity
```

---

# 🚀 Future Enhancements

The current repository is a foundation. The following enhancements can turn it into a full enterprise platform.

## Phase 1 — Managed AWS Observability

- Amazon Managed Service for Prometheus
- Amazon Managed Grafana
- CloudWatch cross-account observability
- CloudWatch cross-region dashboards

## Phase 2 — Advanced Telemetry

- Distributed tracing
- Trace sampling
- OpenTelemetry auto-instrumentation
- Log correlation
- Trace-to-log correlation

## Phase 3 — Intelligent Operations

- AI-based anomaly detection
- Incident summarization
- Root-cause analysis
- Automated runbook recommendations
- ChatOps integration

## Phase 4 — Enterprise Governance

- AWS Organizations account discovery
- Automated account onboarding
- Standardized IAM roles
- Centralized alert policies
- Compliance dashboards
- Observability cost governance

---

# 🧠 DevOps Concepts Demonstrated

This project demonstrates practical knowledge of:

### AWS

- IAM
- STS
- CloudWatch
- EC2
- ECS
- Multi-account architecture
- Cross-account access
- Least privilege

### Observability

- Metrics
- Logs
- Traces
- OpenTelemetry
- Prometheus
- SLO
- Error budgets
- Burn rate
- Golden signals

### Kubernetes

- Deployment
- Service
- HPA
- PDB
- NetworkPolicy
- ServiceAccount
- SecurityContext
- Health probes

### Infrastructure as Code

- Terraform
- IAM policy documents
- Reusable variables
- Outputs
- Validation

### DevOps

- Docker
- Helm
- Git
- GitHub Actions
- CI
- Security scanning
- Automated testing

---

# 💼 Resume Description

### Short version

> Built a centralized multi-account AWS observability platform using OpenTelemetry, Prometheus-compatible metrics, SLO/error-budget monitoring, Terraform, Kubernetes, Helm and Docker, with cross-account least-privilege IAM and automated CI/security validation.

### Detailed version

> Designed and implemented a production-oriented AWS multi-account observability platform that centralizes application and infrastructure telemetry using OpenTelemetry and Prometheus-compatible metrics. Implemented cross-account read-only IAM roles with Terraform, SLO/error-budget calculations, Kubernetes workloads with HPA/PDB/NetworkPolicy, Helm packaging, Docker containerization, automated testing and GitHub Actions security validation using Trivy.

---

# 🎤 Interview Talking Points

You can explain this project in an interview using the following flow:

### 1. Why did you build it?

> As environments scale across multiple AWS accounts, monitoring becomes fragmented. I designed a centralized observability architecture to provide a common monitoring model while maintaining account isolation.

### 2. Why OpenTelemetry?

> OpenTelemetry provides a vendor-neutral standard for collecting metrics, logs and traces, which reduces dependency on a single observability backend.

### 3. Why cross-account IAM?

> The central monitoring account needs visibility into workload accounts, but it should not have unrestricted administrative access. I used cross-account IAM roles with least-privilege read permissions.

### 4. Why SLOs?

> Infrastructure health alone doesn't represent user experience. SLOs let us measure reliability from a service perspective and calculate the available error budget.

### 5. How would you scale it?

> I would integrate AWS Organizations for account discovery, Amazon Managed Service for Prometheus and Grafana for managed storage and visualization, add distributed tracing and centralized logs, and implement multi-window burn-rate alerting.

---

# 📚 Learning Outcomes

After implementing this project, you should understand:

- How centralized observability works
- AWS multi-account monitoring architecture
- Cross-account IAM
- OpenTelemetry architecture
- Prometheus metrics
- SLO and error-budget concepts
- Kubernetes production security
- Helm packaging
- Terraform IAM automation
- Docker containerization
- CI/CD validation
- Vulnerability scanning
- Incident investigation workflows
- Observability cost management

---

# ⭐ Project Highlights

```text
✓ Multi-account AWS architecture
✓ Cross-account IAM
✓ OpenTelemetry
✓ Prometheus metrics
✓ SLO monitoring
✓ Error budgets
✓ Burn-rate calculations
✓ Kubernetes
✓ Helm
✓ Terraform
✓ Docker
✓ GitHub Actions
✓ Trivy security scanning
✓ Automated tests
✓ Production security controls
✓ Incident investigation workflow
```

---

# 📄 License

This project is released under the **MIT License**.

---

## 👨‍💻 Author

**Rahul Kumar**

GitHub: https://github.com/RahulSinha9

---

⭐ If you find this project useful, consider giving the repository a star.
