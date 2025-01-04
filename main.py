import requests
from fastapi import FastAPI, Request
import logging
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Criação do aplicativo FastAPI
app = FastAPI()

# Configuração de logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_message(to, message):
    url = f"{os.getenv('API_BASE_URL')}/message/sendText/{os.getenv('INSTANCE_ID')}"
    headers = {
        "Content-Type": "application/json",
        "apikey": os.getenv('API_KEY')
    }
    payload = {
        "number": to,  # Número no formato internacional, ex: "5521971185909"
        "text": message,
        "delay": 0,  # Define o delay se necessário
        "linkPreview": False,  # Defina True para pré-visualização de links
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao enviar mensagem: {e}")
        return None

@app.post("/webhook")
async def webhook_listener(request: Request):
    try:
        data = await request.json()
        event = data.get("event")

        if event == "messages.upsert":
            # Processa mensagens recebidas
            message_data = data.get("data", {})
            key = message_data.get("key", {})
            message = message_data.get("message", {})
            sender = key.get("remoteJid")
            text = message.get("conversation")

            # Envia uma resposta automática
            response = send_message(
                to=sender,
                message=f"Olá! você disse: {text}"
            )
            logger.info(f"Resposta enviada: {response}")

        return {"status": "success", "message": "Evento processado"}

    except Exception as e:
        logger.error(f"Erro ao processar webhook: {e}")
        return {"status": "error", "message": str(e)}
