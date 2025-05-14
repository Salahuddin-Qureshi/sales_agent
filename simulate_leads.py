
import threading
import time
import uuid
from agent import root_agent, sales_conversation

# Simulate a lead submission
def simulate_lead_submission(name):
    lead_id = str(uuid.uuid4())
    print(f"New lead: {lead_id}, Name: {name}")
    threading.Thread(target=process_lead, args=(lead_id, name)).start()

# Process lead conversation
def process_lead(lead_id, name):
    # Start conversation
    response = sales_conversation(lead_id=lead_id, name=name, response="start", agent=root_agent)
    if response != "Awaiting consent":
        print(f"Agent to {name}: {response}")

    # Simulate responses
    if name == "Alice":
        # Full conversation
        responses = ["yes", "30", "USA", "Software"]
        for resp in responses:
            time.sleep(2)
            response = sales_conversation(lead_id=lead_id, name=name, response=resp, agent=root_agent)
            if response not in ["secured", "no_response", "Awaiting consent"]:
                print(f"Agent to {name}: {response}")
    elif name == "Bob":
        # No consent
        time.sleep(2)
        response = sales_conversation(lead_id=lead_id, name=name, response="no", agent=root_agent)
        if response not in ["secured", "no_response", "Awaiting consent"]:
            print(f"Agent to {name}: {response}")
    elif name == "Charlie":
        # Unresponsive (for follow-up)
        time.sleep(2)
        response = sales_conversation(lead_id=lead_id, name=name, response="yes", agent=root_agent)
        if response not in ["secured", "no_response", "Awaiting consent"]:
            print(f"Agent to {name}: {response}")

# Simulate multiple leads
def main():
    leads = ["Alice", "Bob", "Charlie"]
    for name in leads:
        simulate_lead_submission(name)
        time.sleep(1)

if __name__ == "__main__":
    main()
    time.sleep(20)  # Increased to ensure follow-ups