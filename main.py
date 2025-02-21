import warnings
warnings.filterwarnings("ignore")
import os
from utils import get_openai_api_key, get_serper_api_key
from crewai import Agent, Task, Crew
from crewai_tools import WebsiteSearchTool, SerperDevTool
import json
import re

# Configuration
CONFIG = {
    "university": {
        "name": "Iowa State University",
        "department": "Physics and Astronomy",
        "student_url": "https://www.physastro.iastate.edu/people/graduate-students",
        "email_domain": "iastate.edu"
    },
    "outreach": {
        "num_students": 50,
        "bcc_email": "fez.zafar@mercor.com",
        "sender_name": "Akhilesh",
        "sender_title": "senior at Iowa State"
    },
    "message_template": """
SUBJECT LINE: Intro from Mercor

Hey {name},

I hope you're well! My name is {sender_name}, and I'm an {sender_title}. I'm on the growth team at Mercor, a startup based in San Francisco. 

We hire Specialists in their fields to provide feedback to AI models for top AI labs and have paid over $10M to people on our platform. We're launching a part-time project with STEM Candidates this spring for a leading AI lab, and are paying participants $50 per hour. If you're interested, please apply here asap. We get back very soon!: |https://mercor.com/jobs/list_AAABlNMG_VFPYLU09nlIVqgZ?referralCode=8d5e90f3-a06f-414f-9cf4-9bce6fbbb844

Best,
{sender_name}
"""
}

# Initialize tools
web_tool = WebsiteSearchTool()
search_tool = SerperDevTool()

contact_list = []

# Create data collection agent
data_collection_agent = Agent(
    role="Data Collector",
    goal=f"Collect PhD student information from {CONFIG['university']['name']}'s {CONFIG['university']['department']} department",
    backstory="""You are an expert data collector specializing in academic information.
    Your task is to collect names and emails of PhD students.""",
    tools=[web_tool, search_tool],
    verbose=True,
    allow_delegation=False
)

# Create data review agent
data_review_agent = Agent(
    role="Data Reviewer",
    goal="Ensure all collected data is valid and complete",
    backstory=f"""You are a meticulous data reviewer who ensures all collected information
    is valid and meets the required format. You specifically check for valid email addresses
    ending in @{CONFIG['university']['email_domain']} and complete names.""",
    verbose=True,
    allow_delegation=True
)

def create_collection_task():
    return Task(
        description=f"""
        1. Go to {CONFIG['university']['student_url']}
        2. For the first {CONFIG['outreach']['num_students']} PhD students on the page with a valid email address:
           - Extract their full name
           - Extract their email address
           - Continue with next student
        3. Format the data as a list of JSON objects with this structure:
           [{{"name": "Student Name", "email": "student@{CONFIG['university']['email_domain']}"}}]
        4. Return only the list in the format mentioned above
        """,
        agent=data_collection_agent,
        expected_output="A JSON array containing student information"
    )

def create_review_task():
    return Task(
        description=f"""
        1. Review the collected student data
        2. Verify each entry has:
           - A valid name (not empty or None)
           - A valid email address (must end with @{CONFIG['university']['email_domain']})
        3. Remove any entries with invalid or None emails
        4. If more than 25% of entries are invalid, delegate back to collection agent
        5. Return the cleaned data in the same JSON format
        """,
        agent=data_review_agent,
        expected_output="A validated JSON array containing only valid student information"
    )

def custom_message(name):
    return CONFIG['message_template'].format(
        name=name,
        sender_name=CONFIG['outreach']['sender_name'],
        sender_title=CONFIG['outreach']['sender_title']
    )

def collect_email_processor():
    for contact in contact_list:
        if contact["email"] is not None:
            contact["outreach_message"] = custom_message(contact["name"])

def add_outreach_to_doc():
    if not os.path.exists('outreach/physics'):
        os.makedirs('outreach/physics')
        
    for contact in contact_list:
        if contact["email"] is not None:
            file_name = contact["name"].replace(" ", "_").lower() + ".txt"
            file_path = os.path.join('outreach/physics', file_name)
            
            with open(file_path, 'w') as file:
                file.write(f"Email: {contact['email']}\n")
                file.write(f"BCC: {CONFIG['outreach']['bcc_email']}\n")
                file.write("-" * 50 + "\n\n")
                file.write(contact["outreach_message"])
                
    print("Outreach messages added to individual files in outreach folder")

def clean_json_string(raw_string):
    """Clean and extract JSON array from the raw string"""
    try:
        # Try to find a JSON array in the string
        json_match = re.search(r'\[.*?\]', raw_string, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            # Parse the extracted JSON array
            return json.loads(json_str)
    except Exception as e:
        print(f"Error cleaning JSON string: {e}")
        print("Raw string:", raw_string)
    return None

def main():
    # Create crew
    crew = Crew(
        agents=[data_collection_agent, data_review_agent],
        tasks=[create_collection_task(), create_review_task()],
        verbose=True
    )
    
    try:
        result = crew.kickoff()
        # First try direct JSON parsing
        try:
            json_data = json.loads(result.raw)
        except json.JSONDecodeError:
            # If direct parsing fails, try cleaning the string
            print("Initial JSON parsing failed. Attempting to clean the data...")
            json_data = clean_json_string(result.raw)
            
            if json_data is None:
                print("Failed to parse JSON data. Please check the raw output.")
                return
        
        contact_list.extend(json_data)
        print("Collected contacts:", json.dumps(contact_list, indent=2))
        
        collect_email_processor()
        add_outreach_to_doc()
        
    except Exception as e:
        print(f"Error in main execution: {e}")
        print("Raw result:", result.raw if 'result' in locals() else "No result available")

if __name__ == "__main__":
    main()















