# OpenInvoiceAI

## UI/UX Design

- Version: 1.0
- Author: Sharath S Hebbar
- Status: Draft

### Purpose

- This document defines the user interface architecture, user experience flows, and frontend components for the OpenInvoice-AI platform
- The Frontend provides a single operational interface for uploading invoices, monitoring workflows, reviewing agent decisions, resolving exceptions, and analyzing system performance.
- The design emphasizes transparency, observability, and efficient human-in-the-loop interactions rather than simply serving as an upload page

### Design Goals

| Goal         | Description                                 |
| ------------ | ------------------------------------------- |
| Simplicity   | Minimal learning curve                      |
| Transparency | Expose workflow progress clearly            |
| Human Review | Easy approval and correction workflows      |
| Real-Time    | Live status updates                         |
| Responsive   | Desktop-first with responsive layouts       |
| Extensible   | Modular component architecture              |
| Accessible   | WCAG-compliant interactions where practical |


### Technology Stack

| Component        | Technology                   |
| ---------------- | ---------------------------- |
| Framework        | Streamlit (MVP)              |
| Future Upgrade   | React + FastAPI              |
| State Management | Streamlit Session State      |
| Charts           | Plotly                       |
| Tables           | AgGrid / Streamlit DataFrame |
| File Upload      | Streamlit File Uploader      |
| Authentication   | JWT (future)                 |

### Frontend Architecture

```mermaid
flowchart LR

User["User"]

UI["Streamlit UI"]

API["FastAPI Gateway"]

Workflow["Workflow Service"]

User --> UI
UI --> API
API --> Workflow
```

### Application Navigation

```mermaid
flowchart TD
    Home --> Upload
    Home --> Dashboard
    Home --> Settings
    Home --> System_Health[System Health]
    Dashboard --> Workflow_Details[Workflow Details]
    Workflow_Details --> Human_Review[Human Review]
    Workflow_Details --> Evaluations
```

### User Journey

```mermaid
journey
    title Invoice Processing Journey

    section Upload
      Upload Invoice: 5: User

    section Processing
      OCR Running: 4: System
      Validation: 4: System
      Policy Check: 4: System
      Decision: 4: System

    section Review
      Human Approval: 5: User

    section Completion
      ERP Sync: 5: System
```


### Screen Overview

| Screen          | Purpose                 |
| --------------- | ----------------------- |
| Home            | Entry point             |
| Upload          | Upload invoices         |
| Dashboard       | Monitor processing      |
| Workflow Detail | View workflow state     |
| Human Review    | Resolve exceptions      |
| Evaluation      | Inspect quality metrics |
| Settings        | Runtime configuration   |
| Health          | System diagnostics      |


### Upload Screen

Purpose:
- Upload one or more invoices
- Display upload progress
- Validate file type
- Submit workflow

```mermaid
flowchart LR
    User --> Upload_Form[Upload Form]
    Upload_Form --> API
    API --> Workflow_Created[Workflow Created]
```

Displayed Information:
- File name
- size
- Upload status
- Workflow ID

### Dashboard

The dashboard provides a high level operational overview

Widgets:
- Total Invoices
- Processing Queue
- Completed workflows
- Failed workflows
- Human review queue
- Average Latency
- Token Usage
- Daily throughput

```mermaid
flowchart TD
    KPIs --> Charts
    Charts --> Recent_Workflows[Recent Workflows]
    Recent_Workflows --> Alerts
```


### Workflow Details Screen

Purpose:

Display the full execution history of a workflow

Information includes:
- Current State
- Active Agent
- Workflow Timeline
- State transitions
- Agent Outputs
- Tool invoications
- Errors
- Retry history


```mermaid
flowchart LR
    Workflow --> Timeline
    Timeline --> Agent_Details[Agent Details]
    Agent_Details --> State_Viewer[State Viewer]
```

### Human Review Screen

This is one of the most important screens

Users can:
- Review extracted invoice fields
- Compare OCR output with the original document
- Edit incorrect values
- Approve
- Reject 
- Resume Workflow

```mermaid
flowchart LR

Invoice

-->

Review

-->

Approve

Reject

Edit
```

### Evaluation Dashboard

Displays workflow quality metrics

Metrics include:

- OCR confidence
- Validation success rate
- Policy violations
- LLM Latency
- Token usage
- Cost estimation
- Hallucination score

Charts:
- Processing Latency
- Agent execution time
- Daily throughput
- Cost trends

### Settings Screen

Allows administrators to configure
- Active LLM
- OCR Engine
- Confidence thresholds
- Retry limits
- Human review threshold
- Feature flags


### System Health Screen

Displays:
- Database status
- Redis Status
- LLM Availability
- Queue depth
- API Health
- Storage connectivity

```mermaid
flowchart TD
    System --> Health_Checks[Health Checks]
    Health_Checks --> Status_Cards[Status Cards]
```

### Component Hierarchy

```mermaid
flowchart TD

App

--> Sidebar

--> UploadPage

--> Dashboard

--> WorkflowPage

--> ReviewPage

--> EvaluationPage

--> SettingsPage
```

### Frontend State Management

```mermaid
stateDiagram-v2

Idle --> Uploading

Uploading --> Submitted

Submitted --> Polling

Polling --> Completed

Polling --> HumanReview

HumanReview --> Polling

Completed --> Idle
```

### API Interaction

```mermaid
sequenceDiagram

participant User
participant UI
participant API
participant Workflow

User->>UI: Upload Invoice
UI->>API: POST /invoices
API-->>UI: Workflow ID

loop Status Updates
UI->>API: GET /workflows/{id}
API-->>UI: Current State
end

UI-->>User: Display Progress
```

#### Future Enhancement
- Websockets
- SSE (Server-Sent Events)
- Push notifications

### Error Handling

Common Scenarios

| Error                  | UI Behavior        |
| ---------------------- | ------------------ |
| Upload failed          | Retry prompt       |
| Invalid file           | Validation message |
| Workflow failed        | Error banner       |
| API unavailable        | Offline indicator  |
| Authentication expired | Redirect to login  |


### Accessibility

Key considerations
- Keyboard navigation
- Screen reader labels
- High-contrast mode (future)
- Responsive layouts
- Clear error messaging

### Performance considerations

- Lazy load workflow history
- Paginate invoice lists
- Cache dashboard data
- Poll only active workflows
- Compress uploaded files when appropriate

### Future Enhancements
Potential additions

| Feature              | Purpose                   |
| -------------------- | ------------------------- |
| Drag-and-drop upload | Improved UX               |
| Dark mode            | User preference           |
| Batch upload         | Process multiple invoices |
| Workflow replay      | Debugging                 |
| Live notifications   | Real-time updates         |
| Mobile support       | Operational monitoring    |


### Architecutre Decision Records (ADR)


| ADR ID  | Decision                              | Rationale                               |
| ------- | ------------------------------------- | --------------------------------------- |
| ADR-020 | Streamlit for MVP                     | Faster development and lower complexity |
| ADR-021 | Dashboard-centric UX                  | Focus on operational visibility         |
| ADR-022 | Polling for workflow updates          | Simpler initial implementation          |
| ADR-023 | Human review as a first-class feature | Essential for AI-assisted workflows     |
| ADR-024 | React reserved for future scalability | Avoid premature complexity              |
