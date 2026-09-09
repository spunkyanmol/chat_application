import socket
import threading
import time
import sys

def chat_backend(host='localhost', port=5000):
    # create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # bind socket to port
    server_socket.bind((host, port))
    
    # listen for connections
    server_socket.listen(2)
    print(f"Server listening on {host}:{port}")
    
    clients = []
    lock = threading.Lock()
    
    def handle_client(client_socket, address):
        print(f"Client connected: {address}")
        
        with lock:
            clients.append(client_socket)
        
        try:
            while True:
                msg = client_socket.recv(1024).decode('utf-8')
                
                if not msg:
                    break
                
                print(f"Message from {address}: {msg}")
                
                # broadcast to all clients
                with lock:
                    for client in clients:
                        if client != client_socket:
                            try:
                                client.send(f"{address}: {msg}".encode('utf-8'))
                            except:
                                pass
        
        except:
            pass
        
        finally:
            with lock:
                clients.remove(client_socket)
            client_socket.close()
            print(f"Client disconnected: {address}")
    
    try:
        while True:
            client_socket, address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
            client_thread.daemon = True
            client_thread.start()
    
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server_socket.close()

if __name__ == "__main__":
    chat_backend()
