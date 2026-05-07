"""
Script de Teste de Hashes - Verificação de Autenticação
Use este script para testar se os hashes estão corretos
"""
import os
import bcrypt

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# Hashes configurados
HASHES = {
    "admin": os.getenv("USER_ADMIN_HASH", ""),
    "diacono01": os.getenv("USER_DIACONO01_HASH", ""),
    "diacono02": os.getenv("USER_DIACONO02_HASH", ""),
    "diacono03": os.getenv("USER_DIACONO03_HASH", ""),
}

def testar_hash(usuario, senha, hash_esperado):
    """Testa se a senha corresponde ao hash"""
    try:
        senha_bytes = senha.encode('utf-8')
        hash_bytes = hash_esperado.encode('utf-8')
        resultado = bcrypt.checkpw(senha_bytes, hash_bytes)
        
        if resultado:
            print(f"✅ {usuario}: SENHA CORRETA")
        else:
            print(f"❌ {usuario}: SENHA INCORRETA")
        
        return resultado
    except Exception as e:
        print(f"⚠️ {usuario}: ERRO - {e}")
        return False

if __name__ == "__main__":
    print("\n" + "="*60)
    print("TESTE DE HASHES - Sistema de Dízimos e Ofertas")
    print("="*60 + "\n")
    print("Hashes carregados de variáveis de ambiente (.env ou secrets).\n")
    for usuario, hash_val in HASHES.items():
        status = "✅ configurado" if hash_val else "❌ não configurado"
        print(f"{usuario}: {status}")

    print("\n" + "="*60 + "\n")
    
    # Teste interativo
    print("\n🔧 TESTE CUSTOMIZADO")
    print("Digite 'sair' para encerrar\n")
    
    while True:
        usuario_teste = input("Digite o usuário (admin/diacono01/diacono02/diacono03): ").strip()
        
        if usuario_teste.lower() == 'sair':
            break
        
        if usuario_teste not in HASHES:
            print(f"❌ Usuário '{usuario_teste}' não encontrado!")
            continue

        hash_val = HASHES.get(usuario_teste, "")
        if not hash_val:
            print(f"⚠️ Hash não configurado para '{usuario_teste}' no ambiente.")
            continue
        
        senha_teste = input("Digite a senha: ").strip()

        testar_hash(usuario_teste, senha_teste, hash_val)
        print()
