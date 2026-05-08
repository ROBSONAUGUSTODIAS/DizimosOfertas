"""
Módulo de Configurações do Sistema
"""
import os

# Tenta importar streamlit para uso de secrets (Streamlit Cloud)
try:
    import streamlit as st
    # Verifica se secrets foi realmente configurado com a seção [passwords]
    USE_STREAMLIT_SECRETS = (
        hasattr(st, 'secrets') and 
        'passwords' in st.secrets and 
        len(st.secrets.get('passwords', {})) > 0
    )
except (ImportError, FileNotFoundError, Exception):
    USE_STREAMLIT_SECRETS = False

# Carrega variáveis de ambiente do arquivo .env (desenvolvimento local)
# Mesmo com Streamlit secrets habilitado, manter o .env como fallback.
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

def get_secret(key, section=None):
    """
    Obtém valores secretos de forma flexível:
    - Streamlit Cloud: usa st.secrets
    - Desenvolvimento local: usa .env
    """
    if USE_STREAMLIT_SECRETS:
        try:
            if section:
                # Tenta acessar com seção
                if section in st.secrets and key in st.secrets[section]:
                    value = st.secrets[section][key]
                    if value:  # Garante que não é None ou string vazia
                        return value
            # Tenta acessar diretamente
            if key in st.secrets:
                value = st.secrets[key]
                if value:  # Garante que não é None ou string vazia
                    return value
        except Exception as e:
            print(f"Erro ao acessar secret {key}: {e}")

    # Fallback para variáveis de ambiente (.env)
    value = os.getenv(key)
    if value:
        return value
    return None

# ============================================
# CONFIGURAÇÃO DE USUÁRIOS E ACESSOS
# ============================================

# ATENÇÃO: As senhas agora são armazenadas como hashes bcrypt
# Use o script generate_password_hash.py para gerar novos hashes
# 
# Desenvolvimento local: configure no arquivo .env
# Streamlit Cloud: configure em Settings → Secrets

USUARIOS_HASHES = {
    "admin": get_secret('USER_ADMIN_HASH', 'passwords') or get_secret('USER_ADMIN_HASH'),
    "diacono01": get_secret('USER_DIACONO01_HASH', 'passwords') or get_secret('USER_DIACONO01_HASH'),
    "diacono02": get_secret('USER_DIACONO02_HASH', 'passwords') or get_secret('USER_DIACONO02_HASH'),
    "diacono03": get_secret('USER_DIACONO03_HASH', 'passwords') or get_secret('USER_DIACONO03_HASH')
}

NIVEIS_ACESSO = {
    "admin": "admin",
    "diacono01": "diacono",
    "diacono02": "diacono",
    "diacono03": "diacono"
}

NOMES_USUARIOS = {
    "admin": "Administrador",
    "diacono01": "Diácono01",
    "diacono02": "Diácono02",
    "diacono03": "Diácono03"
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
# CONFIGURAÇÕES DE EMAIL (NEWSLETTER)
# ============================================

def str_to_bool(value, default=False):
    """Converte string para booleano com fallback seguro."""
    if value is None:
        return default
    return str(value).strip().lower() in {"1", "true", "t", "yes", "y", "on"}


SMTP_ENABLED = str_to_bool(get_secret("SMTP_ENABLED"), default=False)
SMTP_HOST = get_secret("SMTP_HOST")
SMTP_PORT = int(get_secret("SMTP_PORT") or 587)
SMTP_USER = get_secret("SMTP_USER")
SMTP_PASSWORD = get_secret("SMTP_PASSWORD")
SMTP_FROM_NAME = get_secret("SMTP_FROM_NAME") or "Sistema de Dízimos e Ofertas"
SMTP_FROM_EMAIL = get_secret("SMTP_FROM_EMAIL") or SMTP_USER
SMTP_USE_TLS = str_to_bool(get_secret("SMTP_USE_TLS"), default=True)


# ============================================
# CONFIGURAÇÕES RAPIDAPI (CORRETOR ORTOGRÁFICO)
# ============================================

JSPELL_API_URL = get_secret("JSPELL_API_URL") or "https://jspell-checker.p.rapidapi.com/check"
JSPELL_API_HOST = get_secret("JSPELL_API_HOST") or "jspell-checker.p.rapidapi.com"
JSPELL_API_KEY = get_secret("JSPELL_API_KEY") or get_secret("RAPIDAPI_KEY")
JSPELL_TIMEOUT_SECONDS = int(get_secret("JSPELL_TIMEOUT_SECONDS") or 20)

