# Importing Necessary Libraries

## System / Environment Management
import os
from dotenv import load_dotenv
from config import REPO_OWNER, REPO_NAME, DIRECTORY_PATH, DAYS_BACK, MAIL_TO

## Networking / API Requests
import requests

## Email Handling
import smtplib
from email.mime.text import MIMEText

## Date and Time
from datetime import datetime, timedelta

'''
----------x----------x----------x----------
'''

# Load local .env for testing
# Uncomment the following line when testing locally to load environment variables from .env file
load_dotenv()

# Email config from environment variables
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

'''
----------x----------x----------x----------
'''

HEADERS = {
    "Accept": "application/vnd.github.v3+json"
}
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"Bearer {GITHUB_TOKEN}"

# Time window
since_date = (datetime.utcnow() - timedelta(days=DAYS_BACK)).isoformat() + "Z"

# GitHub API request
url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/commits"
params = {"since": since_date, "path": DIRECTORY_PATH}
response = requests.get(url, headers=HEADERS, params=params)

# Build contributor list
contributors = {}

if response.status_code == 200:
    for commit in response.json():
        author = commit["commit"]["author"]
        name = author.get("name", "Unknown")
        email = author.get("email", "N/A")
        date = author.get("date", "")
        message = commit["commit"]["message"]

        key = f"{name} <{email}>"
        if key not in contributors:
            contributors[key] = []

        contributors[key].append(f"{date} – {message}")
else:
    print("❌ GitHub API error:", response.status_code)
    exit(1)

# Compose the message
if contributors:
    msg_body = f"✅ Contributors active in '{DIRECTORY_PATH}' over the past {DAYS_BACK} days:\n\n"
    for person, entries in contributors.items():
        msg_body += f"{person}\n"
        for entry in entries:
            msg_body += f"  - {entry}\n"
        msg_body += "\n"
else:
    msg_body = f"⚠️ No commit activity in '{DIRECTORY_PATH}' in the past {DAYS_BACK} days."

print(msg_body)

msg = MIMEText(msg_body)
print(msg)


# Send the email
msg = MIMEText(msg_body)
msg["Subject"] = f"[Activity Report] GitHub Contributors in '{DIRECTORY_PATH}'"
msg["From"] = EMAIL_USER
msg["To"] = MAIL_TO

try:
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, [MAIL_TO], msg.as_string())
        print("✅ Report emailed to HR.")
except Exception as e:
    print(f"❌ Failed to send email: {e}")