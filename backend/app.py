from flask import Flask, jsonify, request
import json
from gpt_model.model import *
import pandas as pd
from flask_cors import CORS
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)
CORS(app)

session = {}


# email config
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
SENDER_EMAIL = "pcchackathon@gmail.com"
SENDER_PASSWORD = "lqypiswihcbzyjwt"
RECEIVER_EMAIL = "pcchackathon@gmail.com"

def send_alert(alert_type, message, patient_id=None):
    if alert_type == "security":
        # Compose the email content
        subject = "Security Alert: Unauthorized Access Attempt Detected"
        body = f"Security Alert:\n\n{message}\n\nPlease investigate this issue."

        # Debugging output
        print("Preparing to send email...")

        # Set up the email message
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Send the email
        try:
            print("Connecting to SMTP server...")
            with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
                print("Starting TLS...")
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                print("Logged into SMTP server.")
                server.send_message(msg)
                print("Security alert email sent successfully.")
        except Exception as e:
            print(f"Failed to send email alert: {e}")


@app.route('/clinical_notes', methods=['GET'])
def get_clinical_notes():
    patient_id = int(request.args.get('patient_id'))
    user_role = int(request.args.get('user_role'))
    required_headers = request.args.getlist('required_header')

    valid_headers = [
            "Patient Information", "Chief Complaint", "History of Present Illness",
            "Past Medical History", "Medications", "Allergies", "Social History",
            "Review of Systems", "Physical Examination", "Assessment", "Patient Education",
            "Plan", "Signature", "Subjective", "Objective"]

    valid_required_headers = [header for header in required_headers if header in valid_headers]
    list_of_access = has_access(user_role)
    unauthorized_headers = [header for header in valid_required_headers if header not in list_of_access]

    # trigger security alert if there are unauthorized headers
    if unauthorized_headers:
        alert_message = (f"User with role {user_role} attempted to access unauthorized headers "
                         f"for patient_id {patient_id}: {', '.join(unauthorized_headers)}")
        send_alert("security", alert_message)


    # check if user is requesting already processed notes with any required headers
    if patient_id in session:
        list_of_access = has_access(user_role) + required_headers
        redacted_note = redact_sections(session[patient_id][0], session[patient_id][1], list_of_access)
        headers_flag = session.get(patient_id, {})[3]

        '''
        for header in headers_flag:
            headers_flag[header] = False

        for header in list_of_access:
            headers_flag[header] = True
        '''

        return jsonify({'patientId': patient_id, 'clinicalNotes': redacted_note.replace("### ", ""),'accesible_section': headers_flag}), 200

    # load clinical notes (from json file for now)
    try:
        clinical_notes_db = pd.read_json("clinical_notes.json")

    except FileNotFoundError:
        return jsonify({'error': 'Clinical Notes DB file not found'}), 500
    except json.JSONDecodeError:
        return jsonify({'error': 'Cannot decode Clinical Notes DB JSON file'}), 500

    if patient_id > len(clinical_notes_db) or patient_id < 1:
        return jsonify({'error': 'Incorrect patient_id field'}), 400

    # check if clinical notes exist for the patient_id and return redacted notes
    if not clinical_notes_db.empty:
        note =  clinical_notes_db["clinical note"][patient_id]
        sections, cleaned_note, list_of_access = gpt_model_note_division(note, user_role,patient_id, required_headers)
        headers_flag={}
        for i in sections["sections"]:
            headers_flag[i['header']] = i['accessible']

        redacted_note = redact_sections(cleaned_note, sections, list_of_access)

        session[patient_id] = (cleaned_note, sections, list_of_access, headers_flag)

        return jsonify({'patientId': patient_id, 'clinicalNotes': redacted_note.replace("### ", ""),'accesible_section':headers_flag}), 200
    else:
        return jsonify({'error': f'No clinical notes found for patient id: {patient_id}'}), 404


if __name__ == "__main__":
    app.run(debug=True)
