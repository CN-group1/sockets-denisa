import socket

# Înlocuiește cu IP-ul de Tailscale al Serverului
SERVER_IP = '100.81.207.113' 
SERVER_PORT = 9090         

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(f"Pregătit pentru chat UDP cu {SERVER_IP}:{SERVER_PORT}")
print("Puteți face schimb de mesaje. (Scrie 'exit' sau apasă Ctrl+C pentru a ieși)\n")

try:
    while True:
        # 1. Trimiterea mesajului
        mesaj = input("Tu (Client): ")
        
        # Oprire manuală
        if mesaj.lower() == 'exit':
            print("Se închide clientul UDP...")
            break
            
        mesaj_codificat = mesaj.encode('utf-8')
        
        # Trimitem la adresa specificată (în UDP mereu atașăm destinația)
        client_socket.sendto(mesaj_codificat, (SERVER_IP, SERVER_PORT))
        
        # 2. Așteptarea răspunsului
        # Spre deosebire de TCP, aici programul se va bloca și va aștepta un pachet de oriunde.
        # recvfrom() returnează două lucruri: datele primite ȘI adresa (IP, Port) de unde au venit.
        raspuns_codificat, adresa_expeditor = client_socket.recvfrom(1024)
        
        # 3. Decodificarea și afișarea răspunsului
        raspuns = raspuns_codificat.decode('utf-8')
        
        # Opțional: afișăm și IP-ul de unde a venit mesajul (adresa_expeditor[0] este IP-ul)
        print(f"Studentul A (Server) [{adresa_expeditor[0]}]: {raspuns}")

except KeyboardInterrupt:
    print("\nAi oprit manual scriptul (Ctrl+C).")
except Exception as e:
    print(f"\nA apărut o eroare neașteptată: {e}")
finally:
    client_socket.close()
    print("Socket-ul a fost închis.")