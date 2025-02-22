import socket
import ssl
import threading

def handle_client(client_sock):
    try:
        # Read the first line of the request to determine the protocol
        request_line = client_sock.recv(4096)
        if not request_line:
            return  # No request received

        # Attempt to decode the request line
        try:
            request_line_decoded = request_line.decode('utf-8').splitlines()
        except UnicodeDecodeError:
            print("Received non-UTF-8 data, handling as raw bytes.")
            request_line_decoded = request_line.splitlines()  # Keep as bytes

        # Check if we have valid request lines
        if isinstance(request_line_decoded, bytes):
            request_line_decoded = [line.decode('latin-1') for line in request_line_decoded]  # Fallback to latin-1

        method, path, _ = request_line_decoded[0].split()

        # Determine the target host and port based on the request
        if method == "CONNECT":
            target_host, target_port = path.split(":") if ":" in path else (path, 443)
            target_port = int(target_port)
            # Send a 200 response for CONNECT requests
            client_sock.sendall(b"HTTP/1.1 200 Connection Established\r\n\r\n")

            # Connect to the target server directly.
            remote_sock = ssl.wrap_socket(socket.create_connection((target_host, target_port)))

            # Start bidirectional data forwarding for HTTPS
            t1 = threading.Thread(target=forward, args=(client_sock, remote_sock))
            t2 = threading.Thread(target=forward, args=(remote_sock, client_sock))
            t1.start()
            t2.start()

        elif method in ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"]:
            # For HTTP requests, parse the target host from the path
            target_host = "ardupilot.org"  # Default target for HTTP requests
            target_port = 80  # Use 80 for HTTP

            # Connect to the target server directly.
            remote_sock = socket.create_connection((target_host, target_port))

            # Forward the entire request to the remote server
            remote_sock.sendall(request_line)

            # Function to forward data between two sockets.
            def forward(source, destination):
                try:
                    while True:
                        data = source.recv(4096)
                        if not data:
                            break
                        
                        print(data)
                        destination.sendall(data)
                except ConnectionAbortedError as e:
                    print("Connection aborted:", e)  # Log the error
                except Exception as e:
                    print("Error during forwarding:", e)  # Log any other errors
                finally:
                    source.close()
                    destination.close()

            # Start bidirectional data forwarding for HTTP
            t1 = threading.Thread(target=forward, args=(remote_sock, client_sock))
            t2 = threading.Thread(target=forward, args=(client_sock, remote_sock))
            t1.start()
            t2.start()

        else:
            print(f"Unsupported method. Only CONNECT, GET, POST, PUT, DELETE, HEAD, OPTIONS are supported. Not {method}")
            client_sock.close()

    except Exception as e:
        print("Error during setup:", e)
        client_sock.close()

def start_secure_proxy(listen_addr='', listen_port=8888, certfile='cert.pem', keyfile='key.pem'):
    """
    Start a secure forward proxy that listens for HTTPS connections.
    The proxy accepts client TLS connections, reads the CONNECT request,
    and tunnels the connection to the target host.
    """
    # Create a TCP server socket.
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((listen_addr, listen_port))
    server_socket.listen(5)
    print(f"Secure proxy listening on {listen_addr or '0.0.0.0'}:{listen_port}")

    # Create an SSL context for the server side.
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=certfile, keyfile=keyfile)

    while True:
        try:
            # Accept a new client connection.
            client_socket, addr = server_socket.accept()
            print(f"Accepted connection from {addr}")
            try:
                # Wrap the connection in TLS.
                secure_client_socket = context.wrap_socket(client_socket, server_side=True)
            except ssl.SSLError as ssl_err:
                print("SSL handshake failed:", ssl_err)
                client_socket.close()
                continue

            # Handle the client connection in a new thread.
            threading.Thread(target=handle_client, args=(secure_client_socket,), daemon=True).start()

        except Exception as e:
            print("Error accepting connections:", e)
            break

    server_socket.close()

if __name__ == '__main__':
    # Replace 'cert.pem' and 'key.pem' with your certificate file paths.
    start_secure_proxy(listen_port=8888, certfile='public_key.crt', keyfile='private_key.pem')
