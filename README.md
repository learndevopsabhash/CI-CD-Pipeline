# Flask CI/CD Pipeline

This repository contains a simple Flask application and a GitHub Actions workflow that automatically tests, builds, and deploys it.

## Workflow Overview

The GitHub Actions pipeline performs the following steps:

1. Checks out the repository
2. Sets up Python 3.11
3. Installs dependencies from requirements.txt
4. Runs the test suite with pytest
5. Builds a deployable artifact in the dist folder
6. Deploys to the staging branch environment when changes are pushed to the staging branch
7. Deploys to production when a version tag starting with v is created

## Required GitHub Secrets

Add the following secrets in your GitHub repository under Settings > Secrets and variables > Actions:

- STAGING_HOST
- STAGING_USERNAME
- STAGING_DEPLOY_KEY
- PROD_HOST
- PROD_USERNAME
- PROD_DEPLOY_KEY

These secrets are used by the deployment steps. If they are not configured, the workflow will print a message and skip deployment gracefully.

## Local Development

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use .venv\Scripts\activate
pip install -r requirements.txt
pytest -q
python app.py
```

## Branch Strategy

- main: mainline development branch
- staging: pre-production validation branch
- Tags like v1.0.0: trigger production deployment
