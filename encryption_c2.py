import socket
from cryptography.fernet import Fernet
import base64
from hashlib import sha256

def derive_key(binary_result):
    hash_key = sha256(binary_result.encode()).digest()
    base64_key = base64.urlsafe_b64encode(hash_key)
    return base64_key

def decrypt_message(encrypted_message, key):
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_message)

def client_main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.108.106', 5555))

    while True:
        data = client_socket.recv(4096)
        if not data:
            break  # Break the loop if no data is received

        binary_result, encrypted_message = data.split(b',', 1)

        # Derive key from binary result and decrypt the message
        key = derive_key(binary_result.decode())
        decrypted_message = decrypt_message(encrypted_message, key)

        # Print the decrypted message
        print(f" Message: {decrypted_message.decode()}")

    client_socket.close()

if __name__ == "__main__":
    client_main()
