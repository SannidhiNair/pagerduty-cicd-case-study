from fastapi import FastAPI
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time
import random

app = FastAPI(title="PD‑App")

# Prometheus metrics
HTTP_COUNTER = Counter("http_requests_total", "Total HTTP requests", ["path"])
LATENCY = Histogram("request_latency_seconds", "Request latency", ["path"])

@app.get("/health")
def health():
    HTTP_COUNTER.labels("/health").inc()
    return {"status": "ok"}

@app.get("/random")
def random_delay():
    start = time.time()
    delay = random.random()   # 0–1 seconds
    time.sleep(delay)
    LATENCY.labels("/random").observe(time.time() - start)
    HTTP_COUNTER.labels("/random").inc()
    return {"slept": delay}

@app.get("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

@app.get("/")
def root():
    return {"msg": "PD‑App is running. Try /health, /random, /docs"}
