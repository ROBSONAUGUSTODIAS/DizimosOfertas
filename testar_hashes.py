"""
Script de Teste de Hashes - Verificação de Autenticação
Use este script para testar se os hashes estão corretos
"""
import bcrypt

# Hashes configurados
HASHES = {
    "admin": "$2b$12$kKdAncvxkviV412Bj.WuMe2ve/Qaqkn4sq1CiFXh.QeWF6Bp1hXbq",
    "diacono01": "$2b$12$7erenEeA2eP5HecUUGGtp.LRxYuxXqYWKb/zNwT8VOIpM6UyeWMEy",
    "diacono02": "$2b$12$7rxfZGjQqq9cOnpaiRvRnu9vLhNKmKVAFh2zwEvfC9fdaaqmEfSN."
}

# Senhas de teste
SENHAS_TESTE = {
    "admin": "AdminSeguro@2026",
    "diacono01": "Diacono01@2026",
    "diacono02": "Diacono02@2026"
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
    
    print("Testando hashes configurados...\n")
    
    todos_ok = True
    for usuario in HASHES.keys():
        senha = SENHAS_TESTE[usuario]
        hash_val = HASHES[usuario]
        
        print(f"\nUsuário: {usuario}")
        print(f"Senha: {senha}")
        print(f"Hash: {hash_val[:30]}...")
        
        resultado = testar_hash(usuario, senha, hash_val)
        todos_ok = todos_ok and resultado
    
    print("\n" + "="*60)
    if todos_ok:
        print("✅ TODOS OS HASHES ESTÃO CORRETOS!")
        print("\nVocê pode usar estas credenciais no sistema:")
        for usuario, senha in SENHAS_TESTE.items():
            print(f"  • {usuario}: {senha}")
    else:
        print("❌ ALGUNS HASHES ESTÃO INCORRETOS!")
        print("\nExecute: python generate_password_hash.py")
        print("Para gerar novos hashes.")
    print("="*60 + "\n")
    
    # Teste interativo
    print("\n🔧 TESTE CUSTOMIZADO")
    print("Digite 'sair' para encerrar\n")
    
    while True:
        usuario_teste = input("Digite o usuário (admin/diacono01/diacono02): ").strip()
        
        if usuario_teste.lower() == 'sair':
            break
        
        if usuario_teste not in HASHES:
            print(f"❌ Usuário '{usuario_teste}' não encontrado!")
            continue
        
        senha_teste = input("Digite a senha: ").strip()
        
        hash_val = HASHES[usuario_teste]
        testar_hash(usuario_teste, senha_teste, hash_val)
        print()
