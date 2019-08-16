#!/usr/bin/env python
from __future__ import unicode_literals
from time import sleep, time, strftime
import urllib.request
import io
import smtplib
import sys
from config import DELAY, ALERT_INTERVAL, EMAIL_HOST, EMAIL_PORT, EMAIL_USERNAME, EMAIL_PASSWORD, EMAIL_RECEIVERS, PUSH_USER_KEY, PUSH_USER_TOKEN


last_alert_time = {}  # Monitored sites and timestamp of last alert sent

# Define escape sequences for colored terminal output
COLOR_DICT = {
    "green": "\033[92m",
    "red": "\033[91m",
    "yellow": "\033[93m",
    "bold": "\033[1m",
    "end": "\033[0m",
}

# Message template for alert
MESSAGE = """From: {sender}
To: {receivers}
Subject: Monitor Service Notification

You are being notified that {site} is experiencing a {status} status!
"""


def colorize(text, color):
    """Return input text wrapped in ANSI color codes for input color."""
    return COLOR_DICT[color] + str(text) + COLOR_DICT['end']


def error_log(site, status):
    """Log errors to stdout and log file, and send alert email via SMTP."""
    # print(colored status message to terminal
    print("\n({}) {} STATUS: {}".format(strftime("%a %b %d %Y %H:%M:%S"),
                                        site,
                                        colorize(status, "yellow"),
                                        ))
    # Log status message to log file
    with open('monitor.log', 'a') as log:
        log.write("({}) {} STATUS: {}\n".format(strftime("%a %b %d %Y %H:%M:%S"),
                                                site,
                                                status,
                                                )
                  )


def send_alert(site, status):
    """If more than ALERT_INTERVAL seconds since last alert, resend alert"""
    if (time() - last_alert_time[site]) > ALERT_INTERVAL:
        send_email(site, status)
        # send_push_notification(site, status)
        last_alert_time[site] = time()  # Update time of last email
        print(colorize("Successfully sent alerts", "green"))


def send_email(site, status):
    try:
        # Set up SMTP object
        smtpObj = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        smtpObj.starttls()
        smtpObj.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        smtpObj.sendmail(EMAIL_USERNAME,
                         EMAIL_RECEIVERS,
                         MESSAGE.format(sender=EMAIL_USERNAME,
                                        receivers=", ".join(EMAIL_RECEIVERS),
                                        site=site,
                                        status=status
                                        )
                         )
    except smtplib.SMTPException:
        print(colorize("Error sending email ({}:{})".format(
            EMAIL_HOST, EMAIL_PORT), "red"))


def send_push_notification(site, status):
    import http.client
    import urllib

    try:
        conn = http.client.HTTPSConnection("api.pushover.net:443")
        conn.request("POST", "/1/messages.json",
                     urllib.parse.urlencode({
                         "token": PUSH_USER_TOKEN,
                         "user": PUSH_USER_KEY,
                         "message": "You are being notified that {site} is experiencing a {status} status!",
                     }), {"Content-type": "application/x-www-form-urlencoded"})
        conn.getresponse()
    except http.client.HTTPException as error:
        print(colorize("Error sending push notification ({})".format(
            PUSH_USER_KEY), "red"))


def ping(site):
    """Send GET request to input site and return status code"""
    try:
        resp = urllib.request.urlopen(site, timeout=5)
        return resp.getcode()
    except urllib.error.URLError as error:
        return 500


def get_sites():
    """Return list of unique URLs from input and sites.txt file."""
    sites = sys.argv[1:]  # Accept sites from command line input

    # Read in additional sites to monitor from sites.txt file
    try:
        sites += [site.strip()
                  for site in io.open('sites.txt', mode='r').readlines()]
    except IOError:
        print(colorize("No sites.txt file found", "red"))

    # Add protocol if missing in URL
    for site in range(len(sites)):
        if sites[site][:7] != "http://" and sites[site][:8] != "https://":
            sites[site] = "http://" + sites[site]

    # Eliminate exact duplicates in sites
    sites = list(set(sites))

    return sites


def main():
    sites = get_sites()

    for site in sites:
        print(colorize("Beginning monitoring of {}".format(site), "bold"))
        last_alert_time[site] = 0  # Initialize timestamp as 0

    while sites:
        try:
            for site in sites:
                status = ping(site)
                if status != 200:
                    error_log(site, status)
                    send_alert(site, status)
            sleep(DELAY)
        except KeyboardInterrupt:
            print(colorize("\n-- Monitoring canceled --", "red"))
            break
    else:
        print(colorize("No site(s) input to monitor!", "red"))


if __name__ == '__main__':
    main()
