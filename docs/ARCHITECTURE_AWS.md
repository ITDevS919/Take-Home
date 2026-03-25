# AWS Architecture Design

## Overview

A scalable multi-tenant ingestion + search platform designed to handle:

- 5,000 tenants
- 50M customers
- 200M cases
- Near real-time search (<10 min freshness)
- 300–1000 QPS

---

## High-Level Architecture

Client → API Gateway → Ingest/Search Service → Data Pipeline → Storage/Search

---

## Components

### API Layer
- AWS API Gateway
- ECS Fargate (FastAPI service)

### Data Source
- Amazon RDS PostgreSQL (primary system)

### Ingestion / CDC
- AWS DMS or Debezium (CDC)
- Kafka (MSK) or Kinesis

### Processing
- Lambda or ECS consumers
- Transform + write to lake

### Data Lake
- Amazon S3
- Partitioned by tenant/date
- Versioned + lifecycle policies

### Search
- Amazon OpenSearch
- Indexed fields: title, description

### State / Checkpoint
- DynamoDB (per-tenant checkpoint tracking)

### Events
- EventBridge or SQS

### Observability
- CloudWatch Logs + Metrics
- X-Ray tracing

---

## Reliability

- Multi-AZ RDS
- S3 durability
- Retry + DLQ for ingestion
- Idempotent processing

---

## Scaling

- ECS auto-scaling
- OpenSearch shard scaling
- Kafka partition scaling

---

## Security

- IAM least privilege
- VPC isolation
- KMS encryption (S3, RDS, OpenSearch)
- TLS everywhere
- Audit logs

---

## Recovery

- RPO ≤ 5 min via CDC replay
- RTO ≤ 30 min via auto-recovery
- S3 versioning for data recovery

---

## Cost Drivers

1. OpenSearch clusters
2. S3 storage + requests
3. Compute (ECS / Lambda)

---

## Cost Optimization

- Data lifecycle policies
- Tiered storage (S3 Glacier)
- Reduce indexing frequency
- Compress JSONL

---

## Tradeoffs

| Choice | Tradeoff |
|-------|---------|
| OpenSearch | cost vs search power |
| CDC pipeline | complexity vs freshness |
| DynamoDB checkpoints | simplicity vs cost |

---

## Assumptions

- eventual consistency acceptable
- tenants logically partitioned
- ingestion is append-heavy workload