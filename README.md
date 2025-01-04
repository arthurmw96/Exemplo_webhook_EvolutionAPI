# Webhook Listener para Evolution API

Este projeto é um exemplo de implementação de um webhook listener para a [Evolution API](https://github.com/evolution-api/evolution-api), uma API para automação do WhatsApp. O projeto demonstra como receber e responder automaticamente a mensagens do WhatsApp usando FastAPI.

## Características

- Webhook listener usando FastAPI
- Resposta automática para mensagens recebidas
- Configuração via variáveis de ambiente
- Compatível com Docker

## Pré-requisitos

- Python 3.12 ou superior
- Evolution API rodando (preferencialmente via Docker)
- UV (gerenciador de pacotes Python)

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/arthurmw96/Exemplo_webhook_EvolutionAPI.git
cd Exemplo_webhook_EvolutionAPI
```

2. Instale as dependências usando UV:
```bash
uv pip install -r requirements.txt
```

## Configuração

1. Copie o arquivo de exemplo de ambiente:
```bash
cp .env.example .env
```

2. Configure as variáveis no arquivo `.env`:

- `API_KEY`: Sua chave de API do Evolution API (gerada no painel administrativo)
- `INSTANCE_ID`: Nome da sua instância do WhatsApp no Evolution API
- `API_BASE_URL`: URL base do Evolution API
  - Se usando Docker compose: `http://evolution-api:8080`
  - Se usando Docker run: `http://[IP_DO_CONTAINER]:8080`

## Uso

1. Inicie o servidor:
```bash
uvicorn main:app --reload
```

2. Configure o webhook no Evolution API para apontar para:
```
http://seu-servidor:8000/webhook
```

3. O servidor irá automaticamente:
   - Receber mensagens via webhook
   - Responder com uma confirmação da mensagem recebida

## Estrutura do Projeto

- `main.py`: Implementação principal do webhook listener
- `.env`: Configurações sensíveis (não versionado)
- `.env.example`: Exemplo de configurações
- `pyproject.toml`: Configurações do projeto e dependências

## Contribuição

Sinta-se à vontade para contribuir com o projeto. Abra uma issue ou envie um pull request.

## Licença

Este projeto está sob a licença MIT.
