"""
Módulo de Configurações do Sistema
"""

"""
Módulo de Configurações do Sistema
"""
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# ============================================
# CONFIGURAÇÃO DE USUÁRIOS E ACESSOS
# ============================================

# ATENÇÃO: As senhas agora são armazenadas como hashes bcrypt
# Use o script generate_password_hash.py para gerar novos hashes
# As senhas devem ser configuradas no arquivo .env

USUARIOS_HASHES = {
    "admin": os.getenv('USER_ADMIN_HASH'),
    "diacono01": os.getenv('USER_DIACONO01_HASH'),
    "diacono02": os.getenv('USER_DIACONO02_HASH')
}

NIVEIS_ACESSO = {
    "admin": "admin",
    "diacono01": "admin",
    "diacono02": "admin"
}

NOMES_USUARIOS = {
    "admin": "Administrador",
    "diacono01": "Diácono01",
    "diacono02": "Diácono02"
}

# ============================================
# CONFIGURAÇÕES DO BANCO DE DADOS
# ============================================

DATABASE_NAME = "dizimos_ofertas.db"

# ============================================
# CONFIGURAÇÕES DA APLICAÇÃO
# ============================================

PAGE_TITLE = "Dízimos e Ofertas"
PAGE_ICON = "💰"
LAYOUT = "wide"
LOGO_PATH = "./imagem/igrejadechomai.jpg"

# ============================================
# CATEGORIAS E TIPOS
# ============================================

TIPOS_PAGAMENTO = ["Dinheiro", "Cartão", "Transferência", "Cheque", "Pix"]
CATEGORIAS = ["Dízimo", "Oferta", "Visitante"]

# ============================================
# CONFIGURAÇÕES DO WHATSAPP (TWILIO)
# ============================================

# Para habilitar o WhatsApp, configure as variáveis abaixo:
# 1. Crie uma conta em https://www.twilio.com
# 2. Ative o WhatsApp Sandbox ou configure WhatsApp Business API
# 3. Obtenha as credenciais no console Twilio
# 4. Substitua os valores abaixo ou use variáveis de ambiente

import os

# Habilitar/Desabilitar funcionalidade WhatsApp
WHATSAPP_ENABLED = os.getenv('WHATSAPP_ENABLED', 'False').lower() == 'true'

# Credenciais Twilio (obtenha em https://console.twilio.com)
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', 'seu_account_sid_aqui')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', 'seu_auth_token_aqui')

# Número WhatsApp Twilio (formato: whatsapp:+14155238886)
TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER', 'whatsapp:+14155238886')

# Mensagem padrão pode ser personalizada
WHATSAPP_MENSAGEM_PADRAO = """
🙏 *Ministério Dechonai*

Sua contribuição foi registrada com sucesso!

Que Deus abençoe sua vida!
"""

# ============================================
# OPERADORAS DE CELULAR
# ============================================

OPERADORAS = [
    "Vivo",
    "Claro",
    "TIM",
    "Oi",
    "Algar",
    "Nextel",
    "Sercomtel",
    "Outra"
]

# ============================================
# CONFIGURAÇÕES DE NOTIFICAÇÕES
# ============================================

# Configurações de Email (SMTP)
SMTP_SERVER = "smtp.gmail.com"  # Servidor SMTP do Gmail
SMTP_PORT = 587  # Porta para TLS
EMAIL_REMETENTE = "seu-email@gmail.com"  # Email remetente
EMAIL_SENHA = "sua-senha-app"  # Senha de aplicativo do Gmail

# Configurações de SMS (Twilio - exemplo)
TWILIO_ACCOUNT_SID = "seu_account_sid"  # Account SID do Twilio
TWILIO_AUTH_TOKEN = "seu_auth_token"  # Auth Token do Twilio
TWILIO_PHONE_NUMBER = "+5511999999999"  # Número do Twilio

# Habilitar/Desabilitar Notificações
NOTIFICACOES_HABILITADAS = True  # True para habilitar, False para desabilitar
ENVIAR_EMAIL_AUTO = True  # Enviar e-mail automaticamente após cadastro
ENVIAR_SMS_AUTO = True  # Enviar SMS automaticamente após cadastro
