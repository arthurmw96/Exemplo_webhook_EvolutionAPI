**Tutorial de Configuração e Implementação do Evolution API**

Este tutorial guia você na configuração do Evolution API e na criação de um webhook para interagir com mensagens do WhatsApp. Ele também cobre como enviar mensagens usando Python.

---

### **1. Configuração do Ambiente Local**

#### **Passo 1: Instale o Docker e Docker Compose**
Certifique-se de que o Docker e o Docker Compose estejam instalados em sua máquina.

- Instale o Docker seguindo as instruções do site oficial: [Docker Installation](https://docs.docker.com/get-docker/).
- Instale o Docker Compose: [Compose Installation](https://docs.docker.com/compose/install/).

#### **Passo 2: Configuração do Docker Compose**
Crie um arquivo `docker-compose.yml` com o seguinte conteúdo:

```yaml
docker-compose.yml
---
services:
  api:
    container_name: evolution_api
    image: atendai/evolution-api:latest
    restart: always
    depends_on:
      - redis
      - postgres
    ports:
      - 8080:8080
    volumes:
      - evolution_instances:/evolution/instances
    networks:
      - evolution-net
    env_file:
      - .env
    expose:
      - 8080

  redis:
    image: redis:latest
    networks:
      - evolution-net
    container_name: redis
    command: >
      redis-server --port 6379 --appendonly yes
    volumes:
      - evolution_redis:/data
    ports:
      - 6379:6379

  postgres:
    container_name: postgres
    image: postgres:15
    networks:
      - evolution-net
    command: ["postgres", "-c", "max_connections=1000"]
    restart: always
    ports:
      - 5432:5432
    environment:
      - POSTGRES_PASSWORD=<sua-senha>
    volumes:
      - postgres_data:/var/lib/postgresql/data
    expose:
      - 5432

volumes:
  evolution_instances:
  evolution_redis:
  postgres_data:

networks:
  evolution-net:
    name: evolution-net
    driver: bridge
```

#### **Passo 3: Suba os Contêineres**
Execute o comando:
```bash
docker-compose up -d
```
Isso iniciará os serviços do Evolution API, Redis e PostgreSQL.

#### **Passo 4: Configure o Webhook no Evolution Manager**
1. Acesse o painel do Evolution API em `http://localhost:8080`.
2. Configure a URL do Webhook com o seguinte formato:
   ```
   http://<seu-ip>:8000/webhook
   ```
   Certifique-se de que esta URL aponte para o servidor que receberá os eventos do WhatsApp.

---

### **2. Configuração do Webhook com Python**

#### **Passo 1: Crie o Projeto Python**
1. Crie um diretório para o projeto.
2. Crie um ambiente virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   .venv\Scripts\activate   # Windows
   ```
3. Instale as dependências:
   ```bash
   pip install fastapi uvicorn requests
   ```

#### **Passo 2: Crie o Servidor Webhook**
Crie o arquivo `main.py`:

```python
from fastapi import FastAPI, Request
import requests
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)

API_KEY = "<sua-api-key>"
INSTANCE_ID = "<seu-instance-id>"

@app.post("/webhook")
async def webhook(request: Request):
    try:
        data = await request.json()
        logging.info(f"Dados recebidos no webhook: {data}")
        # Responda com status 200 para confirmar recebimento
        return {"status": "ok"}
    except Exception as e:
        logging.error(f"Erro no Webhook: {e}")
        return {"error": str(e)}
```

Inicie o servidor:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

#### **Passo 3: Enviar Mensagens com Python**
Adicione uma função para enviar mensagens:

```python
@app.post("/send-message")
async def send_message(to: str, message: str):
    url = f"http://127.0.0.1:8080/message/sendText/{INSTANCE_ID}"
    headers = {
        "Content-Type": "application/json",
        "apikey": API_KEY
    }
    payload = {
        "number": to,
        "text": message,
        "delay": 0
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao enviar mensagem: {e}")
        return {"error": str(e)}
```

Chame esta rota para enviar mensagens usando cURL ou Postman:

```bash
curl --request POST \
  --url http://127.0.0.1:8000/send-message \
  --header 'Content-Type: application/json' \
  --data '{"to": "5521971185909", "message": "Olá! Isso é um teste."}'
```

---

### **3. Deploy para uma VPS**

Quando mover para uma VPS:
1. **Atualize o Webhook**:
   - Use o IP público ou domínio da VPS no Evolution Manager:
     ```
     http://<ip-publico>:8000/webhook
     ```
2. **Ajuste o Host do FastAPI**:
   No comando de inicialização, mantenha:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```
3. **Certifique-se de que as Portas Estão Abertas**:
   Configure as regras de firewall para permitir acesso às portas `8080` (Evolution API) e `8000` (Webhook).

---

Parabéns! Você configurou o Evolution API e um webhook funcional para interagir com o WhatsApp. Se precisar de ajuda, não hesite em pedir!

