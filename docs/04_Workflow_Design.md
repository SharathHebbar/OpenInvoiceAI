# OpenInvoice AI
## Workflow Design

- Version 1.0
- Author: Sharath S Hebbar
- Status: Draft


### Purpose

- Explain why Langgraph was chosen instead of sequential pipeline.

### Workflow Overview

- High Level Execution Flow

```mermaid
flowchart TD
    Upload --> Queue
    Queue --> Worker
    Worker --> Supervisor
    Supervisor --> Agents
    Agents --> ERP
    ERP --> Evaluation

    %% Styling to distinguish boundaries (Ingestion vs Execution vs System of Record)
    style Upload fill:#f9f9f9,stroke:#333,stroke-width:1px
    style ERP fill:#e3f2fd,stroke:#1565c0,stroke-width:1px
    style Evaluation fill:#e8f5e9,stroke:#2e7d32,stroke-width:1px
```

### Workflow State

- Define `InvoiceState`
    - InvoiceState
        - invoice
        - ocr_result
        - structured_invoice
        - validation
        - policy
        - decision
        - erp_status
        - evaluation
        - current_node
        - errors
        - retry_count

### Supervisor

Responsibilities
- Routing
- Retry
- Interrupt
- Resume
- Logging
- State transitions

Importantly

- The supervisor is deterministic, not LLM Driven

### Workflow Nodes

For each node:
- Purpose
- Input
- Output
- Failure Modes
- Next Nodes

Example
- Document Agent
    - Input: PDF
    - Output: Structured JSON
    - Possible Transitions
        - Success -> Validation Agent
        - Failure -> Retry -> Human Review


### Conditional Routing

Example 1

```mermaid
flowchart TD
    Validation{Validation Passed?}
    
    Validation -- YES --> PolicyAgent[Policy Agent]
    Validation -- NO --> HumanReview[Human Review]

    %% Color-coded decision paths for visual scannability
    style Validation fill:#e3f2fd,stroke:#1565c0,stroke-width:1px
    style PolicyAgent fill:#e8f5e9,stroke:#2e7d32,stroke-width:1px
    style HumanReview fill:#fff3e0,stroke:#ef6c00,stroke-width:1px
```

Example 2

```mermaid
flowchart TD
    Confidence{Confidence < 0.80?}
    
    Confidence -- YES --> RetryOCR[Retry OCR]
    Confidence -- NO / Else --> Continue[Continue Workflow]

    %% Visual styling for the condition check
    style Confidence fill:#e3f2fd,stroke:#1565c0,stroke-width:1px
    style RetryOCR fill:#fff3e0,stroke:#ef6c00,stroke-width:1px
    style Continue fill:#e8f5e9,stroke:#2e7d32,stroke-width:1px
```

### Human Review Interrupt

```mermaid
flowchart TD
    Workflow --> Interrupt
    Interrupt --> PersistState[Persist State]
    PersistState --> Wait
    Wait --> Resume
    Resume --> Continue

    %% Styling to reflect a paused execution cycle
    style Interrupt fill:#ffebee,stroke:#c62828,stroke-width:1px
    style PersistState fill:#fff3e0,stroke:#ef6c00,stroke-width:1px
    style Wait fill:#fff3e0,stroke:#ef6c00,stroke-width:1px
    style Resume fill:#e8f5e9,stroke:#2e7d32,stroke-width:1px
```

### Retry Strategy

Different Retry Strategies Examples

| Strategy | Retry Logic |
| -------- | ----------- |
| OCR      | Retry Twice |
| LLM Timeout | Exponential Backoff |
| ERP Failure | Queue Retry |
| Policy Failure | Human Review |

### Error Handling

- Recoverable vs Non-recoverable

Examples

- LLM Resilience
- Validation Failure
- OCR Timeout Handler

```mermaid
flowchart TD
    %% Scenario 1: OCR Timeout
    subgraph Scenario1 [OCR Timeout Handler]
        OCRTimeout[OCR Timeout] --> Retry[Retry Process]
    end

    %% Scenario 2: Invalid Invoice
    subgraph Scenario2 [Validation Failure]
        InvalidInvoice[Invalid Invoice] --> Reject[Reject Invoice]
    end

    %% Scenario 3: AI Availability
    subgraph Scenario3 [LLM Resilience]
        LLMUnavailable[LLM Unavailable] --> FallbackModel[Switch to Fallback Model]
    end

    %% Error/Exception Handling Styles
    style OCRTimeout fill:#ffebee,stroke:#c62828,stroke-width:1px
    style InvalidInvoice fill:#ffebee,stroke:#c62828,stroke-width:1px
    style LLMUnavailable fill:#ffebee,stroke:#c62828,stroke-width:1px
    
    %% Remediation Styles
    style Retry fill:#fff3e0,stroke:#ef6c00,stroke-width:1px
    style Reject fill:#ffcdd2,stroke:#b71c1c,stroke-width:2px
    style FallbackModel fill:#e8f5e9,stroke:#2e7d32,stroke-width:1px
```

### Workflow State Machine

```mermaid
flowchart TD
    START([START]) --> OCR
    OCR --> Validation
    Validation --> Policy
    Policy --> Decision
    Decision --> ERP
    ERP --> Evaluation
    Evaluation --> END([END])

    %% Styling start/end boundaries and systems of record
    style START fill:#eceff1,stroke:#37474f,stroke-width:2px
    style ERP fill:#e3f2fd,stroke:#1565c0,stroke-width:1px
    style Evaluation fill:#e8f5e9,stroke:#2e7d32,stroke-width:1px
    style END fill:#eceff1,stroke:#37474f,stroke-width:2px
```

### Sequence Diagram

```mermaid
flowchart TD
    Streamlit[Streamlit UI] --> FastAPI
    FastAPI --> Celery[Celery Queue]
    Celery --> LangGraph[LangGraph Orchestrator]
    LangGraph --> Agents[AI Agents]
    Agents --> Database[(Database)]
    Database --> ERP[ERP System]
    ERP --> UI[Streamlit UI Updates]

    %% Layout styling for stack components
    style Streamlit fill:#ffe0b2,stroke:#f57c00,stroke-width:1px
    style Database fill:#e1f5fe,stroke:#0288d1,stroke-width:1px
    style UI fill:#ffe0b2,stroke:#f57c00,stroke-width:1px
```

### Design Decisions

