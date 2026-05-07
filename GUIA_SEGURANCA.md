# 🔐 Guia de Segurança - Login e Senha

## ⚠️ IMPORTANTE - Leia Antes de Publicar

Este documento explica como o sistema de autenticação seguro funciona e como configurá-lo corretamente antes de publicar no Streamlit Cloud.

## 🎯 O Que Foi Implementado

### 1. **Hash de Senhas com Bcrypt**
- ✅ Senhas nunca são armazenadas em texto plano
- ✅ Utiliza algoritmo bcrypt com salt automático
- ✅ Proteção contra força bruta e rainbow tables
- ✅ Impossível recuperar a senha original a partir do hash

### 2. **Variáveis de Ambiente**
- ✅ Credenciais armazenadas em arquivo `.env`
- ✅ Arquivo `.env` no `.gitignore` (não vai para o GitHub)
- ✅ Código-fonte não contém senhas
- ✅ Compatível com Streamlit Cloud Secrets

### 3. **Arquivos de Configuração**
- `.env` - Arquivo com credenciais reais (NÃO compartilhar)
- `.env.example` - Modelo sem dados sensíveis (pode compartilhar)
- `.gitignore` - Protege `.env` de ser enviado ao GitHub
- `generate_password_hash.py` - Script para gerar novos hashes

## 🚀 Como Usar Localmente

### Passo 1: Instalar Dependências
```bash
pip install -r requirements.txt
```

### Passo 2: Configurar Senhas (Primeira Vez)

O arquivo `.env` já foi criado com senhas de TESTE. 

**Senhas de TESTE atuais:**
- Usuário: `admin` | Senha: `SENHA_ADMIN_EXEMPLO`
- Usuário: `diacono01` | Senha: `SENHA_DIACONO01_EXEMPLO`
- Usuário: `diacono02` | Senha: `SENHA_DIACONO02_EXEMPLO`

**Para criar suas próprias senhas:**

1. Execute o gerador:
```bash
python generate_password_hash.py
```

2. Siga as instruções interativas:
```
Digite o nome do usuário: admin
Digite a senha: suaSenhaForte@123
```

3. Copie o hash gerado:
```
USER_ADMIN_HASH=$2b$12$abc123...xyz789
```

4. Cole no arquivo `.env`

### Passo 3: Executar a Aplicação
```bash
streamlit run app.py
```

## 🌐 Como Publicar no Streamlit Cloud

### ⚠️ ATENÇÃO: NÃO Envie o Arquivo .env para o GitHub!

O arquivo `.gitignore` já está configurado para proteger o `.env`, mas verifique:

```bash
# Ver o que será enviado ao git
git status

# O .env NÃO deve aparecer na lista!
# Se aparecer, adicione ao .gitignore
```

### Configurar Secrets no Streamlit Cloud

1. **Faça Push do Código para o GitHub** (sem o .env)
```bash
git add .
git commit -m "Sistema com autenticação segura"
git push origin main
```

2. **No Streamlit Cloud:**
   - Acesse: https://share.streamlit.io
   - Selecione seu app
   - Clique em **⚙️ Settings**
   - Vá em **Secrets**
   - Cole o conteúdo do seu arquivo `.env`:

```toml
USER_ADMIN_HASH = "$2b$12$seu_hash_completo_aqui"
USER_DIACONO01_HASH = "$2b$12$seu_hash_completo_aqui"
USER_DIACONO02_HASH = "$2b$12$seu_hash_completo_aqui"

WHATSAPP_ENABLED = "false"
TWILIO_ACCOUNT_SID = "seu_account_sid"
TWILIO_AUTH_TOKEN = "seu_auth_token"
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"
```

3. **Salve e Reinicie o App**

## 🔒 Boas Práticas de Segurança

### ✅ Senhas Fortes

**O que é uma senha forte?**
- Mínimo 12 caracteres
- Letras maiúsculas: A-Z
- Letras minúsculas: a-z
- Números: 0-9
- Símbolos: !@#$%^&*

**Exemplos de senhas fortes:**
- `Igreja@Segura#2026!`
- `Diacono$Forte123@`
- `Admin&Protegido2026#`

**❌ Evite:**
- Senhas curtas (menos de 8 caracteres)
- Palavras do dicionário
- Informações pessoais (nome, data de nascimento)
- Sequências óbvias (123456, abcdef)
- Senha igual para todos os usuários

### 🛡️ Gerenciamento de Usuários

**Localização:** [config.py](config.py)

```python
# Adicionar novo usuário
USUARIOS_HASHES = {
    "admin": os.getenv('USER_ADMIN_HASH'),
    "diacono01": os.getenv('USER_DIACONO01_HASH'),
    "diacono02": os.getenv('USER_DIACONO02_HASH'),
    "novousuario": os.getenv('USER_NOVOUSUARIO_HASH'),  # ← Adicione aqui
}

NIVEIS_ACESSO = {
    "admin": "admin",
    "diacono01": "admin",
    "diacono02": "admin",
    "novousuario": "editor",  # ← Defina nível
}

NOMES_USUARIOS = {
    "admin": "Administrador",
    "diacono01": "Diácono01",
    "diacono02": "Diácono02",
    "novousuario": "Nome Completo",  # ← Adicione nome
}
```

