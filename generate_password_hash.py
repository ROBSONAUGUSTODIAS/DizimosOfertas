"""
Utilitário para Gerar Hash de Senhas
Use este script para gerar hashes seguros para as senhas dos usuários
"""
import bcrypt


def gerar_hash(senha: str) -> str:
    """
    Gera um hash bcrypt para a senha fornecida
    
    Args:
        senha: Senha em texto plano
    
    Returns:
        Hash da senha em formato string
    """
    # Gera o salt e cria o hash
    salt = bcrypt.gensalt()
    senha_bytes = senha.encode('utf-8')
    hash_bytes = bcrypt.hashpw(senha_bytes, salt)
    
    # Retorna o hash como string
    return hash_bytes.decode('utf-8')


def main():
    """Função principal para gerar hashes interativamente"""
    print("=" * 60)
    print("🔐 GERADOR DE HASH DE SENHAS")
    print("=" * 60)
    print("\nUse este script para gerar hashes seguros para suas senhas.")
    print("Os hashes gerados devem ser adicionados ao arquivo .env\n")
    
    while True:
        print("\n" + "-" * 60)
        usuario = input("Digite o nome do usuário (ou 'sair' para encerrar): ")
        
        if usuario.lower() == 'sair':
            print("\n✅ Encerrando...")
            break
        
        senha = input("Digite a senha: ")
        
        if len(senha) < 6:
            print("❌ A senha deve ter pelo menos 6 caracteres!")
            continue
        
        hash_gerado = gerar_hash(senha)
        
        print(f"\n✅ Hash gerado para '{usuario}':")
        print("-" * 60)
        print(f"USER_{usuario.upper()}_HASH={hash_gerado}")
        print("-" * 60)
        print("\n💡 Copie a linha acima e adicione ao arquivo .env")


if __name__ == "__main__":
    main()
