# OpenInvoice AI
# Product Requirements Document (PRD)

Version 1.0
Author: Sharath S Hebbar
Status: Draft


### Vision

Build an open-source, production-inspired, multi-agent AI platform that autonomously processes invoices using specialized AI agents while providing observability, evaluation, auditability, and human approval workflows.

The platform should demonstrate modern AI engineering practices including:

- Multi-agent orchestration
- Tool calling
- Structured outputs
- Retrieval-based memory
- Human-in-the-loop workflows
- Distributed task execution
- AI observability
- Production deployment

### Problem Statement

Many organizations still process invoices manually

#### Typical Workflow 

Receive Invoice -> Extract Data -> Validate -> Check Vendor -> Check Purchase Order -> Apply Company Policies -> ERP Entry -> Approval -> Archive

#### Problems
- Manual Effort
- Human Errors
- Duplicate Invoices
- Slow Approvals
- Lack of Traceablity
- Poor Audit History
- Difficult Policy Enforcement

### Product Goals

OpenInvoice should automate as much of the workflow as possible while keeping humans involved only when necessary.

#### Goals

- Reduce manual invoice processing
- Detect Duplicate Invoices
- Validate Invoice Correctness
- Enforce business policies
- Route uncertain invoices for review
- Provide complete audit trial
- Support Multiple ERP Systems
- Be fully open-source

### Target User

| Team Type | Primary | Secondary | Future |
| :--- | :--- | :--- | :--- |
| **Department** | Finance Teams | System Administrators | Developers |
| **Responsibilities** | • Upload invoices<br>• Review flagged invoices<br>• Approve or reject invoices | • Configure company policies<br>• Monitor processing<br>• View system health<br>• Configure LLM providers | • Add new agents<br>• Add ERP integrations<br>• Add tools<br>• Fine-tune prompts |

### Functional Requirements

#### Invoice Upload

System Shall:
- Accept PDF Invoices
- Accept Image Invoices
- Generate Unique Job ID
- Store Uploaded File
- Queue Processing

#### OCR

System Shall:
- Extract Invoice Text
- Detect Tables
- Detect Vendor
- Detect Invoice Metadata
- Produce Structured JSON

#### Validation

System Shall verify:
- GST Number
- Invoice Number
- Duplicate Invoices
- Currency 
- Tax Calculations
- Total Amount
- Purchase Order

#### Policy Engine

System Shall:
- Evaluate Business Policies such as
    - If Invoice > 50K then Manager Approval
    - Unknown Vendor then Reject
    - Foreign Currency then Finance Review

#### Decision Engine

Possible Outputs
- Approved
- Rejected
- Retry OCR
- Human Review


#### ERP

System Shall
- Map invoice fields -> ERP Schema -> Persist Data

#### Evaluation

Every processed invoice receives
- Confidence Score
- Policy Compliance
- Latency
- Cost
- Agent Trace
- Tool Usage

### Non Functional Requirements


| System Attribute | Performance | Scalability | Reliability | Observability | Security |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Metrics / Features** | • Upload < 2 seconds<br>• OCR < 15 seconds<br>• End-to-End < 60 seconds | • Concurrent invoice processing<br>• Distributed workers | • Automatic retries<br>• Dead-letter queue | • Langfuse traces<br>• OpenTelemetry | • API Authentication (future)<br>• Secure secret management |


### User Journey

```mermaid
graph LR
    A[User Uploads Invoice] --> B[FastAPI receives request]
    B --> C[Create Job]
    C --> D[Store Invoice]
    D --> E[Redis Queue]
    E --> F[Celery Worker]
    F --> G[LangGraph]
    
    subgraph AI Agent Workflow
        G --> H[Document Agent]
        H --> I[Validation Agent]
        I --> J[Policy Agent]
        J --> K[Decision Agent]
        K --> L[ERP Agent]
        L --> M[Evaluation Agent]
    end
    
    M --> N[Store Results]
    N --> O[Update Dashboard]

    %% Styling %%
    style A fill:#4CAF50,stroke:#333,stroke-width:2px,color:#fff
    style O fill:#2196F3,stroke:#333,stroke-width:2px,color:#fff
    classDef default fill:#f9f9f9,stroke:#333,stroke-width:1px;
```

### Success Metrics

Technical
- OCR Accuracy
- JSON Validity
- Tool Success Rate
- Processing Latency
- Agent Latency

Business
- Approval Rate
- Duplication Detection Rate
- Manual Review %
- Policy Compliance %

### Assumptions

- Invoice is Readable
- OCR Returns usable outputs
- Vendor Database exists
- Company policies are configurable

### Constraints

Current MVP
- Single Tenant
- English Invoices
- PostgreSQL
- Streamlit UI
- Groq / Ollama

Future
- Multi Tenant
- Authentication
- SAP
- Oracle
- Email Ingestion
- Voice Approvals

### Technology Stack

| Component | Technology |
| --- | --- |
| UI | Streamlit |
| Backend API | FastAPI |
| Agentic Framework | LangGraph |
| LLM | LiteLLM (Groq) |
| OCR | Docling |
| Queue | Celery and Redis |
| Database | PostgreSQL |
| VectorDB | Qdrant |
| Embeddings | BAAI/bge-small-en-v1.5 |
| Observability | Langfuse |
| Tracing | OpenTelemetry |
| Evaluation | DeepEval |
| Container | Docker Compose |
| Package Manager | uv |
| Testing | pytest |