"""
Script de Diagnóstico - Verificar carregamento de configurações
"""
import os
from dotenv import load_dotenv

print("\n" + "="*60)
print("DIAGNÓSTICO DE CONFIGURAÇÃO")
print("="*60 + "\n")

# Verificar se arquivo .env existe
env_path = ".env"
if os.path.exists(env_path):
    print(f"✅ Arquivo .env encontrado em: {os.path.abspath(env_path)}")
else:
    print(f"❌ Arquivo .env NÃO encontrado!")
    exit(1)

# Carregar variáveis
print("\nCarregando variáveis do .env...")
load_dotenv()

# Verificar hashes
print("\n" + "-"*60)
print("VERIFICANDO HASHES CARREGADOS:")
print("-"*60)

usuarios = ["admin", "diacono01", "diacono02"]

for usuario in usuarios:
    key = f"USER_{usuario.upper()}_HASH"
    valor = os.getenv(key)
    
    print(f"\n{usuario}:")
    print(f"  Chave: {key}")
    if valor:
        print(f"  ✅ Hash carregado: {valor[:20]}... (tamanho: {len(valor)})")
        if len(valor) != 60:
            print(f"  ⚠️ AVISO: Hash deveria ter 60 caracteres!")
    else:
        print(f"  ❌ Hash NÃO carregado!")

# Testar importação do config
print("\n" + "-"*60)
print("TESTANDO IMPORTAÇÃO DE config.py:")
print("-"*60)

try:
    from config import USUARIOS_HASHES
    print("\n✅ config.py importado com sucesso!")
    
    print("\nHashes disponíveis em USUARIOS_HASHES:")
    for usuario, hash_val in USUARIOS_HASHES.items():
        if hash_val:
            print(f"  ✅ {usuario}: {hash_val[:20]}... (tamanho: {len(hash_val)})")
        else:
            print(f"  ❌ {usuario}: None ou vazio")
            
except Exception as e:
    print(f"\n❌ Erro ao importar config: {e}")

print("\n" + "="*60)
print("FIM DO DIAGNÓSTICO")
print("="*60 + "\n")
