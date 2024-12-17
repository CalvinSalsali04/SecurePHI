# Installation
- Required Python=3.10 

- To install the required dependencies, run the following command:

    pip3 install -r requirements.txt

# Call Main Function
To call the main function "gpt_model_note_division" and get the extracted sections, cleaned note, and list of accessible sections, you can use the following code:

#Import necessary functions from the code file  
from model import gpt_model_note_division  
  
#Set the patient ID and user role  
patient_id = int(0)
user_role = int(1)  
  
#Call the main function  
sections, cleaned_note, list_of_access = gpt_model_note_division(patient_id, user_role) 
