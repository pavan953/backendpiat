import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

def send_email_to_admin(usn, name, location, image_path):
    sender_email = "bushingaripavankumar@gmail.com"
    sender_password = "ejeqnnzalayubanu"
    admin_email = "pk5684865@gmail.com"

    subject = f"Person Tracked: {name} ({usn})"
    body = f"""
    <h3>Person Tracked</h3>
    <p>The person <b>{name}</b> with USN <b>{usn}</b> has been tracked.</p>
    <p><b>Location:</b> {location}</p>
    <p>Please find the attached image of the tracked person.</p>
    """

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = admin_email
    msg['Subject'] = subject

    # Attach the email body
    msg.attach(MIMEText(body, 'html'))

    # Attach the image
    if os.path.exists(image_path):
        with open(image_path, 'rb') as img_file:
            mime_base = MIMEBase('application', 'octet-stream')
            mime_base.set_payload(img_file.read())
            encoders.encode_base64(mime_base)
            mime_base.add_header(
                'Content-Disposition',
                f'attachment; filename={os.path.basename(image_path)}'
            )
            msg.attach(mime_base)

    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print(f"Email sent successfully to {admin_email}")
    except Exception as e:
        print(f"Error sending email: {str(e)}")
