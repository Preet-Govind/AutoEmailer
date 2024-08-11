import time
import logging
import os
from configparser import ConfigParser
import importlib
import subprocess
import sys

# Required libraries and their respective pip package names
REQUIRED_LIBRARIES = {
    'smtplib': None,
    'email': None,
    'schedule': 'schedule',
    'importlib': None,
    'configparser': None
}

# Configure logging
logging.basicConfig(filename='email_sender.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def install_package(package_name):
    """Install the package using pip."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        logging.info(f"{package_name} installed successfully.")
        print(f"{package_name} installed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to install {package_name}: {e}")
        print(f"Failed to install {package_name}. Please install it manually.")

def check_libraries():
    """Check if required libraries are installed, and install them if they are missing."""
    for package, module_name in REQUIRED_LIBRARIES.items():
        try:
            if module_name:
                importlib.import_module(module_name)
            logging.info(f"{package} is installed.")
        except ImportError:
            logging.error(f"{package} is not installed. Attempting to install...")
            print(f"{package} is not installed. Attempting to install...")
            if module_name:
                install_package(module_name)
            else:
                print(f"{package} is a standard library and should be available in your Python installation.")

# Check and install required libraries
check_libraries()

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import schedule

# Load configuration from the config file
config = ConfigParser()
config.read('config.ini')

SMTP_SERVER = config.get('email', 'SMTP_SERVER')
SMTP_PORT = config.getint('email', 'SMTP_PORT')
SMTP_USERNAME = config.get('email', 'SMTP_USERNAME')
SMTP_PASSWORD = config.get('email', 'SMTP_PASSWORD')
FROM_EMAIL = config.get('email', 'FROM_EMAIL')
TO_EMAIL = config.get('email', 'TO_EMAIL')
SUBJECT = 'Daily Report'


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import schedule



config = ConfigParser()
config.read('config.ini')

SMTP_SERVER = config.get('email', 'SMTP_SERVER')
SMTP_PORT = config.getint('email', 'SMTP_PORT')
SMTP_USERNAME = config.get('email', 'SMTP_USERNAME')
SMTP_PASSWORD = config.get('email', 'SMTP_PASSWORD')
FROM_EMAIL = config.get('email', 'FROM_EMAIL')
TO_EMAIL = config.get('email', 'TO_EMAIL')
SUBJECT = 'Daily Report'

def send_email():
    try:
        # email heads 
        msg = MIMEMultipart()
        msg['From'] = FROM_EMAIL
        msg['To'] = TO_EMAIL
        msg['Subject'] = SUBJECT

        # email body
        body = 'This is to notify you , email body here.'
        msg.attach(MIMEText(body, 'plain'))

        # attach file when needed
        filename = 'report.pdf'
        if os.path.isfile(filename):
            with open(filename, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {filename}',
                )
                msg.attach(part)
        else:
            logging.warning(f"{filename} not found. No attachment will be sent.")

        # Connect to the SMTP server and send the email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())
            logging.info("Email sent successfully")

    except Exception as e:
        logging.error(f"Failed to send email: {e}")


schedule.every().day.at("09:00").do(send_email)

while True:
    schedule.run_pending()
    time.sleep(60)  # one min sleep
