# OpenInvoiceAI

## System Architecture

- Version: 1.0
- Author: Sharath S Hebbar
- Status: Draft

### Purpose

This document describes the high-level architecture of OpenInvoiceAI, including service integrations, agent orchestration, infrastructure components, data flow, and deployment architecure.

The goal is to build a modular, scalable, production-inspired AI platform for autonomous invoice processing using agentic workflows.

### High Level Architecture

```mermaid
graph TD
    %% Nodes Definitions
    UI["Streamlit UI<br>Upload • Dashboard • Review"]
    API["FastAPI Gateway<br>Upload • APIs • Auth"]
    Redis["Redis<br>Celery Queue"]
    Worker["Celery Worker<br>Executes LangGraph Workflow"]
    Router["LangGraph Supervisor (Deterministic Router)"]
    
    DocAgent["Document Agent"]
    ValAgent["Validation Agent"]
    PolAgent["Policy Agent"]
    
    DecAgent["Decision Agent"]
    Human["Human Review"]
    
    ERP["ERP Adapter"]
    Retry["Retry / Reject"]
    
    EvalAgent["Evaluation Agent"]
    
    Storage[(PostgreSQL • Qdrant • Langfuse • OpenTelemetry • Audit Logs)]

    %% Execution Flow
    UI --> API
    API -->|Create Processing Job| Redis
    Redis --> Worker
    Worker --> Router

    %% Router Split to Core Agents
    Router --> DocAgent
    Router --> ValAgent
    Router --> PolAgent

    %% Core Agents Converge
    DocAgent --> DecAgent
    DocAgent --> Human
    ValAgent --> DecAgent
    ValAgent --> Human
    PolAgent --> DecAgent
    PolAgent --> Human

    %% Decision Router Split
    DecAgent --> ERP
    DecAgent --> Retry

    %% Final Chain
    ERP --> EvalAgent
    EvalAgent --> Storage

    %% Clean Architectural Styling
    classDef default fill:#ffffff,stroke:#333333,stroke-width:1px,color:#333333;
    classDef storageNode fill:#f8f9fa,stroke:#333333,stroke-dasharray: 5 5;
    class Storage storageNode;

```


### Design Principles

The architecture follows these principles

#### Modular

- Every component should be independently replaceable.
- Example 

```mermaid
graph TD
    A[Docling] --> B[PaddleOCR]
    B --> C[Azure Document Intelligence]

    %% Clean Minimal Styling %%
    style A fill:#4A90E2,stroke:#333,stroke-width:1px,color:#fff
    style B fill:#50E3C2,stroke:#333,stroke-width:1px,color:#333
    style C fill:#0078D4,stroke:#333,stroke-width:1px,color:#fff
```

- Changing OCR should not require changes elsewhere.

#### Agent Oriented

Every major business responsibility belongs to an independent AI Agent
Each Agent should:
- Have one responsibility
- Produce structured outputs
- Call tools when required
- Never directly access the UI

#### Event Driven

Invoice processing is asynchronous

```mermaid
graph TD
    A[Upload] --> B[Queue]
    B --> C[Worker]
    C --> D[Process]
    D --> E[Notify]

    %% Professional Minimal Styling %%
    style A fill:#4CAF50,stroke:#333,stroke-width:1px,color:#fff
    style E fill:#2196F3,stroke:#333,stroke-width:1px,color:#fff
    classDef default fill:#f9f9f9,stroke:#bbb,stroke-width:1px,color:#333;
```

- Users never wait for OCR.


#### Tool-Centric

Agents should reason.
Tools should execute.
Example:

Validation Agent decides -> Vendor Lookup Tool executes SQL

This separation keeps prompts simple and logic deterministic

#### Observable

Every Agent execution should produce:
- Logs
- Traces
- Metrics 
- LLM token usage
- Latency
- Tool Calls

### Component Responsibilities

#### 1. Application & Core Logic Components

