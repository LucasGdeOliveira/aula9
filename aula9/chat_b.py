from flask import Flask, request
import threading
import requests
from rsa_custom import generate_keys, encrypt, decrypt
from prompt_toolkit import prompt
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.shortcuts import clear

import time

app = Flask(__name__)

my_public, my_private = generate_keys()
peer_public = None

# Endpoint para receber mensagens criptografadas
@app.route('/receive', methods=['POST'])
def receive():
    global peer_public
    data = request.json
    if data.get("type") == "key_exchange":
        peer_public = tuple(data["key"])
        print(f"\n[Sistema] Chave pública recebida: {peer_public}")
    elif data.get("type") == "message":
        cipher = data["data"]
        message = decrypt(cipher, my_private)
        print(f"\n[Remetente] {message}")
    return 'OK', 200

# Thread para iniciar o servidor Flask
def start_server():
    app.run(port=5001)

# Thread para envio de mensagens com prompt_toolkit
def start_sender():
    global peer_public
    peer_url = input("URL do outro sistema (ex: http://localhost:5001/receive): ")
    
    print("[Sistema] Enviando chave pública...")
    requests.post(peer_url, json={"type": "key_exchange", "key": list(my_public)})

    # Interface de entrada interativa
    with patch_stdout():
        while True:
            try:
                msg = prompt("[Você] ")
                if peer_public:
                    cipher = encrypt(msg, peer_public)
                    requests.post(peer_url, json={"type": "message", "data": cipher})
                else:
                    print("[Erro] Chave pública do destinatário ainda não recebida.")
            except KeyboardInterrupt:
                print("\n[Encerrando]")
                break

# Início
if __name__ == '__main__':
    threading.Thread(target=start_server, daemon=True).start()
    time.sleep(1)  # Pequeno delay para garantir que o servidor suba antes da digitação
    start_sender()
