# GitHub Activity Monitor

This script checks volunteer GitHub activity (commits) in specified repositories. It sends an email to HR if any volunteers haven't made updates in the last 2 weeks.

## Features
- Uses GitHub REST API to check commits
- Sends summary emails via SMTP
- Automatically runs weekly via GitHub Actions

## Setup

### 1. Clone this repo and install dependencies:
```bash
pip install -r requirements.txt
```

## Status
Currently testing with demo projects. Yet to deploy.