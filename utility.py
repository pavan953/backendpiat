import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from config.email_config import EMAIL_CONFIG

def send_tracking_alert(person_name, location, image_data):
    msg = MIMEMultipart()
    msg['Subject'] = f'Person Tracked: {person_name}'
    msg['From'] = EMAIL_CONFIG['SENDER_EMAIL']
    msg['To'] = EMAIL_CONFIG['ADMIN_EMAIL']
    
    text_content = f"""
    Person Detected:
    Name: {person_name}
    Location: {location}
    Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """
    
    msg.attach(MIMEText(text_content))
    
    # Attach image
    image = MIMEImage(image_data)
    image.add_header('Content-Disposition', 'attachment', filename=f'{person_name}_detection.jpg')
    msg.attach(image)
    
    try:
        with smtplib.SMTP(EMAIL_CONFIG['SMTP_SERVER'], EMAIL_CONFIG['SMTP_PORT']) as server:
            server.starttls()
            server.login(EMAIL_CONFIG['SENDER_EMAIL'], EMAIL_CONFIG['SENDER_PASSWORD'])
            server.send_message(msg)
            return True
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False