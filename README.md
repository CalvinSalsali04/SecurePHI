Overview
SecurePHI is an AI-driven solution designed to safeguard sensitive patient data in clinical notes. By leveraging role-based access control and OpenAI’s GPT-4O model, SecurePHI dynamically identifies, segments, and redacts sensitive sections of patient records. This ensures that only authorized personnel have access to protected health information (PHI), reducing the risk of data breaches and supporting compliance with healthcare data privacy regulations.

Key Features:

AI-Based Medical Concept Extraction: Uses GPT-4O (Azure OpenAI) to parse clinical notes, identify key medical sections (e.g., Patient Information, Chief Complaint, Medications), and structure them for easy segmentation.
Role-Based Access Control: Dynamically determines which sections a user can view based on their role. Users with restricted privileges receive redacted versions of sensitive sections.
Automated Redaction & Overrides: Sensitive information is hidden from unauthorized users. Emergency overrides trigger instant email alerts to security teams for audit and follow-up.
Database Integration for User Data: Extracts user roles, facility access, and permissions from a SQL database (e.g., Azure SQL Server). By adjusting the connection parameters, this approach can also be applied to Postgres or other SQL databases.
Email Alerts via SMTP: Unauthorized access attempts generate automatic email alerts, using an SMTP connection for secure and immediate notification.
Architecture
The system comprises three main components:

Backend (Python, Flask, GPT-4O, Database, SMTP):

Flask API: Manages incoming HTTP requests, retrieves and processes clinical notes, and communicates with GPT-4O for note segmentation.
GPT-4O Integration: Leverages Azure OpenAI’s GPT-4O model to structure raw clinical notes into categorized sections.
Database Connectivity: Uses pyodbc to connect to a SQL database (Azure SQL Server in the provided example) and retrieve user data, roles, and facility information. Adjust connection parameters to support Postgres or other SQL engines.
Redaction & Role Mapping: Applies access rules based on database-derived roles to show only allowed sections, redacting restricted content.
Security Alerts (SMTP): Uses smtplib over SSL to securely send email notifications if unauthorized data requests are detected.
Frontend (React + Vite):

User Interface: Collects user input such as patient ID, role, and requested headers.
Requests & Display: Sends requests to the Flask API and displays processed, potentially redacted clinical notes.
Visual Indicators: Highlights accessible sections and indicates restricted areas if the user lacks proper authorization.
Data Sources & Storage:

Clinical Notes (JSON): Notes are currently stored in a JSON file for demonstration.
User Roles & Permissions (SQL DB): User and facility data is fetched from a SQL database. Adaptable to Postgres or other databases with minor configuration changes.
Installation & Setup
Backend Setup
Requirements:

Python 3.10+
pip for Python dependency management
Azure OpenAI API credentials (endpoint, deployment name, API key for GPT-4O)
Valid database connection credentials for user/facility data (Azure SQL Server or Postgres)
SMTP-enabled email account for sending alerts
Steps:

Navigate to backend directory:
bash
Copy code
cd backend
Install dependencies:
bash
Copy code
pip3 install -r requirements.txt
Set the required environment variables (if any) for OpenAI keys, SMTP server, and credentials.
Run the Flask application:
bash
Copy code
python3 app.py
The backend will run at http://localhost:5000 (in debug mode).

Frontend Setup
Requirements:

Node.js and npm
Vite (included in devDependencies)
A running backend on http://localhost:5000
Steps:

Navigate to frontend directory:
bash
Copy code
cd frontend
Install dependencies:
bash
Copy code
npm install
Start the development server:
bash
Copy code
npm run dev
Open http://localhost:5173 (or indicated port) in your browser to access the frontend UI.

Usage
Enter Patient ID and Headers (Optional):
In the frontend UI, enter a patient ID and optional headers to request specific sections of the clinical note.

Select User Role:
Choose a role (e.g., "Hospital" or "Internal") that determines which sections you can access. The available roles and their permissions come from the database.

Submit Request:
Click “Search” to send a request to the backend. The backend queries the database, processes the note via GPT-4O, determines accessible sections, and redacts unauthorized content.

If unauthorized headers are requested, they are redacted, and a security alert email is sent automatically.
Security & Compliance
Role-Based Controls: Ensures controlled visibility over sensitive PHI segments, enforced by database-derived user roles.
Redaction of Sensitive Information: PHI is automatically redacted for unauthorized users.
Email Alert System: Unauthorized access attempts trigger SMTP-based email notifications to a security team.
Future Enhancements
Full Database Logging: Implement a dedicated database to store audit logs of all accesses and overrides for security monitoring.
Custom User Groups: Allow clients to define their own user groups and permission sets, enhancing flexibility.
Refined AI-Powered Policies: Use GPT-4O prompts to define more granular rules tailored to different roles and data types.
