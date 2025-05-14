Conversational Sales Agent
This project is a conversational sales agent built for Zikra Infotech, using Python and Google ADK (gemini-2.0-flash). It collects lead information (age, country, interest) after obtaining consent, handles multiple chats concurrently, follows up after 10 seconds if a lead doesn't respond, and saves data in leads.csv. The project meets all Zikra requirements, including functionality, ADK integration, and data persistence.
Project Structure

agent.py: Main script containing the chatbot logic, using ADK to process responses and manage conversations.
simulate_leads.py: Test script that simulates three leads (Alice, Bob, Charlie) to demonstrate multi-lead handling and follow-ups.
leads.csv: Stores lead data (lead_id, name, age, country, interest, status).
__init__.py: Makes the directory a Python package.
.env: Stores the Google API key (not included in Git).
README.md: This file.

Prerequisites

Python 3.8+: Install from python.org.
Google ADK: Requires a Google API key for gemini-2.0-flash.
Dependencies: Listed in requirements.txt (assumed, create if needed).

Setup Instructions

Clone the Repository:
            git clone https://github.com/Salahuddin-Qureshi/sales_agent
            cd sales_agent


Set Up a Virtual Environment:
python -m venv .venv
.\.venv\Scripts\Activate.ps1


Install Dependencies:
pip install google-adk python-dotenv


Configure the Google API Key:

Create a .env file in sales_agent/ with:GOOGLE_API_KEY=your_google_api_key_here


Obtain the key from Google Cloud Console.



Running the Project
Option 1: Interactive Mode (agent.py)
Run the chatbot interactively to test it with your own responses.

In the terminal, navigate to sales_agent/:cd D:\Zikra\sales_agent


Activate the virtual environment (if not already active):


Run the script:python .\agent.py


Follow the prompts:
Enter your name (e.g., "Test").
Respond to questions (e.g., "sure" for consent, "25" for age).
Expected output: The chatbot asks for consent, age, country, and interest, saving responses to leads.csv with status secured or no_response.



Option 2: Simulation Mode (simulate_leads.py)
Test the chatbot with three predefined leads (Alice, Bob, Charlie) to demonstrate multi-lead handling and follow-ups.

In the terminal, navigate to sales_agent/:cd D:\Zikra\sales_agent


Activate the virtual environment (if not already active):


Run the script:python .\simulate_leads.py


Expected output:
Alice: Answers all questions (age=30, country=USA, interest=Software), status secured.
Bob: Declines consent ("no"), status no_response.
Charlie: Agrees ("yes") but stops, triggering a follow-up after ~10 seconds, status followed_up.
Data is saved in leads.csv.



Expected Output

Console: Chat messages (e.g., "Agent to Alice: What is your age?") and follow-ups (e.g., "Just checking in to see if you're still interested, Charlie.").
leads.csv: Updated with lead data, e.g.:lead_id,name,age,country,interest,status
<uuid>,Alice,30,USA,Software,secured
<uuid>,Bob,,,no_response
<uuid>,Charlie,,,followed_up



Video Demonstration
A 9 minute video demo is available 

Shows interactive and simulation modes.
Explains the code, focusing on agent.py’s sales_conversation and follow_up_check functions.
Demonstrates multi-lead handling and data storage.

Notes

The consent message in agent.py’s interactive mode is slightly modified ("I'd like to gather some information...") but functions as required.
The project uses threading for concurrent chats and csv_lock for safe data storage.
For issues, contact me at salahuddinq.cs@gmail.com.

Acknowledgments
Thank you, Zikra Infotech, for this opportunity to showcase my skills!
