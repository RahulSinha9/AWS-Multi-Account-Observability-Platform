# AWS Multi-Account Observability Platform

Production-oriented observability foundation for AWS workloads across multiple accounts and regions.

## Included

- FastAPI demo service with Prometheus metrics
- SLO, error-budget and burn-rate calculations
- OpenTelemetry Collector configuration
- Cross-account AWS read-only IAM role via Terraform
- Kubernetes manifests with HPA, PDB, NetworkPolicy and hardened security context
- Helm chart
- Docker and Docker Compose
- GitHub Actions CI with tests, Helm validation, Terraform validation, Trivy and container build

## Architecture

```text
AWS Accounts / Regions
        |
        +--> CloudWatch Metrics / Logs
        +--> Application OTLP
        |
        v
Central Observability Account
        |
   OpenTelemetry Collector
        |
   Prometheus / AMP
        |
      Grafana
        |
   SLO / Alerting
```

## Local run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Run tests:

```bash
pytest -q
```

Endpoints:

- `GET /health`
- `GET /metrics`
- `GET /slo`

## Docker

```bash
docker compose up --build
```

## Kubernetes

```bash
kubectl apply -f k8s/
```

The workload runs as non-root, uses a read-only filesystem, drops Linux capabilities, uses RuntimeDefault seccomp, and includes probes, HPA, PDB and NetworkPolicy.

## Helm

```bash
helm lint helm/observability-demo
helm template observability-demo helm/observability-demo
helm install observability-demo helm/observability-demo
```

## Terraform

```bash
cd terraform
terraform init
terraform fmt -check
terraform validate
terraform plan -var='observability_account_id=123456789012'
```

The IAM role is intentionally read-only for CloudWatch, Logs, EC2 and ECS metadata and does not grant operational mutation actions.

## Repository structure

```text
app/                 FastAPI service, metrics and SLO logic
config/              SLO configuration
otel/                OpenTelemetry Collector config
demo/                Dashboard definition
k8s/                 Kubernetes manifests
helm/                Helm chart
terraform/           Cross-account IAM foundation
tests/               Automated tests
.github/workflows/   CI pipeline
```

## Production roadmap

- Amazon Managed Service for Prometheus
- Amazon Managed Grafana
- CloudWatch cross-account observability
- Tempo/Jaeger or AWS-native tracing backend
- Loki/OpenSearch logging
- Alertmanager/PagerDuty routing
- AWS Organizations account discovery
- SLO burn-rate alerting
- Synthetic monitoring and retention/cost controls

## Resume bullet

> Built a multi-account AWS observability platform using OpenTelemetry, Prometheus-compatible metrics, SLO/error-budget calculations, Kubernetes, Terraform and Docker; designed cross-account read roles and production-grade telemetry collection with CI security validation.

MIT License.
