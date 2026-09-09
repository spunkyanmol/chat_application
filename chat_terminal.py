import socket
import threading
import time
import sys

def chat_terminal(host='localhost', port=5000):
    # create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to the server
    client_socket.connect((host, port))
    print(f"Connected to {host}:{port}")

    def send_msg():
        while True:
            # send message to the server
            msg = input("\nEnter your message: ")

            if msg == "/quit":
                # closing socket connection and breaking code
                print("Closing chat interface safely...")
                time.sleep(2)
                client_socket.close()
                break

            client_socket.send(msg.encode('utf-8'))

    def recv_msg():
        while True:
            # receive response from the server
            response = client_socket.recv(1024).decode('utf-8')

            if not response:
                print("Host maybe got disconnected. Breaking socket.")
                sys.exit()

            print(f"\nReceived: {response}\n\nEnter your message: ")

    sender = threading.Thread(target=send_msg)
    receiver = threading.Thread(target=recv_msg)
    receiver.start()
    sender.start()
    receiver.join()
    sender.join()

if __name__ == "__main__":
    chat_terminal()
