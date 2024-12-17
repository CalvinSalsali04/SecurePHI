import os
from openai import AzureOpenAI
import pandas as pd
import json

def process_clinical_note(note):

    """Read and process the clinical note.
    df = pd.read_json(input_file)
    note = df["clinical note"][patient_id]
    """
    note = note.replace("**", "")  # Remove asterisks

    # Trim note if necessary
    lines = note.strip().split("\n")
    if len(lines) > 0:
        note = "\n".join(lines[0:-1])  # Keep all but the last line if there are any lines

    return note

def call_gpt_model(note):
    """Call the Azure GPT model and get the processed output."""

    # Initialize Azure OpenAI client with key-based authentication
    endpoint = os.getenv("ENDPOINT_URL", "https://oai-use2-dcsvc-np-ssv.openai.azure.com/")
    deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4o-mini")
    subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "6e7a8ec72af64faebd44cc20b72f2153")

    client = AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=subscription_key,
        api_version="2024-06-01",
    )

    # Prepare the chat prompt
    chat_prompt = [{
    "role": "system",
    "content": "Hi, I'm an AI assistant. I can help you break down the clinical note into sections based on the identified headers and divide those sections into individual sentences.Please provide the clinical note you'd like me to analyze."
    },
    {"role" : "user",
     "content": [
         {"type" : "text",
          "text" : "Please format the sections by adding '###'' before each header and starting each sentence on a new line with ' - '. The first section should be 'Patient Information'. Here is the clinical note I want to analyze:"},
          {"type" : "text",
           "text" : note}]
    }]

    # Generate the completion
    completion = client.chat.completions.create(
        model=deployment,
        messages=chat_prompt,
        max_tokens=4096,
        temperature=0.7,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
        stream=False
    )

    return completion.choices[0].message.content

def post_process_output(gpt_retuned_note):

    """Post-process the output from the GPT model."""
    # Exclude the first line if necessary
    lines = gpt_retuned_note.strip().split("\n")
    if len(lines) > 0:
        trimmed_note = "\n".join(lines[1:])  # Exclude the first line
    else:
        trimmed_note = gpt_retuned_note  # Keep the original if no lines

    return trimmed_note


def extract_sections(trimmed_note,patient_id,list_of_access):
    sections = []
    section_id = 1

    # Process each line to create a dictionary for each section
    for index, line in enumerate(trimmed_note.split("\n")):
        if line.startswith("###"):
            # Remove the number and keep the header
            header = line.split(".", 1)[-1].strip()  # Get the header after "###"
            section_dict = {
                "id": section_id,
                "header": header.replace("###" ,"").strip(),
                "value": "",  # Initialize the value as empty; we'll fill it next
                "accessible": header.replace("###" ,"").strip() in list_of_access,
                "header_line_number": index + 1,  # Store the line number of the header
                "content_line_numbers": []  # Initialize a list for content line numbers
            }
            sections.append(section_dict)
            section_id += 1  # Increment the section ID
        else:
            # Add the line to the last section's value
            if sections:
                sections[-1]["value"] += line.strip() + " "  # Add line value and space for readability
                sections[-1]["content_line_numbers"].append(index + 1)  # Store the line number for the content

    final_json_structure = {
    "sections": sections
    }

    return final_json_structure

def has_access(user_role):

    access_roles = {
    1 :
    ["Patient Information", "History of Present Illness", "Chief Complaint",
    "Past Medical History","Medications", "Allergies", "Review of Systems", "Patient Education",
    "Physical Examination", "Assessment", "Plan", "Signature","Subjective","Objective"],

    2 :
    ["Chief Complaint", "Physical Examination", "Assessment", "Allergies","Social History","Plan","Subjective"]}

    return access_roles.get(user_role)

def gpt_model_note_division(note,user_role,patientid,required_headers=[]):
    try:

        if user_role not in [1, 2]:
            raise ValueError("User Role can only be 1 or 2")

        note = process_clinical_note(note)
        model_output = call_gpt_model(note)
        trimmed_note = post_process_output(model_output)
        list_of_access = has_access(user_role)
        sections = extract_sections(trimmed_note,patientid,list_of_access)

        list_of_access.extend(required_headers)

        return sections,trimmed_note,list_of_access

    except ValueError as e:
        print(f"Invalid input: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


def redact_sections(cleaned_note, sections, list_of_access):
    # Split the cleaned note into lines for easier manipulation
    lines = cleaned_note.strip().split('\n')

    # Create a set for quick lookup
    accessible_sections = set(list_of_access)

    # Iterate over the sections to determine which ones to redact
    redacted_lines = []
    current_section_header = None

    for line in lines:
        # Check if the line is a section header
        if line.startswith("###"):
            current_section_header = line.replace("###", "").strip()
            redacted_lines.append(line)  # Add header to redacted lines
        else:
            # Redact content if it's not in an accessible section
            if current_section_header and current_section_header not in accessible_sections:
                redacted_lines.append("[REDACTED]")
            else:
                redacted_lines.append(line)

    # Join the lines back into a single string
    redacted_note = "\n".join(redacted_lines)
    return redacted_note


