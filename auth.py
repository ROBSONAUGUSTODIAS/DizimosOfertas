"""
Módulo de Autenticação e Autorização
Sistema Seguro com Hash de Senhas usando Bcrypt
"""
from typing import Optional, Dict
import bcrypt
from config import USUARIOS_HASHES, NIVEIS_ACESSO, NOMES_USUARIOS


def verificar_senha_hash(senha: str, hash_armazenado: str) -> bool:
    """
    Verifica se a senha corresponde ao hash armazenado
    
    Args:
        senha: Senha em texto plano fornecida pelo usuário
        hash_armazenado: Hash bcrypt armazenado no sistema
    
    Returns:
        True se a senha está correta, False caso contrário
    """
    try:
        # Converte senha e hash para bytes
        senha_bytes = senha.encode('utf-8')
        hash_bytes = hash_armazenado.encode('utf-8')
        
        # Verifica se a senha corresponde ao hash
        return bcrypt.checkpw(senha_bytes, hash_bytes)
    except Exception as e:
        print(f"Erro ao verificar senha: {e}")
        return False


def verificar_login(usuario: str, senha: str) -> Optional[Dict[str, str]]:
    """
    Verifica as credenciais do usuário usando hash bcrypt
    
    Args:
        usuario: Nome de usuário
        senha: Senha do usuário em texto plano
    
    Returns:
        Dict com informações do usuário se válido, None caso contrário
    """
    # Debug: mostra informações de login
    print(f"\n=== DEBUG LOGIN ===")
    print(f"Usuário tentando logar: {usuario}")
    print(f"Usuários disponíveis: {list(USUARIOS_HASHES.keys())}")
    
    # Verifica se o usuário existe
    if usuario not in USUARIOS_HASHES:
        print(f"❌ Usuário '{usuario}' não existe")
        return None
    
    # Obtém o hash armazenado
    hash_armazenado = USUARIOS_HASHES[usuario]
    
    # Debug: verifica se hash existe
    if not hash_armazenado:
        print(f"⚠️ Hash não configurado para o usuário: {usuario}")
        print(f"USUARIOS_HASHES[{usuario}] = {hash_armazenado}")
        return None
    
    print(f"✓ Hash encontrado: {hash_armazenado[:20]}...")
    print(f"✓ Tamanho da senha: {len(senha)} caracteres")
    
    # Verifica a senha
    senha_valida = verificar_senha_hash(senha, hash_armazenado)
    print(f"✓ Senha válida: {senha_valida}")
    print(f"==================\n")
    
    if senha_valida:
        return {
            "usuario": usuario,
            "nome": NOMES_USUARIOS.get(usuario, usuario),
            "nivel": NIVEIS_ACESSO.get(usuario, "visualizador")
        }
    
    return None


def tem_permissao(nivel_acesso: str, permissao_requerida: str) -> bool:
    """
    Verifica se o nível de acesso tem a permissão necessária
    
    Args:
        nivel_acesso: Nível de acesso do usuário
        permissao_requerida: Permissão requerida (visualizador, editor, admin)
    
    Returns:
        True se tem permissão, False caso contrário
    """
    hierarquia = {
        "visualizador": 1,
        "editor": 2,
        "admin": 3
    }
    
    nivel_atual = hierarquia.get(nivel_acesso, 0)
    nivel_requerido = hierarquia.get(permissao_requerida, 999)
    
    return nivel_atual >= nivel_requerido


def pode_editar(nivel_acesso: str) -> bool:
    """Verifica se o usuário pode editar lançamentos"""
    return nivel_acesso in ["admin", "editor"]


def pode_administrar(nivel_acesso: str) -> bool:
    """Verifica se o usuário pode administrar (editar/excluir todos os registros)"""
    return nivel_acesso == "admin"
