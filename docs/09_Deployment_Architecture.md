# OpenInvoiceAI

## Deployment Architecture

- Version: 1.0
- Author: Sharath S Hebbar
- Status: Draft

### Purpose

- This document defines the deployment architecture for the OpenInvoice-AI Platform, including infrastructure topology, containerization, networking, scaling, strategy, storage, and runtime dependencies.
- The architecture supports
    - Local Development
    - Single Node Deployment
    - Cloud Deployment
    - Future K8s based scaling


### Development Goals

| Goal           | Description                             |
| -------------- | --------------------------------------- |
| Portable       | Run locally or in the cloud             |
| Containerized  | All services run in Docker containers   |
| Scalable       | Independent service scaling             |
| Fault Tolerant | Recover from service failures           |
| Observable     | Centralized monitoring and logging      |
| Secure         | Network isolation and secret management |


### Deployment Topology

```mermaid
flowchart TB

User["User / Browser"]

Frontend["Streamlit Frontend"]

Gateway["FastAPI Gateway"]

Redis["Redis Queue"]

Worker["Celery Worker"]

LangGraph["LangGraph Supervisor"]

Postgres[(PostgreSQL)]

Qdrant[(Qdrant)]

Storage[(Object Storage)]

LLM["LLM Server\n(Ollama / vLLM)"]

Monitoring["Langfuse + OpenTelemetry"]

User --> Frontend
Frontend --> Gateway
Gateway --> Redis
Redis --> Worker
Worker --> LangGraph

LangGraph --> Postgres
LangGraph --> Qdrant
LangGraph --> Storage
LangGraph --> LLM

Gateway --> Monitoring
Worker --> Monitoring
LangGraph --> Monitoring
```

### Runtime Components

| Component   | Responsibility         |
| ----------- | ---------------------- |
| Streamlit   | User interface         |
| FastAPI     | REST API               |
| Redis       | Message broker         |
| Celery      | Background jobs        |
| LangGraph   | Workflow orchestration |
| PostgreSQL  | Persistent data        |
| Qdrant      | Vector search          |
| Ollama/vLLM | LLM inference          |
| Langfuse    | LLM observability      |


### Container Architecture

```mermaid
flowchart LR

DockerHost

--> FrontendContainer

--> GatewayContainer

--> WorkerContainer

--> RedisContainer

--> PostgresContainer

--> QdrantContainer

--> OllamaContainer

--> MonitoringContainer
```

Each service runs independently and communicates over Docker networks

### Docker Network

```mermaid
flowchart LR

Frontend

--> BackendNetwork

Gateway

--> BackendNetwork

Worker

--> BackendNetwork

Redis

--> BackendNetwork

Postgres

--> BackendNetwork

Qdrant

--> BackendNetwork

LLM

--> BackendNetwork
```

A dedicated backend network isolates internal services from external access.

### Request Flow

```mermaid
sequenceDiagram

participant User
participant Frontend
participant Gateway
participant Redis
participant Worker
participant LangGraph

User->>Frontend: Upload Invoice
Frontend->>Gateway: POST /invoices
Gateway->>Redis: Queue Job
Redis->>Worker: Dispatch Task
Worker->>LangGraph: Execute Workflow
LangGraph-->>Worker: Result
Worker-->>Gateway: Update Status
Gateway-->>Frontend: Workflow Status
```

### Storage Architecture

```mermaid
flowchart TD
    Uploaded_Invoice[Uploaded Invoice] --> Object_Storage[Object Storage]
    Object_Storage --> Workflow
    Workflow --> Processed_Invoice[Processed Invoice]
    Processed_Invoice --> Archive
```

Supported storage backends
- Local filesystem (development)
- MinIO
- AWS S3
- Azure Blob Storage

### LLM Deployment

```mermaid
flowchart LR

Agents

-->

LiteLLM

-->

Ollama

Llama.cpp

vLLM
```

The abstraction layer allows switching between providers without changing agent logic.

### Scaling Strategy

| Component      | Scaling Method                 |
| -------------- | ------------------------------ |
| Streamlit      | Horizontal replicas            |
| FastAPI        | Multiple instances             |
| Celery Workers | Worker pool expansion          |
| Redis          | Single instance (MVP)          |
| PostgreSQL     | Vertical scaling / replication |
| Qdrant         | Cluster mode (future)          |
| LLM            | GPU replicas                   |


