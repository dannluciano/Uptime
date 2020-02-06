#!/usr/bin/env python
import os

DELAY = 60  # Delay between site queries
ALERT_INTERVAL = 1800  # Delay between alert emails

# Login email and password for account sending alerts
EMAIL_USERNAME = "dannluciano@ifpi.edu.br"
EMAIL_PASSWORD = os.getenv("SMTP_PASSWORD", "defaultpassworld")

# Mail domain and port for account sending alerts
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587

# Recipients that will get alert
EMAIL_RECEIVERS = ["18hv1a55pr@pomail.net", ]

PUSH_USER_KEY = 'user'
PUSH_USER_TOKEN = 'token'
