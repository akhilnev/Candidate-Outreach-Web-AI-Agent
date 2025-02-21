# Email Outreach Automation Script Documentation

## Overview
This script automates outreach workflow

## Prerequisites
- Python 3.x
- Required packages: crewai, warnings, os, json, re
- API Keys:
  - OpenAI API key
  - Serper API key

## Configuration
The script uses a CONFIG dictionary with the following customizable settings:

1. University Settings:
   - name: University name
   - department: Department name
   - student_url: URL to student directory
   - email_domain: University email domain

2. Outreach Settings:
   - num_students: Number of students to contact
   - bcc_email: BCC email address
   - sender_name: Your name
   - sender_title: Your title
   - message_template: Email template

## Usage

1. Install Dependencies:

### Install from requirements.txt ( Its uncleaned rn!)
pip install -r requirements.txt

### Or install individual packages
pip install crewai warnings os json re

2. Set up API Keys:
   - Ensure your API keys are properly configured in utils.py
   - Required: OpenAI API key and Serper API key

3. Run the Script:

bash
python main.py

## Output
The script will:
1. Collect student information from the specified URL
2. Validate email addresses and names
3. Generate personalized outreach messages
4. Create individual text files in the 'outreach/physics' directory for each contact
   - File format: firstname_lastname.txt
   - Contains: Email, BCC, and personalized message

## Error Handling
- The script includes JSON parsing error handling
- Failed operations are logged to console
- Invalid entries are automatically filtered out


## Notes
- The script uses AI agents for data collection and validation
- Ensures email addresses match the specified university domain
- Automatically creates the outreach directory if it doesn't exist
- Skips entries with invalid or missing email addresses

## Troubleshooting
If you encounter errors:
1. Check API key configuration
2. Verify internet connection
3. Ensure the student directory URL is accessible
4. Check console output for specific error messages

Feel free to modify based on your need! 


