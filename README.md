# SecurePHI

## Overview

**SecurePHI** is an AI-driven solution designed to safeguard sensitive patient data in clinical notes. By leveraging role-based access control and OpenAI’s **GPT-4O** model, SecurePHI dynamically identifies, segments, and redacts sensitive sections of patient records. This ensures that only authorized personnel have access to protected health information (PHI), reducing the risk of data breaches and supporting compliance with healthcare data privacy regulations.

**Key Features:**

- **AI-Based Medical Concept Extraction:**  
  Uses GPT-4O (Azure OpenAI) to parse clinical notes, identifying key medical sections (e.g., Patient Information, Chief Complaint, Medications) and structuring them for easy segmentation.

- **Role-Based Access Control:**  
  Dynamically determines which sections a user can view based on their role. Users with restricted privileges receive redacted versions of sensitive sections.

- **Automated Redaction & Overrides:**  
  Sensitive information is hidden from unauthorized viewers. Emergency overrides trigger instant email alerts to security teams for audit and follow-up.

- **Database Integration for User Data:**  
  Extracts user roles, facility access, and permissions from a SQL database (e.g., Azure SQL Server) via `pyodbc`. This approach is adaptable to other SQL databases (e.g., Postgres) with minor configuration changes.

- **Email Alerts via SMTP:**  
  Unauthorized access attempts generate automatic email alerts, leveraging SMTP for secure and immediate notification.

## Architecture

**Backend (Python, Flask, GPT-4O, Database, SMTP):**
- Flask API for managing requests and responses.
- GPT-4O for segmenting and interpreting clinical notes.
- SQL database (via `pyodbc`) for retrieving user, role, and facility data.
- Redaction logic based on user roles.
- SMTP integration for sending email alerts on unauthorized access attempts.

**Frontend (React + Vite):**
- User-friendly interface for inputting patient ID, user role, and requested headers.
- Sends requests to the backend and displays processed, potentially redacted clinical notes.
- Highlights accessible sections and indicates restricted areas if the user lacks proper authorization.

**Data Sources & Storage:**
- Clinical notes stored in JSON for demonstration.
- User roles and permissions fetched from a SQL database.
- Potential to integrate additional data sources and persistent storage solutions.

## Installation & Setup

### Backend Setup

**Requirements:**
- Python 3.10+
- `pip` for Python dependency management
- Azure OpenAI API credentials (endpoint, deployment name, API key for GPT-4O)
- Valid database connection credentials for user/facility data (Azure SQL Server or Postgres)
- SMTP-enabled email account for sending alerts

**Steps:**
1. Navigate to `backend` directory:
   ```bash
   cd backend
   pip3 install -r requirements.txt
   python3 app.py
The backend runs at http://localhost:5000 by default.

### Frontend Setup

**Requirements:**
- Node.js and npm
- Vite (included in devDependencies)
- A running backend on http://localhost:5000

**Steps:**
1. Navigate to `frontend` directory:
   ```bash
   cd frontend
   npm install
   npm run dev
