import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_CONFIG = {
    'SMTP_SERVER': 'smtp.gmail.com',
    'SMTP_PORT': 587,
    'SENDER_EMAIL': os.getenv('EMAIL_USERNAME'),
    'SENDER_PASSWORD': os.getenv('EMAIL_APP_PASSWORD'),
    'ADMIN_EMAIL': os.getenv('ADMIN_EMAIL')
}