from langchain_openai import ChatOpenAI
from browser_use import Agent as Browser_Agent
import asyncio
from dotenv import load_dotenv
import json
import os

load_dotenv()

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

contact_list = [
    {
        "name": "Waqwoya Abebe",
        "email": "wmabebe@iastate.edu"
    },
    {
        "name": "Ali Adibifar",
        "email": "deris@iastate.edu"
    },
    {
        "name": "Jobayer Ahmmed",
        "email": "jobayer@iastate.edu"
    },
    {
        "name": "Abdullah Al Asif",
        "email": "aaasif@iastate.edu"
    },
    {
        "name": "Muhammad Arshad",
        "email": "arbab@iastate.edu"
    },
    {
        "name": "Modeste Atsague",
        "email": "modeste@iastate.edu"
    },
    {
        "name": "Priyanka Banerjee",
        "email": "pb11@iastate.edu"
    },
    {
        "name": "Aobo Chen",
        "email": "aobo@iastate.edu"
    },
    {
        "name": "Jiajun Chen",
        "email": "jiajunch@iastate.edu"
    },
    {
        "name": "Michael Qi Yin Chen",
        "email": "mqychen@iastate.edu"
    },
    {
        "name": "Le Chen",
        "email": "lechen@iastate.edu"
    },
    {
        "name": "Feifei Cheng",
        "email": "fch777@iastate.edu"
    },
    {
        "name": "Joseph Clanin",
        "email": "jsc@iastate.edu"
    },
    {
        "name": "Isaak N Daniels",
        "email": "isaakd@iastate.edu"
    },
    {
        "name": "Lichuan Deng",
        "email": "lcdeng@iastate.edu"
    },
    {
        "name": "Rebecca Eiland",
        "email": "reiland@iastate.edu"
    },
    {
        "name": "Joshua Ellis",
        "email": "jde314@iastate.edu"
    },
    {
        "name": "Olukorede Fakorede",
        "email": "fakorede@iastate.edu"
    },
    {
        "name": "Haniyeh Fekrmandi",
        "email": "haniyehf@iastate.edu"
    },
    {
        "name": "Jiale Feng",
        "email": "colour@iastate.edu"
    }
]

async def collect_student_info():
    agent = Browser_Agent(
        task="""
        1. Go to https://www.cs.iastate.edu/people/phd-students
        2. For the first 50 PhD students on the page:
           - Only if email ID exists, extract their full name
           - Extract their full name
           - Extract their email address
           - Continue with next student
        3. Format the data as a list of JSON objects with this structure:
           [{"name": "Student Name", "email": "student@iastate.edu"}, ...]
        4. Return only the list in the format mentioned above
        """,
        llm=ChatOpenAI(model="gpt-4o"),
        use_vision=True,
    )

    try:
        result = await agent.run()
        
        # Write results to contact_list.txt
        with open('contact_list.txt', 'w') as f:
            json.dump(result, f, indent=2)
        print("Successfully wrote results to contact_list.txt")
            
        # Read and parse the file
        with open('contact_list.txt', 'r') as f:
            parsed_contacts = json.load(f)
            
        # Extend contact_list with parsed data
        contact_list.extend(parsed_contacts)
        print(f"Successfully loaded {len(parsed_contacts)} student contacts")
        print("Contact List:", contact_list)
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")



def collect_email_processor():
    for contact in contact_list:
        if(contact["email"] is not None):
            contact["outreach_message"] = custom_message(contact["name"])


def add_outreach_to_doc():
    # Create outreach directory if it doesn't exist
    if not os.path.exists('outreach'):
        os.makedirs('outreach')
        
    for contact in contact_list:
        if contact["email"] is not None:
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


async def main():
    await collect_student_info()
    # collect_email_processor()
    # add_outreach_to_doc()

if __name__ == "__main__":
    asyncio.run(main())
