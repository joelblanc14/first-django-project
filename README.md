# 🧩 Django Monitoring & Logging Stack

A **containerized Django application** with a **full observability stack** for metrics, logs, and dashboards — built with **Prometheus**, **Grafana**, **Loki**, and **Promtail**, integrated with **AWS S3** for long-term log storage.

## ⚙️ Architecture Overview

```
                ┌────────────────────────┐
                │      Grafana UI        │
                │  (Dashboards & Alerts) │
                └──────────┬─────────────┘
                           │
                 ┌─────────┴──────────┐
                 │   Prometheus        │
                 │ (Metrics Scraper)   │
                 └─────────┬──────────┘
                           │
 ┌───────────────────┐     │     ┌───────────────────┐
 │   Django App      │─────┤────▶│   Node Exporter   │
 │  (w/ Prometheus   │     │     │   + cAdvisor      │
 │   metrics /metrics│     │     │   (System metrics)│
 └───────────────────┘     │     └───────────────────┘
                           │
                 ┌─────────┴──────────┐
                 │       Loki         │
                 │ (Central Log Store)│
                 └─────────┬──────────┘
                           │
                      ┌────┴────┐
                      │Promtail │
                      │(Log shipper)
                      └────┬────┘
                           │
                    ┌──────┴────────┐
                    │ AWS S3 Bucket │
                    │ useit.loki-playground │
                    └────────────────┘

```


## 🚀 Features
* **Django REST API** with custom JWT middleware and Prometheus instrumentation.

* **Prometheus** scrapes Django metrics `(/metrics)`, Node, and Docker container stats.

* **Loki** + **Promtail** aggregate application logs from the Django container.

* **Grafana** dashboards visualize both **metrics** and **logs**.

* **AWS S3** used as Loki’s object store backend for log persistence.

* Fully reproducible **Docker Compose environment**.

## 🐳 Containers Overview

| Service           | Description                                                   |
| ----------------- | ------------------------------------------------------------- |
| **web**           | Django app (API + Prometheus metrics + custom JWT middleware) |
| **db**            | PostgreSQL 15 database                                        |
| **prometheus**    | Scrapes metrics from Django, Node Exporter, cAdvisor, Loki    |
| **grafana**       | Dashboards and alerts (Port `3000`)                           |
| **loki**          | Centralized log aggregation backend (Port `3100`)             |
| **promtail**      | Collects Django logs from `/app/logs` and sends them to Loki  |
| **node-exporter** | Exposes host-level system metrics                             |
| **cadvisor**      | Exposes container-level performance metrics                   |

## 🧱 Stack Configuration Details

### 📝 Django

* REST Framework + JWT middleware for token auth

* Prometheus middleware: `/metrics` endpoint for scraping

* Logging to file: `logs/blog.log`

* Database:

  * **SQLite** in development mode

  * **PostgreSQL** in production (when `DJANGO_DEBUG=False`)

### 📊 Prometheus

Located at: `monitoring/prometheus.yml`

Scrapes metrics from:

* Django app → `web:8000/metrics`

* Loki → `loki:3100`

* Node Exporter → `node-exporter:9100`

* cAdvisor → `cadvisor:8080`

* Itself → `prometheus:9090`

Data retention: **60s (configurable)**

### 📈 Grafana

* Runs on port `3000`

* Default credentials:

  * User: `admin`

  * Password: `admin`

* Dashboards can visualize both **Prometheus** metrics and **Loki** logs.


### 📦 Loki

Configured in `monitoring/loki-config.yaml`:

* `auth_enabled: false`

* Writes indexes and chunks to AWS S3 (`useit.loki-playground`)

* Uses **TSDB schema v13**

* Persistent volume: `/var/lib/loki`

If local Docker volumes are deleted, Loki will **restore data automatically** from S3.

### 📜 Promtail

Configured in monitoring/promtail-config.yaml:

* Reads all logs from:

```bash
/app/logs/*.log
```
* Pushes them to Loki at:

```bash
http://loki:3100/loki/api/v1/push
```

### ☁️ AWS S3 Integration

Loki stores logs in S3 for persistence:

* Bucket: `useit.loki-playground`

* Credentials are read from `.env`
  
Files inside the bucket:

* `index_...` → Loki indexes (mapping metadata)

* `fake/` → example logs

* `loki_cluster_seed.json` → internal cluster metadata


## 🧩 Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone https://github.com/joelblanc14/first-django-project
cd first-django-project
```

### 2️⃣ Configure environment variables

Create a `.env` file:

```bash
POSTGRES_DB=yourdb
POSTGRES_USER=youruser
POSTGRES_PASSWORD=yourpassword
AWS_REGION=your_region
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
DJANGO_DEBUG=False
```

### 3️⃣ Build and start containers

```bash
docker compose up -d --build
```

### 4️⃣ Run Django migrations

```bash
docker exec -it django_app python manage.py migrate
```

### 5️⃣ Access the services

| Service       | URL                                            |
| ------------- | ---------------------------------------------- |
| Django API    | [http://localhost:8000](http://localhost:8000) |
| Prometheus    | [http://localhost:9090](http://localhost:9090) |
| Grafana       | [http://localhost:3000](http://localhost:3000) |
| Loki API      | [http://localhost:3100](http://localhost:3100) |
| cAdvisor      | [http://localhost:8080](http://localhost:8080) |
| Node Exporter | [http://localhost:9100](http://localhost:9100) |


## 🧠 How It Works

1. Django writes logs to /app/logs/blog.log.

2. Promtail tails this file and pushes entries to Loki.

3. Loki stores the logs in S3 for persistence.

4. Prometheus scrapes metrics from Django, Node Exporter, and cAdvisor.

5. Grafana unifies everything into dashboards and log panels.