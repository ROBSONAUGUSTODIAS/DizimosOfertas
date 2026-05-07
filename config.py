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

