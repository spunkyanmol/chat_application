import socket
import threading
import time
import sys
import customtkinter as ctk

def chat_gui(host='localhost', port=5000):
    # create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to the server
    client_socket.connect((host, port))
    print(f"Connected to {host}:{port}")

    # Create GUI window
    app = ctk.CTk()
    app.title("Chat Application")
    app.geometry("500x600")

    # Message display area
    message_frame = ctk.CTkFrame(app)
    message_frame.pack(padx=10, pady=10, fill="both", expand=True)

    text_display = ctk.CTkTextbox(message_frame, state="disabled", text_color="white")
    text_display.pack(fill="both", expand=True)

    # Input area
    input_frame = ctk.CTkFrame(app)
    input_frame.pack(padx=10, pady=10, fill="x")

    message_input = ctk.CTkEntry(input_frame, placeholder_text="Enter your message...")
    message_input.pack(side="left", fill="x", expand=True, padx=(0, 10))

    def send_msg():
        msg = message_input.get()

        if msg == "/quit":
            # closing socket connection
            print("Closing chat interface safely...")
            time.sleep(1)
            client_socket.close()
            app.quit()
            return

        if msg:
            client_socket.send(msg.encode('utf-8'))
            message_input.delete(0, "end")

    def recv_msg():
        while True:
            try:
                response = client_socket.recv(1024).decode('utf-8')

                if not response:
                    print("Host maybe got disconnected. Breaking socket.")
                    sys.exit()

                text_display.configure(state="normal")
                text_display.insert("end", f"\nReceived: {response}")
                text_display.configure(state="disabled")
                text_display.see("end")

            except:
                break

    send_button = ctk.CTkButton(input_frame, text="Send", command=send_msg)
    send_button.pack(side="right")

    receiver = threading.Thread(target=recv_msg)
    receiver.daemon = True
    receiver.start()

    message_input.bind("<Return>", lambda e: send_msg())

    app.mainloop()

if __name__ == "__main__":
    chat_gui()
