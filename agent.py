import csv
import threading
import time
import uuid
from datetime import datetime, timedelta
from google.adk.agents import Agent
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Store lead data, timers, and lock for safe CSV writing
lead_states = {}
timers = {}  # Store timers to prevent garbage collection
csv_lock = threading.Lock()

# Create leads.csv with headers if it doesn't exist
def initialize_csv():
    with csv_lock:
        try:
            with open('leads.csv', 'x', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['lead_id', 'name', 'age', 'country', 'interest', 'status'])
        except FileExistsError:
            pass

# Update lead data in CSV
def update_lead_in_csv(lead_id, name, age=None, country=None, interest=None, status='pending'):
    with csv_lock:
        temp_data = []
        updated = False
        try:
            with open('leads.csv', 'r', newline='') as f:
                reader = csv.reader(f)
                temp_data = list(reader)
                for row in temp_data[1:]:  # Skip header
                    if row[0] == lead_id:
                        row[1] = name or ''
                        row[2] = age or row[2]
                        row[3] = country or row[3]
                        row[4] = interest or row[4]
                        row[5] = status
                        updated = True
                        break
        except FileNotFoundError:
            initialize_csv()
        if not updated:
            temp_data.append([lead_id, name or '', age or '', country or '', interest or '', status])
        with open('leads.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(temp_data)

# Check for unresponsive leads
def follow_up_check(lead_id, agent):
    lead = lead_states.get(lead_id, {})
    last_interaction = lead.get('last_interaction', datetime.now())
    name = lead.get('name', 'there')
    if datetime.now() - last_interaction > timedelta(seconds=10):
        if lead.get('status') not in ['secured', 'no_response']:
            print(f"Follow-up for {lead_id}: Just checking in to see if you're still interested, {name}.")
            lead['status'] = 'followed_up'
            update_lead_in_csv(lead_id, name, lead.get('age'), lead.get('country'), lead.get('interest'), 'followed_up')
    # Reschedule if still pending
    if lead.get('status') not in ['secured', 'no_response']:
        timer = threading.Timer(10, follow_up_check, args=(lead_id, agent))
        timers[lead_id] = timer  # Store timer reference
        timer.start()
        print(f"Scheduled follow-up for {lead_id} in 10 seconds")

# Process response with ADK (simplified due to API uncertainty)
def process_response_with_adk(agent, response, context):
    response = response.lower().strip()
    if context['step'] == 'consent':
        positive = ['yes', 'y', 'sure', 'ok', 'okay', 'yep', 'yeah']
        negative = ['no', 'n', 'nope', 'nah', 'not interested']
        if any(word in response for word in positive):
            return 'yes'
        elif any(word in response for word in negative):
            return 'no'
        else:
            return 'invalid'
    return response

# Handle sales conversation
def sales_conversation(lead_id, name, response, agent):
    lead = lead_states.setdefault(lead_id, {
        'name': name,
        'status': 'pending',
        'step': 'consent',
        'last_interaction': datetime.now()
    })

    # Process response with ADK
    context = {'step': lead['step']}
    processed_response = process_response_with_adk(agent, response, context)

    # Update CSV with current state
    update_lead_in_csv(lead_id, name, status=lead['status'])

    if lead['status'] in ['secured', 'no_response']:
        return lead['status']

    # Consent step
    if lead['step'] == 'consent':
        if processed_response == 'start':
            print(f"Agent to {name}: Hey {name}, thank you for filling out the form. Is that okay?")
            return "Awaiting consent"
        elif processed_response == 'yes':
            lead['step'] = 'age'
            lead['last_interaction'] = datetime.now()
            timer = threading.Timer(10, follow_up_check, args=(lead_id, agent))
            timers[lead_id] = timer  # Store timer reference
            timer.start()
            print(f"Scheduled follow-up for {lead_id} in 10 seconds")
            update_lead_in_csv(lead_id, name)
            print(f"Agent to {name}: Great, {name}! Let's get started.")
            return f"What is your age, {name}?"
        elif processed_response == 'invalid':
            print(f"Agent to {name}: Sorry, I didn't understand. Could you please say 'yes' or 'no'?")
            return "Awaiting consent"
        else:
            lead['status'] = 'no_response'
            lead['last_interaction'] = datetime.now()
            update_lead_in_csv(lead_id, name, status='no_response')
            print(f"Agent to {name}: Alright, no problem, {name}. Have a great day!")
            return "no_response"

    # Sequential questions
    if lead['step'] == 'age':
        lead['age'] = processed_response
        lead['step'] = 'country'
        lead['last_interaction'] = datetime.now()
        update_lead_in_csv(lead_id, name, age=processed_response)
        return f"Which country are you from, {name}?"
    elif lead['step'] == 'country':
        lead['country'] = processed_response
        lead['step'] = 'interest'
        lead['last_interaction'] = datetime.now()
        update_lead_in_csv(lead_id, name, age=lead.get('age'), country=processed_response)
        return f"What product or service are you interested in, {name}?"
    elif lead['step'] == 'interest':
        lead['interest'] = processed_response
        lead['status'] = 'secured'
        lead['last_interaction'] = datetime.now()
        update_lead_in_csv(lead_id, name, age=lead.get('age'), country=lead.get('country'), interest=processed_response, status='secured')
        print(f"Agent to {name}: Thank you for providing the information, {name}!")
        return "secured"

    return "Please respond to the current question."

# Define ADK agent
root_agent = Agent(
    name="sales_agent",
    model="gemini-2.0-flash",
    description="Robotic sales agent to collect lead information interactively.",
    instruction="Collect lead information (age, country, interest) step-by-step after obtaining consent. Start with 'Hey [Lead Name], thank you for filling out the form. Is that okay?'. Use natural language processing to handle varied user inputs. Follow up if no response in 24 hours (10 seconds for testing).",
    tools=[sales_conversation]
)

# Initialize CSV
initialize_csv()

# Interactive chatbot mode
if __name__ == "__main__":
    lead_id = str(uuid.uuid4())
    name = input("Please provide your name: ")
    lead_states[lead_id] = {
        'name': name,
        'status': 'pending',
        'step': 'consent',
        'last_interaction': datetime.now()
    }
    print(f"Agent to {name}: Hey {name}, thank you for filling out the form. I'd like to gather some information from you. Is that okay?")
    while True:
        try:
            user_input = input("Your response: ")
            response = sales_conversation(lead_id, name, user_input, root_agent)
            if response not in ["Awaiting consent"]:
                print(f"Agent to {name}: {response}")
            if response in ["secured", "no_response"]:
                break
        except KeyboardInterrupt:
            print(f"\nAgent to {name}: Goodbye, {name}!")
            break