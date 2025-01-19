# import cv2
# import numpy as np
# import face_recognition
# from database import get_all_persons
# from datetime import datetime
# import sys
# import threading
# import requests
# from database import add_tracking_event
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from email.mime.image import MIMEImage
# from datetime import datetime
# import os

# # List of camera IP addresses
# camera_ips = [
#     "http://192.0.0.4:8080/video",
# ]
# known_face_encodings = []
# known_face_usns = []
# known_face_names = []

# def load_known_faces():
#     """
#     Load face encodings, USNs, and names from the database.
#     """
#     global known_face_encodings, known_face_usns, known_face_names
#     persons = get_all_persons()
#     known_face_encodings = [np.frombuffer(person[2], dtype=np.float64) for person in persons]
#     known_face_usns = [person[0] for person in persons]
#     known_face_names = [person[1] for person in persons]

# load_known_faces()
# usn_to_track = sys.argv[1] if len(sys.argv) > 1 else None
# if usn_to_track and usn_to_track not in known_face_usns:
#     requests.post('http://localhost:8000/api/person_not_found', 
#                  json={'message': f'USN {usn_to_track} not found in database'})
#     print(f"Error: USN {usn_to_track} not found in database")
#     sys.exit(1)
# caps = [cv2.VideoCapture(ip) for ip in camera_ips]
# frames = [None] * len(caps)
# lock = threading.Lock()

# def capture_frames(index, cap):
#     global frames
#     while True:
#         success, frame = cap.read()
#         if success:
#             with lock:
#                 frames[index] = frame
# threads = []
# for i, cap in enumerate(caps):
#     thread = threading.Thread(target=capture_frames, args=(i, cap))
#     thread.daemon = True
#     thread.start()
#     threads.append(thread)

# def send_email_to_admin(usn, name, location, face_image_path):
#     """
#     Send an email notification to admin when a tracked person is found.
#     Args:
#         usn (str): USN of the tracked person
#         name (str): Name of the tracked person
#         location (str): Location where the person was detected
#         face_image_path (str): Path to the saved face image
#     """
#     SMTP_SERVER = "smtp.gmail.com"
#     SMTP_PORT = 587
#     SENDER_EMAIL = "bushingaripavankumar@gmail.com"
#     SENDER_PASSWORD = "ejeqnnzalayubanu"
#     # ADMIN_EMAIL = "kiranbusari2208@gmail.com"
#     ADMIN_EMAIL = "pk5684865@gmail.com"
    
#     if not all([SENDER_EMAIL, SENDER_PASSWORD, ADMIN_EMAIL]):
#         print("Email configuration not complete. Please set SENDER_EMAIL, SENDER_PASSWORD, and ADMIN_EMAIL environment variables.")
#         return
    
#     # Create the email message
#     msg = MIMEMultipart()
#     msg['Subject'] = f'Person Detected: {name} ({usn})'
#     msg['From'] = SENDER_EMAIL
#     msg['To'] = ADMIN_EMAIL
    
#     # Email body
#     body = f"""
#     Person Detection Alert
    
#     A tracked person has been detected:
#     Name: {name}
#     USN: {usn}
#     Location: {location}
#     Coordinates: {coordinates}
#     Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    
#     Tracked Person Image.
#     """
#     msg.attach(MIMEText(body, 'plain'))
    
#     # Attach the face image
#     try:
#         with open(face_image_path, 'rb') as f:
#             img = MIMEImage(f.read())
#             img.add_header('Content-Disposition', 'attachment', filename=os.path.basename(face_image_path))
#             msg.attach(img)
#     except Exception as e:
#         print(f"Error attaching image: {e}")
    
#     # Send the email
#     try:
#         with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
#             server.starttls()
#             server.login(SENDER_EMAIL, SENDER_PASSWORD)
#             server.send_message(msg)
#         print(f"Email notification sent to admin for {name} ({usn})")
#     except Exception as e:
#         print(f"Error sending email: {e}")

# person_found = False

# while True:
#     for i, frame in enumerate(frames):
#         if frame is None:
#             continue

#         # Detect faces and compute encodings
#         face_locations = face_recognition.face_locations(frame)
#         face_encodings = face_recognition.face_encodings(frame, face_locations)

#         for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
#             matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
#             face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
#             usn = "Unknown"
#             name = "Unknown"

#             # Check if the face matches any known encoding
#             if face_distances.size > 0:
#                 best_match_index = np.argmin(face_distances)
#                 if matches[best_match_index] and face_distances[best_match_index] < 0.6:  # Threshold for face distance
#                     usn = known_face_usns[best_match_index]
#                     name = known_face_names[best_match_index]

#             # Highlight the detected face
#             # if usn == usn_to_track:
#             #     color = (0, 255, 0)  # Green for the tracked person
#             #     label = f"{name} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
#             #     if not person_found:
#             #         person_found = True
#             #         # Add tracking event to database
#             #         add_tracking_event(usn, f'Camera {i}')
#             #         # Send notification
#             #         requests.post('http://localhost:5000/api/person_found', 
#             #                      json={'camera': f'Camera {i}', 'name': name})
#             if usn == usn_to_track:
#                 color = (0, 255, 0)  # Green for the tracked person
#                 label = f"{name} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
#                 if not person_found:
#                     person_found = True
#                     # Add tracking event to database
#                     add_tracking_event(usn, f'Camera {i}')
        
