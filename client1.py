import cv2
import os
import random
import socket
import base64
from cryptography.fernet import Fernet
from hashlib import sha256

def analyze_coordinates(contours):
    if not contours or len(contours) < 4:
        return None
    selected_contours = random.sample(contours, min(4, len(contours)))
    random_coordinates = []
    for contour in selected_contours:
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            random_coordinates.append((cx, cy))
    multiplication_result = 1
    for coord in random_coordinates:
        multiplication_result *= coord[0] * coord[1]
    return bin(multiplication_result)[2:].zfill(25)

def generate_secret_key(binary_result):
    hash_key = sha256(binary_result.encode()).digest()
    return base64.urlsafe_b64encode(hash_key)

def main():
    cap = cv2.VideoCapture(0)  # Use the default camera (index 0)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.108.106', 5555))

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to read frame from webcam.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        binary_result = analyze_coordinates(contours)
        if binary_result:
            secret_key = generate_secret_key(binary_result)
            user_message = input("enter message (or '0' to exit): ")
            if user_message == "0":
                break

            # Encrypt the message with the derived secret key
            fernet = Fernet(secret_key)
            encrypted_message = fernet.encrypt(user_message.encode())

            # Send binary result and encrypted message to the server
            client_socket.sendall(binary_result.encode() + b',' + encrypted_message)

    client_socket.close()
    cap.release()

if __name__ == "__main__":
    main()