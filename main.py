import warnings
warnings.filterwarnings("ignore")
import os
from utils import get_openai_api_key
from IPython.display import Markdown
from crewai import Agent, Task, Crew
from crewai_tools import WebsiteSearchTool, SerperDevTool

import os
import json
from utils import get_openai_api_key, pretty_print_result
from utils import get_serper_api_key

openai_api_key = get_openai_api_key()
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4-turbo'
os.environ["SERPER_API_KEY"] = get_serper_api_key()

university_name = "Iowa State University"

# Initialize tools
web_tool = WebsiteSearchTool()
search_tool = SerperDevTool()

contact_list = []

# Create data collection agent
data_collection_agent = Agent(
    role="Data Collector",
    goal="Collect PhD student information from ISU's CS department",
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
    backstory="""You are a meticulous data reviewer who ensures all collected information
    is valid and meets the required format. You specifically check for valid email addresses
    and complete names.""",
    verbose=True,
    allow_delegation=True
)


def custom_message(name):
    return f'''
SUBJECT LINE: Intro from Mercor

Hey {name},

I hope you're well! My name is Akhilesh, and I'm an undergrad at Iowa State. I’m on the growth team at Mercor, a startup based in San Francisco. 

We hire PhDs to provide feedback to AI models for top AI labs and have paid over $10M to people on our platform. We're launching a part-time project with CS/AI/ML PhDs and PhD candidates this spring for a leading AI lab, and are paying participants $50-100 per hour.

Would you be interested in joining?

Best,
Akhilesh
'''

# Create task for data collection
collection_task = Task(
    description="""
        1. Go to https://www.cs.iastate.edu/people/phd-students
        2. For the first 150 PhD students on the page with a valid email address, None does not count:
           - Extract their full name
           - Extract their email address
           - Continue with next student
        3. Format the data as a list of JSON objects with this structure:
           [{"name": "Student Name", "email": "student@iastate.edu"}, ...]
        4. Return only the list in the format mentioned above
        """,
    agent=data_collection_agent,
    expected_output="A JSON array containing student information"
)


review_task = Task(
    description="""
    1. Review the collected student data
    2. Verify each entry has:
       - A valid name (not empty or None)
       - A valid email address (must be like the follwoing:  @<some-school>.edu)
    3. Remove any entries with invalid or None emails
    4. If more than 25% of entries are invalid, delegate back to collection agent
    5. Return the cleaned data in the same JSON format
    6. Ensure the JSON array is complete and properly terminated
    """,
    agent=data_review_agent,
    expected_output="A validated JSON array containing only valid student information"
)

# Create crew
crew = Crew(
    agents=[data_collection_agent, data_review_agent],
    tasks=[collection_task, review_task],
    verbose=True
)

def collect_email_processor():
    for contact in contact_list:
        if(contact["email"] is not 'None'):
            contact["outreach_message"] = custom_message(contact["name"])


def add_outreach_to_doc():
    # Create outreach directory if it doesn't exist
    if not os.path.exists('outreach'):
        os.makedirs('outreach')
        
    for contact in contact_list:
        if contact["email"] is not 'None':
            # Create file name from person's name
            file_name = contact["name"].replace(" ", "_").lower() + ".txt"
            file_path = os.path.join('outreach', file_name)
            
            with open(file_path, 'w') as file:
                # Write email as heading
                file.write(f"Email: {contact['email']}\n")
                file.write("-" * 50 + "\n\n")  # Separator line
                # Write outreach message
                file.write(contact["outreach_message"])
                
    print("Outreach messages added to individual files in outreach folder")

def main():
    result = (crew.kickoff()) # defined globally on top! 
    json_data = json.loads(result.raw)  # Parse the raw JSON string
    contact_list.extend(json_data)  # Add the parsed data to contact_list
    print("The result exactly is: ", contact_list)
    collect_email_processor()
    add_outreach_to_doc()

if __name__ == "__main__":
    main()















