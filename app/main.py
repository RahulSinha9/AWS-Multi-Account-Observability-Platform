import time
from fastapi import FastAPI, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from .config import settings
from .metrics import REQUESTS, LATENCY
from .slo import availability, error_budget

app = FastAPI(title="AWS Multi-Account Observability Demo", version="1.0.0")
_state = {"successful": 0, "total": 0}

@app.middleware("http")
async def metrics_middleware(request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    elapsed = time.perf_counter() - start
    REQUESTS.labels(request.method, request.url.path, response.status_code).inc()
    LATENCY.labels(request.method, request.url.path).observe(elapsed)
    _state["total"] += 1
    if response.status_code < 500:
        _state["successful"] += 1
    return response

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/slo")
def slo():
    return {"target": settings.slo_target, "availability": availability(_state["successful"], _state["total"]), "error_budget": error_budget(settings.slo_target), "total_requests": _state["total"]}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
