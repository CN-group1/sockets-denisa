# frozen_string_literal: true
require 'socket'

# --- CONFIGURARE ---
# Ascultă pe toate interfețele (echivalent cu 0.0.0.0)
HOST = '100.81.207.113'
PORT = 9090

def start_tcp_chat_server
  puts "--- Server TCP Bidirecțional (Chat) ---"
  
  # Creăm un server TCP care ascultă pe portul specificat
  server = TCPServer.new(HOST, PORT)
  puts "[*] Aștept conexiuni pe portul #{PORT}..."

  # Acceptăm conexiunea (blocant până se conectează cineva)
  client = server.accept
  peer_ip = client.peeraddr[3]
  puts "[+] Conectat cu succes la clientul: #{peer_ip}"
  puts "Așteaptă ca Studentul B să trimită primul mesaj...\n\n"

  loop do
    # 1. Serverul AȘTEAPTĂ mesajul de la client
    mesaj_primit = client.recv(1024).force_encoding('UTF-8').strip
    
    if mesaj_primit.empty?
      puts "\n[-] Clientul a închis conexiunea."
      break
    end

    puts "[Studentul B]: #{mesaj_primit}"
    
    if mesaj_primit.downcase == 'exit'
      puts "Conexiunea a fost închisă de client."
      break
    end

    # 2. Serverul TRIMITE răspunsul
    print "[Tu - Server TCP]: "
    raspuns = gets.chomp # Citește de la tastatură și elimină enter-ul de la final

    client.send(raspuns, 0)
    
    break if raspuns.downcase == 'exit'
  end

  # Curățenie: închidem socket-urile
  client.close
  server.close
end

def start_udp_chat_server
  puts "--- Server UDP Bidirecțional (Chat Ping-Pong) ---"
  
  # Creăm un socket UDP
  server = UDPSocket.new
  server.bind(HOST, PORT)
  
  puts "[*] Serverul UDP ascultă pe portul #{PORT}..."
  puts "Așteaptă primul pachet UDP...\n\n"

  loop do
    # 1. Serverul AȘTEAPTĂ mesajul. recvfrom returnează datele și informații despre expeditor
    mesaj_primit, sender = server.recvfrom(1024)
    mesaj_primit = mesaj_primit.force_encoding('UTF-8').strip
    
    sender_ip = sender[3]
    sender_port = sender[1]

    puts "[Studentul B (#{sender_ip})]: #{mesaj_primit}"
    
    break if mesaj_primit.downcase == 'exit'

    # 2. Serverul TRIMITE răspunsul direct la IP-ul și portul expeditorului
    print "[Tu - Server UDP]: "
    raspuns = gets.chomp

    server.send(raspuns, 0, sender_ip, sender_port)
    
    break if raspuns.downcase == 'exit'
  end

  server.close
end

# --- SELECTOR DE PROTOCOL ---
# Decomentează metoda pe care vrei să o rulezi:

#start_tcp_chat_server
start_udp_chat_server