#                     # Save the face image
#                     face_image_path = f"tracked_person_{usn}.jpg"
#                     tracked_face_image = frame[top:bottom, left:right]
#                     cv2.imwrite(face_image_path, tracked_face_image)

#         # Send email to admin
#                     location = f"Camera {i}"
#                     send_email_to_admin(usn, name, location, face_image_path)

#         # Send notification
#                     requests.post('http://localhost:5000/api/person_found', 
#                                 json={'camera': f'Camera {i}', 'name': name})

#             else:
#                 color = (0, 0, 255)  # Red for others
#                 label = f"{name} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}" if usn != "Unknown" else "Unknown"
            
#             cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
#             cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
#             font = cv2.FONT_HERSHEY_DUPLEX
#             cv2.putText(frame, label, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

#         # Display the video feed
#         cv2.imshow(f"Camera {i}", frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release all video captures and close windows
# for cap in caps:
#     cap.release()
# cv2.destroyAllWindows()
import cv2
import face_recognition
import numpy as np
import threading
import requests
import sys
from datetime import datetime
from database import get_all_persons, add_tracking_event
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from datetime import datetime
import os
camera_info = [
    {"ip": "http://192.0.0.4:8080/video", "coordinates": "37.7749° N, 122.4194° W"},
]
known_face_encodings = []
known_face_usns = []
known_face_names = []

def load_known_faces():
    """
    Load face encodings, USNs, and names from the database.
    """
    global known_face_encodings, known_face_usns, known_face_names
    persons = get_all_persons()
    known_face_encodings = [np.frombuffer(person[2], dtype=np.float64) for person in persons]
    known_face_usns = [person[0] for person in persons]
    known_face_names = [person[1] for person in persons]
load_known_faces()
usn_to_track = sys.argv[1] if len(sys.argv) > 1 else None
if usn_to_track and usn_to_track not in known_face_usns:
    requests.post('http://localhost:8000/api/person_not_found', 
                 json={'message': f'USN {usn_to_track} not found in database'})
    print(f"Error: USN {usn_to_track} not found in database")
    sys.exit(1)
caps = [cv2.VideoCapture(info["ip"]) for info in camera_info]
frames = [None] * len(caps)
lock = threading.Lock()

def capture_frames(index, cap):
    global frames
    while True:
        success, frame = cap.read()
        if success:
            with lock:
                frames[index] = frame
threads = []
for i, cap in enumerate(caps):
    thread = threading.Thread(target=capture_frames, args=(i, cap))
    thread.daemon = True
    thread.start()
    threads.append(thread)

def send_email_to_admin(usn, name, coordinates, face_image_path):
    """
    Send an email notification to admin when a tracked person is found.
    Args:
        usn (str): USN of the tracked person
        name (str): Name of the tracked person
        coordinates (str): Coordinates where the person was detected
        face_image_path (str): Path to the saved face image
    """
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    SENDER_EMAIL = "bushingaripavankumar@gmail.com"
    SENDER_PASSWORD = "ejeqnnzalayubanu"
    ADMIN_EMAIL = "kiranbusari2208@gmail.com"
    
    if not all([SENDER_EMAIL, SENDER_PASSWORD, ADMIN_EMAIL]):
        print("Email configuration not complete. Please set SENDER_EMAIL, SENDER_PASSWORD, and ADMIN_EMAIL environment variables.")
        return
    
    # Create the email message
    msg = MIMEMultipart()
    msg['Subject'] = f'Person Detected: {name} ({usn})'
    msg['From'] = SENDER_EMAIL
    msg['To'] = ADMIN_EMAIL
    
    body = f"""
    Person Detection Alert
    
    A tracked person has been detected:
    Name: {name}
    USN: {usn}
    Coordinates: {coordinates}
    Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    
    Please find the detected face image attached.
    """
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        with open(face_image_path, 'rb') as f:
            img = MIMEImage(f.read())
            img.add_header('Content-Disposition', 'attachment', filename=os.path.basename(face_image_path))
            msg.attach(img)
    except Exception as e:
        print(f"Error attaching image: {e}")
    
    # Send the email
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        print(f"Email notification sent to admin for {name} ({usn})")
    except Exception as e:
        print(f"Error sending email: {e}")

person_found = False

while True:
    for i, frame in enumerate(frames):
        if frame is None:
            continue

        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            usn = "Unknown"
            name = "Unknown"

            if face_distances.size > 0:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    usn = known_face_usns[best_match_index]
                    name = known_face_names[best_match_index]

            if usn == usn_to_track:
                color = (0, 255, 0)  # Green for the tracked person
                label = f"{name} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                if not person_found:
                    person_found = True
                    # Save the face image
                    face_image_path = f"tracked_person_{usn}.jpg"
                    tracked_face_image = frame[top:bottom, left:right]
                    cv2.imwrite(face_image_path, tracked_face_image)
                    coordinates = camera_info[i]["coordinates"]
                    add_tracking_event(usn, f'Camera {i}', tracked_face_image.tobytes())
                    send_email_to_admin(usn, name, coordinates, face_image_path)
                    requests.post('http://localhost:5000/api/person_found', 
                                  json={'camera': f'Camera {i}', 'name': name})

            else:
                color = (0, 0, 255)  # Red for others
                label = f"{name} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}" if usn != "Unknown" else "Unknown"
            
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, label, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        cv2.imshow(f"Camera {i}", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
for cap in caps:
    cap.release()
cv2.destroyAllWindows()