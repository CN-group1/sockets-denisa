import socket

# 1. Configurarea detaliilor de conectare
SERVER_IP = '100.81.207.113' 
SERVER_PORT = 9090       

# 2. Crearea socket-ului TCP
# AF_INET specifică utilizarea protocolului IPv4
# SOCK_STREAM specifică utilizarea protocolului TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    print(f"Connecting to {SERVER_IP}:{SERVER_PORT}...")
    client_socket.connect((SERVER_IP, SERVER_PORT))
    print("Connected successfully! The connection will stay open until an error occurs.\n")

    # Infinite loop to keep asking for and sending messages
    while True:
        # 1. Trimiterea mesajului
        mesaj = input("Tu (Client): ")
        client_socket.sendall(mesaj.encode('utf-8'))
        
        # 2. Primirea răspunsului
        # Programul va sta pe pauză aici până când Serverul îți trimite ceva înapoi
        raspuns_codificat = client_socket.recv(1024)
        
        # Dacă funcția recv() primește un pachet gol, înseamnă că Serverul a închis conexiunea
        if not raspuns_codificat:
            print("\nServerul a închis conexiunea în mod normal.")
            break
            
        # 3. Decodificarea și afișarea răspunsului
        # Folosim UTF-8 pentru a decodifica diacriticele și caracterele speciale trimise de Server
        raspuns = raspuns_codificat.decode('utf-8')
        print(f"Studentul A (Server): {raspuns}")
        
except ConnectionRefusedError:
    print("\nError: Connection refused. Is Student A's server running and listening?")
except ConnectionResetError:
    print("\nError: The server (Student A) abruptly closed the connection.")
except BrokenPipeError:
    print("\nError: The network pipe broke. The message could not be sent.")
except TimeoutError:
    print("\nError: Connection timed out. Check your Tailscale connection.")
except KeyboardInterrupt:
    # This catches you pressing Ctrl+C in the terminal to manually kill the script
    print("\nScript manually stopped via Ctrl+C.")
except Exception as e:
    print(f"\nAn unexpected error occurred: {e}")
finally:
    # This block ONLY runs if one of the errors above happens, or if you press Ctrl+C
    client_socket.close()
    print("Socket closed safely.")