**Passos para adicionar usuário:**

1. Edite `config.py` conforme acima
2. Gere o hash da senha:
```bash
python generate_password_hash.py
```
3. Adicione ao `.env`:
```env
USER_NOVOUSUARIO_HASH=$2b$12$hash_gerado
```
4. Reinicie a aplicação

### 📋 Níveis de Acesso

| Nível | Permissões |
|-------|-----------|
| **admin** | Tudo: visualizar, registrar, editar, excluir |
| **editor** | Visualizar e registrar lançamentos |
| **visualizador** | Apenas visualizar lançamentos |

## 🔍 Verificação de Segurança

### Checklist antes de publicar:

- [ ] Arquivo `.env` no `.gitignore`
- [ ] `.env` NÃO enviado para o GitHub
- [ ] Senhas fortes configuradas
- [ ] Hashes únicos para cada usuário
- [ ] Secrets configurados no Streamlit Cloud
- [ ] Testado localmente antes de publicar
- [ ] Credenciais do Twilio (se usando WhatsApp) protegidas

### Comandos de verificação:

```bash
# Verificar se .env está ignorado
git check-ignore .env
# Deve retornar: .env

# Ver arquivos que serão enviados
git status
# .env NÃO deve aparecer!

# Testar login local
streamlit run app.py
# Tente fazer login com as credenciais configuradas
```

## 🆘 Solução de Problemas

### ❌ "Hash não configurado para o usuário"

**Causa:** Falta o hash no arquivo `.env`

**Solução:**
1. Verifique se o arquivo `.env` existe
2. Confirme se a variável está definida:
```env
USER_ADMIN_HASH=$2b$12$...
```
3. Reinicie o Streamlit

### ❌ "Credenciais inválidas"

**Causas possíveis:**
1. Senha digitada incorretamente
2. Hash não corresponde à senha
3. Arquivo `.env` não carregado

**Solução:**
1. Confirme a senha correta
2. Gere novo hash: `python generate_password_hash.py`
3. Atualize o `.env`
4. Reinicie o Streamlit

### ❌ "ModuleNotFoundError: No module named 'bcrypt'"

**Causa:** Biblioteca não instalada

**Solução:**
```bash
pip install -r requirements.txt
```

### ❌ No Streamlit Cloud: Login não funciona

**Causa:** Secrets não configurados

**Solução:**
1. Acesse Settings → Secrets no Streamlit Cloud
2. Cole o conteúdo do `.env`
3. Salve e reinicie o app

## 📚 Arquivos Importantes

| Arquivo | Descrição | Compartilhar? |
|---------|-----------|---------------|
| `.env` | Credenciais reais | ❌ NUNCA |
| `.env.example` | Modelo sem dados sensíveis | ✅ SIM |
| `.gitignore` | Proteção de arquivos | ✅ SIM |
| `config.py` | Configuração do sistema | ✅ SIM |
| `auth.py` | Lógica de autenticação | ✅ SIM |
| `generate_password_hash.py` | Gerador de hashes | ✅ SIM |

## 📖 Documentação Adicional

- [README.md](README.md) - Documentação completa do sistema
- [DOCUMENTACAO_TECNICA.md](DOCUMENTACAO_TECNICA.md) - Detalhes técnicos
- [bcrypt documentation](https://github.com/pyca/bcrypt/) - Biblioteca bcrypt
- [Streamlit Secrets](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management) - Gerenciamento de secrets

## 🎓 Entendendo o Sistema

### Como funciona o hash bcrypt?

```python
# 1. Usuário cria senha
senha = "MinhaSenh@123"

# 2. Sistema gera salt aleatório
salt = bcrypt.gensalt()
# Resultado: $2b$12$NzQ3ODkxMjM0NTY3ODkw

# 3. Sistema combina senha + salt e gera hash
hash = bcrypt.hashpw(senha.encode(), salt)
# Resultado: $2b$12$NzQ3ODkxM...abc123xyz

# 4. Hash é armazenado (senha nunca é salva!)
# No .env: USER_ADMIN_HASH=$2b$12$NzQ3ODkxM...abc123xyz

# 5. No login, verifica senha contra hash
bcrypt.checkpw(senha_digitada.encode(), hash_armazenado)
# Retorna True se corresponder, False caso contrário
```

**Por que é seguro?**
- Hash é unidirecional (não pode reverter)
- Salt único para cada senha
- Milhares de iterações (lento = seguro)
- Mesmo senha gera hashes diferentes

## 📞 Suporte

Se tiver dúvidas ou problemas:

1. Consulte a seção 🔐 Segurança e Autenticação do README
2. Verifique os erros no terminal/logs
3. Execute os comandos de verificação acima
4. Revise o checklist de segurança

---

**🔐 Lembre-se: A segurança da aplicação depende de senhas fortes e proteção adequada das credenciais!**
