import cv2
import numpy as np
import smtplib
import pygame
import threading

Alarm_Active = False  # Variable to track alarm status
Email_Status = False
Fire_Reported = 0

# Initialize pygame mixer
pygame.mixer.init()

def play_alarm_sound_function():
    global Alarm_Active  # Use the global variable

    while True:
        if Alarm_Active:
            pygame.mixer.music.load('alarm-sound.mp3')
            pygame.mixer.music.play(-1)  # -1 makes it play continuously
            pygame.mixer.music.set_volume(0.5)

            while Alarm_Active:  # Keep playing while the alarm is active
                # Check for any key press to stop the alarm
                key = cv2.waitKey(1)
                if key != -1:
                    Alarm_Active = False
                    pygame.mixer.music.stop()
                pygame.time.delay(1000)

def send_mail_function():
    recipientEmail = "gowtham2mohanasundaram@gmail.com"  # Replace with your email address
    recipientEmail = recipientEmail.lower()

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login("gowtham3032004m@gmail.com", 'gowtham@123')  # Replace with your email and password
        server.sendmail('gowtham3032004m@gmail.com', recipientEmail, "Warning: A Fire Accident has been reported on ABC Company")
        print("Sent to {}".format(recipientEmail))
        server.close()
    except Exception as e:
        print(e)

video = cv2.VideoCapture("nerupu.mp4")  # If you want to use a webcam, use an index like 0 or 1.

while True:
    (grabbed, frame) = video.read()
    if not grabbed:
        break

    frame = cv2.resize(frame, (960, 540))

    blur = cv2.GaussianBlur(frame, (21, 21), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    lower = [18, 50, 50]
    upper = [35, 255, 255]
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")

    mask = cv2.inRange(hsv, lower, upper)

    output = cv2.bitwise_and(frame, hsv, mask=mask)

    no_red = cv2.countNonZero(mask)

    if int(no_red) > 15000:
        Fire_Reported = Fire_Reported + 1
        Alarm_Active = True  # Activate the alarm sound

    cv2.imshow("output", frame)

    if Fire_Reported >= 1:
        if not Email_Status:
            threading.Thread(target=send_mail_function).start()
            Email_Status = True

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
video.release()