### High Availability (Future)

```mermaid
flowchart TD

LoadBalancer

--> Gateway1

--> Gateway2

Gateway1 --> Redis
Gateway2 --> Redis

Redis --> Worker1
Redis --> Worker2

Worker1 --> PostgreSQL
Worker2 --> PostgreSQL
```

Future Improvements
- Redis Sentinel
- PostgreSQL replication
- Multiple Worker Nodes

### Configuration Management

Configuration Sources:
- Environmental Variables
- `.env` files (development)
- Docker Compose overrides
- Kubernetes ConfigMaps (future)
- Secret stores

Example categories:
- Database URLs
- API Keys
- LLM Model selection
- Retry policies
- Storage paths

### Secrets Management

```mermaid
flowchart LR
    Application --> Secret_Manager[Secret Manager]
    Secret_Manager --> Credentials
    Credentials --> External_Service[External Service]
```

Principles:

- Never hardcode secrets
- Separate development and production credentials
- Rotate secrets periodically

### Logging Architecture

```mermaid
flowchart LR
    Frontend --> Gateway
    Gateway --> Worker
    Worker --> LangGraph
    LangGraph --> Structured_Logs[Structured Logs]
    Structured_Logs --> Central_Log_Store[Central Log Store]
```

Each log entry includes
- Timestamp
- Trace ID
- Workflow ID
- Service name
- Log Level

### Montioring Architecture

```mermaid
flowchart LR

Services

-->

OpenTelemetry

-->

Langfuse

-->

Dashboards
```

Metrics
- API Latency
- Workflow duration
- Queue depth
- LLM Latency
- Token usage
- Error Rates

### Health Checks

Every service exposes

| Endpoint  | Purpose         |
| --------- | --------------- |
| `/health` | Basic health    |
| `/ready`  | Readiness probe |
| `/live`   | Liveness probe  |

These endpoints enable orchestration platforms to monitor service health

### Deployment Environments

| Environment | Purpose                   |
| ----------- | ------------------------- |
| Local       | Development               |
| Development | Shared testing            |
| Staging     | Pre-production validation |
| Production  | Live workloads            |

Each environment may use different models, databases, and storage backends.

### Docker Compose Architecture

```mermaid
flowchart TD

docker-compose.yml

-->

Frontend

-->

Gateway

-->

Worker

-->

Redis

-->

Postgres

-->

Qdrant

-->

LLM

-->

Langfuse
```

Docker compose serves as the primary deployment mechanism for local development and demonstrations.

### Future Kubernetes Architecture

```mermaid
flowchart TB
    Ingress --> Frontend_Pods[Frontend Pods]
    Frontend_Pods --> Gateway_Pods[Gateway Pods]
    Gateway_Pods --> Worker_Pods[Worker Pods]
    Worker_Pods --> Postgres
    Worker_Pods --> Qdrant
    Worker_Pods --> Redis

    subgraph Stateful_Services [Stateful Services]
        Postgres
        Qdrant
        Redis
    end
```

Future Enhancements
- Horizontal Pod Autoscaler
- Persistent Volumes
- Helm Charts
- Service Mesh (optional)


### Disaster Recovery

Recovery Strategy:
- Automated PostgreSQL backups
- Object storage snapshots
- Configuration backups
- Workflow checkpoint persistence
- Container image versioning

Recovery Objective:
- Resume interrupted workflows from checkpoints without reprocessing completed steps.

### Performance Considerations
| Component  | Optimization               |
| ---------- | -------------------------- |
| Gateway    | Async request handling     |
| Workers    | Parallel task execution    |
| Redis      | In-memory queue            |
| PostgreSQL | Indexed queries            |
| Qdrant     | Optimized vector indexing  |
| LLM        | Model caching and batching |


### Architecture Decision Records (ADR)

| ADR ID  | Decision                                   | Rationale                               |
| ------- | ------------------------------------------ | --------------------------------------- |
| ADR-025 | Docker-first deployment                    | Consistent local and cloud environments |
| ADR-026 | Celery + Redis for asynchronous processing | Mature, reliable task queue             |
| ADR-027 | Dedicated LLM service                      | Decouple inference from business logic  |
| ADR-028 | Object storage for invoice files           | Scalable and cloud-agnostic             |
| ADR-029 | Container-per-service architecture         | Independent scaling and fault isolation |