| Component | Key Responsibilities | Architectural Constraints / Scope |
| :--- | :--- | :--- |
| **Streamlit** | • Upload invoices<br>• Show processing status<br>• Display reasoning<br>• Human approvals<br>• Dashboard<br>• History | ⚠️ **Never** performs AI processing. |
| **FastAPI** | • Receive uploads<br>• Validate requests<br>• Create Job<br>• Store files<br>• Expose REST APIs<br>• Return Job IDs | ⚠️ **Never** executes AI workflows. |
| **Redis** | • Queue jobs<br>• Message broker | *N/A* |
| **Celery** | • Execute background workflows<br>• Retry failed tasks<br>• Schedule long-running jobs | *N/A* |
| **LangGraph** | • Manage workflow state<br>• Execute agent graph<br>• Handle conditional routing<br>• Retry failed nodes<br>• Human interrupts | *N/A* |

#### 2. Databases & Storage Systems

| Database | Primary Storage Entities | Specialized Storage Engine Capability |
| :--- | :--- | :--- |
| **PostgreSQL** | • Invoices<br>• Jobs<br>• Policies<br>• Vendors<br>• Agent Runs<br>• Audit Logs<br>• Evaluations | Relational Data & System State Tracking |
| **Qdrant** | • Vendor history<br>• Previous invoices<br>• Company policy<br>• Invoice corrections | 🔍 Supports **semantic retrieval** using vector embeddings. |

#### 3. LLM Observability Layer

| Monitoring Platform | Telemetry & Metrics Captured |
| :--- | :--- |
| **Langfuse** | • Prompt traces<br>• Tool calls<br>• Token usage<br>• LLM latency<br>• Cost<br>• Agent reasoning |

### Agent Architecture

#### Supervisor Agent

Responsibilites
- Start Workflow
- Select next agent
- Handle failures 
- Retry Orchestration
- Maintain workflow state

Never performs business logic

#### Document Agent

- Input
- Invoice PDF
- Output
- Structured Invoice JSON
- Uses
    - OCR Tool
    - LLM

#### Validation Agent

Uses Tools
- GST Validator
- Vendor LookUp
- Duplicate Checker
- Currency Validator
- Tax Validator

Produces
- Validation Report


#### Policy Agent

Reads
- Company Policies

Reasons Over
- Amount
- Vendor
- Country
- Currency
- Risk

Produces
- Policy Recommendation

#### Decision Agent

- Combines
    - Validation
    - Policy
    - Confidence

- Produces
- Approve
- Reject
- Retry
- Human Review

#### ERP Agent

```mermaid
graph TD
    %% Nodes Definitions
    UI["Streamlit UI<br>Upload • Dashboard • Review"]
    API["FastAPI Gateway<br>REST APIs • Auth • Upload"]
    Redis["Redis<br>Celery Queue"]
    Worker["Celery Worker<br>Executes LangGraph Workflow"]
    Router["Supervisor Agent (Router)"]
    
    DocAgent["Document Agent"]
    ValAgent["Validation Agent"]
    PolAgent["Policy Agent"]
    DecAgent["Decision Agent"]
    
    ERPAgent["ERP Agent"]
    Human["Human Review"]
    EvalAgent["Evaluation Agent"]
    
    Storage[(PostgreSQL • Qdrant • Langfuse • Audit Logs)]

    %% Execution Flow
    UI --> API
    API -->|Create Processing Job| Redis
    Redis --> Worker
    Worker --> Router

    %% Router Split
    Router --> DocAgent
    Router --> ValAgent
    Router --> PolAgent

    %% Merge to Decision Agent
    DocAgent --> DecAgent
    ValAgent --> DecAgent
    PolAgent --> DecAgent

    %% Decision Split
    DecAgent --> ERPAgent
    DecAgent --> Human

    %% Final Chain
    ERPAgent --> EvalAgent
    EvalAgent --> Storage

    %% Styling to mimic the clean ASCII look
    classDef default fill:#ffffff,stroke:#333333,stroke-width:1px,color:#333333;
    classDef storageNode fill:#f8f9fa,stroke:#333333,stroke-dasharray: 5 5;
    class Storage storageNode;
```

#### Evaluation Agent

Calculates
- Confidence
- Latency
- Cost
- Policy Compliance
- Tool Success
- Overall Quantity

### Data Flow

