## Background
This project is a part of a case study I received for an interview. Since there was no NDA and basically a free takehome assignment, I decided to upload my work here.

## The Goal:
Design and build a facade for an Agentic Workflow Management System that processes medical appointments.


## Core Product Requirements

*Intelligent Orchestrator:* A master agent that ingests a feed of appointments from a database. It must intelligently decide which appointments to process first based on dynamic priorities (which may vary by client, specialty, or other unknown factors).

*Agentic Processing:* Appointments go through a configurable number of processing stages (e.g., 6 stages). Each stage should be conceptualized as an individual agent.

*Standardized Outputs:* Each processing stage must return one of four states: Not Started, Processing, Complete, or Escalate.

*The Exception Queue:* If an agent returns Escalate, the appointment must be routed to a human-in-the-loop Exception Queue.

*Human Concierge Resolution:* A human user must be able to interact with the Exception Queue to unblock the issue. Once resolved, the system should immediately update the appointment status to Cleared and resume workflow if necessary.

## Solution Design:
This is lightweight system for medical appointment processing, where each appointment flows through a 6-stage pipeline (Intake, Insurance check, Clinical pre-check, Provider Matching, Outreach, and Final confirmation).
The system includes a dynamic priority engine that ranks appointments based on factors like VIP status, risk score, specialty, client type, and time sensitivity (with both rule-based and LLM-ready design).

Appointments are processed by an orchestrator that executes stages sequentially, and any failures or edge cases are routed to a human-in-the-loop exception queue (Human Concierge) for resolution via UI or API.

## Backend endpoints:
```
POST /run-pipeline → triggers workflow execution
GET /appointments → fetch all appointments with current stage + status
GET /exceptions → view escalated cases
POST /resolve/{id} → resolve and resume workflow
POST /appointments → add new appointments (raw data)
```

The design focuses on clear separation of concerns, extensibility for LLM-based decision making, and a realistic simulation of healthcare workflow orchestration systems.

Adding screenshots of my FastAPI backend.

![Fast Api Backend](fastapi_image.png)

This is how my basic Human concierge UI would look like, where a human-in-the-loop would resolve in case an appointment is stuck in any stage

![Human Conceirge](huma_conceirge_front_end.png)

This is how my basic database table in PostgreSQL looks:

![Postgres Backend](postgres_backend.png)
