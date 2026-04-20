Assignment tasks provided :

Creating a python script for -
1. Registers a participant to an existing CP
2. Registers a visit to the newly added participant
3. Creates a primary specimen and 5 aliquots

This script automates the end-to-end workflow in OpenSpecimen using the REST API. It authenticates a session, registers a new participant, records a clinical visit, and handles the collection of primary specimens and their subsequent aliquots.

## Key FeaturesSession Management: 
Uses a persistent requests.
Session to handle authentication tokens and headers efficiently.
Automated Workflow: Executes four major steps in a single run:
Participant Registration: Creates a new record in a specific Collection Protocol (CP).
Visit Creation: Logs a clinical event (e.g., "Operative") for the participant.
Primary Specimen Collection: Registers a new "Fluid" specimen (Bone Marrow Plasma).
Bulk Aliquotting: Uses a loop and the specimens/collect endpoint to generate 5 aliquots in one API call.

## Technical Implementation
The implementation relies on several key REST API interactions. It first performs Authentication by exchanging credentials for a secure API token. Participant Registration links the user to the protocol, followed by Visit Management to define the clinical encounter.

The core specimen logic uses the Create Specimen endpoint for the primary sample and the Specimen Collect endpoint for the aliquots. The script ensures high data quality by using ISO 8601 UTC timestamps for the createdOn fields and carefully managing the parentId to maintain the biological hierarchy.

Field Highlights
lineage: Tracks the relationship between the primary sample (New) and its children (Aliquot).
createdOn: Utilizes ISO 8601 UTC timestamps for precise tracking.
parentId: Explicitly links the 5 aliquots back to the primary specimen ID.

## Setup & UsageConfigure Credentials:
Update LOGIN_NAME, PASSWORD, and BASE_URL.
Set IDs: Ensure CP_ID and SITE_NAME match your specific OpenSpecimen instance configuration.

Run:
'''
python openspecimen_workflow.py
'''
