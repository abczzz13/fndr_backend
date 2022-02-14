import os


# Temporary script to set the environment variables
# Type: python env_var_script.py
os.environ["FLASK_APP"] = "fndr_backend.py"
os.environ["FLASK_ENV"] = "development"
os.environ["APP_SETTINGS"] = "config.DevelopmentConfig"
os.environ["POSTGRES_USER"] = "postgres"
os.environ["POSTGRES_PW"] = "aiYpDytgn8MwXEDcQvkU"
os.environ["POSTGRES_URL"] = "localhost:5432"
os.environ["POSTGRES_DB"] = "fndr_backend_dev"

print("Environment variables for fndr_backend set")

# Environment Variables from .env:
# FLASK_APP=fndr_backend.py
# FLASK_ENV=development
# APP_SETTINGS=config.DevelopmentConfig
# POSTGRES_USER="postgres"
# POSTGRES_PW="aiYpDytgn8MwXEDcQvkU"
# POSTGRES_URL="localhost:5432"
# POSTGRES_DB="fndr_backend_dev"
