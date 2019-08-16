#!/usr/bin/env python
import os

DELAY = 60  # Delay between site queries
EMAIL_INTERVAL = 1800  # Delay between alert emails

# Login email and password for account sending alerts
EMAIL_USERNAME = "dannluciano@ifpi.edu.br"
EMAIL_PASSWORD = os.environ.get("SMTP_PASSWORD")

# Mail domain and port for account sending alerts
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587

# Recipients that will get alert
EMAIL_RECEIVERS = ["dannluciano@ifpi.edu.br"]