```mermaid
graph TD
    A["Upload Invoice"] --> B["FastAPI"]
    B --> C["PostgreSQL"]
    C --> D["Redis Queue"]
    D --> E["Celery Worker"]
    E --> F["LangGraph"]
    F --> G["Supervisor Agent"]
    G --> H["Document Agent"]
    H --> I["Validation Agent"]
    I --> J["Policy Agent"]
    J --> K["Decision Agent"]
    K --> L["ERP Agent"]
    L --> M["Evaluation Agent"]
    M --> N["Persist Results"]
    N --> O["Frontend Dashboard"]

    %% Professional Technical Styling %%
    style A fill:#4CAF50,stroke:#333,stroke-width:1px,color:#fff
    style O fill:#2196F3,stroke:#333,stroke-width:1px,color:#fff
    classDef default fill:#ffffff,stroke:#333,stroke-width:1px,color:#333;
```

### Failure Handling

| Failure         | Action             |
| --------------- | ------------------ |
| OCR Failure     | Retry              |
| Invalid JSON    | Retry Agent        |
| Vendor Missing  | Human Review       |
| Policy Conflict | Human Review       |
| ERP Failure     | Retry Queue        |
| LLM Timeout     | Retry with Backoff |graph TD
    %% Nodes Definitions
    UI["Streamlit UI<br>Upload • Dashboard • Review"]
    API["FastAPI Gateway<br>Upload • APIs • Auth"]
    Redis["Redis<br>Celery Queue"]
    Worker["Celery Worker<br>Executes LangGraph Workflow"]
    Router["LangGraph Supervisor (Deterministic Router)"]
    
    DocAgent["Document Agent"]
    ValAgent["Validation Agent"]
    PolAgent["Policy Agent"]
    
    DecAgent["Decision Agent"]
    Human["Human Review"]
    
    ERP["ERP Adapter"]
    Retry["Retry / Reject"]
    
    EvalAgent["Evaluation Agent"]
    
    Storage[(PostgreSQL • Qdrant • Langfuse • OpenTelemetry • Audit Logs)]

    %% Execution Flow
    UI --> API
    API -->|Create Processing Job| Redis
    Redis --> Worker
    Worker --> Router

    %% Router Split to Core Agents
    Router --> DocAgent
    Router --> ValAgent
    Router --> PolAgent

    %% Core Agents Converge
    DocAgent --> DecAgent
    DocAgent --> Human
    ValAgent --> DecAgent
    ValAgent --> Human
    PolAgent --> DecAgent
    PolAgent --> Human

    %% Decision Router Split
    DecAgent --> ERP
    DecAgent --> Retry

    %% Final Chain
    ERP --> EvalAgent
    EvalAgent --> Storage

    %% Clean Architectural Styling
    classDef default fill:#ffffff,stroke:#333333,stroke-width:1px,color:#333333;
    classDef storageNode fill:#f8f9fa,stroke:#333333,stroke-dasharray: 5 5;
    class Storage storageNode;


### Scalability

Horizontal scaling support for:
- FastAPI
- Celery Workers
- Redis
- PostgreSQL Read Replicas
- Qdrant Cluster

### Security

Future Enhancements
- JWT Authentication
- Role Base Access Control (RBAC)
- Secret Manager
- Audit Logs
- Encryption at Rest

### Technology Decisions

| Requirement | Technology     | Reason                       |
| ----------- | -------------- | ---------------------------- |
| UI          | Streamlit      | Fast prototyping             |
| API         | FastAPI        | Async APIs                   |
| Workflow    | LangGraph      | Stateful agent orchestration |
| Queue       | Celery         | Distributed task execution   |
| Broker      | Redis          | Lightweight and mature       |
| Database    | PostgreSQL     | ACID transactions            |
| Vector DB   | Qdrant         | Fast semantic search         |
| OCR         | Docling        | Modern document parsing      |
| LLM         | LiteLLM        | Provider abstraction         |
| Evaluation  | DeepEval       | LLM evaluation               |
| Tracing     | Langfuse       | Prompt observability         |
| Deployment  | Docker Compose | Easy local setup             |

