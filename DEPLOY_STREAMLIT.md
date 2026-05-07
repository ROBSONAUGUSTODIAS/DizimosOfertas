# 🚀 GUIA DE DEPLOY - STREAMLIT CLOUD

## 📋 Pré-requisitos

✅ Repositório GitHub público ou privado  
✅ Arquivo `.env` com suas credenciais locais  
✅ Banco de dados vazio no repositório (dados sensíveis protegidos)  

---

## 🌐 PASSO 1: Preparar o Repositório

### ✅ Verificar Arquivos Protegidos

```bash
# Verificar o que está sendo ignorado
git status

# ❌ NÃO deve aparecer:
# - .env
# - .streamlit/secrets.toml
# - dizimos_ofertas_BACKUP.db
# - __pycache__/
```

### ✅ Arquivos que DEVEM Estar no Repositório

```
✅ app.py
✅ auth.py
✅ config.py (com suporte a st.secrets)
✅ database.py
✅ mobile_config.py
✅ utils.py
✅ whatsapp_service.py
✅ notifications.py
✅ requirements.txt
✅ dizimos_ofertas.db (vazio)
✅ modules/ (todos os .py)
✅ README.md
✅ .gitignore
```

---

## ☁️ PASSO 2: Deploy no Streamlit Cloud

### 1. Acessar Streamlit Cloud

🌐 **URL:** https://share.streamlit.io/

### 2. Fazer Login

- Clique em **Sign in**
- Use sua conta GitHub
- Autorize o acesso ao Streamlit

### 3. Criar Novo App

- Clique em **New app**
- Selecione:
  - **Repository:** `ROBSONAUGUSTODIAS/DizimosOfertas`
  - **Branch:** `main`
  - **Main file path:** `app.py`
- Clique em **Deploy!**

---

## 🔐 PASSO 3: Configurar Secrets (CRÍTICO!)

### ⚠️ ATENÇÃO: Sem esta configuração, o app NÃO funcionará!

1. **No painel do Streamlit Cloud:**
   - Vá em **Settings** (engrenagem) → **Secrets**

2. **Cole o conteúdo do arquivo `.env`** no formato TOML:

```toml
# ========================================
# CONFIGURAÇÃO DE SECRETS - STREAMLIT CLOUD
# ========================================

[passwords]
USER_ADMIN_HASH = "$2b$12$SUA_HASH_ADMIN_AQUI"
USER_DIACONO01_HASH = "$2b$12$SUA_HASH_DIACONO01_AQUI"
USER_DIACONO02_HASH = "$2b$12$SUA_HASH_DIACONO02_AQUI"

[twilio]
TWILIO_ACCOUNT_SID = "seu_account_sid_aqui"
TWILIO_AUTH_TOKEN = "seu_auth_token_aqui"
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"

[pix]
PIX_CHAVE = "sua_chave_pix_aqui"
PIX_BENEFICIARIO = "Nome da Igreja"
```

### 📝 Como Obter os Hashes?

**Opção 1: Do arquivo `.env` local:**
```bash
cat .env
```

**Opção 2: Gerar novos hashes:**
```bash
python generate_password_hash.py
```

3. **Clique em Save**

---

## ✅ PASSO 4: Configurações Adicionais (Opcional)

### Configurações Avançadas

No painel **Settings** → **Advanced settings**:

```
Python version: 3.11
```

### Configurar Domínio Customizado (Opcional)

1. Settings → **General**
2. Em **App URL**, você pode customizar:
   - `dizimos-ofertas.streamlit.app` (exemplo)

---

## 🧪 PASSO 5: Testar o Deploy

### 1. Aguardar Deploy

- O Streamlit Cloud vai instalar as dependências
- Tempo estimado: 2-5 minutos
- Você verá os logs em tempo real

### 2. Testar Login

Acesse a URL do app e tente fazer login:

```
Usuário: admin
Senha: SENHA_ADMIN_EXEMPLO
```

### 3. Testar Funcionalidades

✅ **Visualizar:** Métricas e tabelas  
✅ **Registrar:** Novo lançamento  
✅ **Editar:** Modificar/deletar (admin)  
✅ **Mobile:** Testar no celular  

---

## 🔧 PASSO 6: Gerenciar Banco de Dados

### ⚠️ Banco de Dados SQLite no Streamlit Cloud

**IMPORTANTE:** O Streamlit Cloud usa sistema de arquivos **efêmero**!

- ❌ Dados são **perdidos** quando o app reinicia
- ❌ Cada sessão tem seu próprio banco
- ❌ Não é adequado para produção com dados reais

### 🎯 Soluções para Persistência de Dados:

#### Opção 1: PostgreSQL (Recomendado)
```bash
# Usar banco PostgreSQL remoto (Supabase, Render, etc)
pip install psycopg2-binary
```

#### Opção 2: Google Sheets
```bash
# Usar Google Sheets como banco de dados
pip install gspread oauth2client
```

#### Opção 3: Firebase/Firestore
```bash
# Usar Firebase Firestore
pip install firebase-admin
```

#### Opção 4: Turso/LibSQL (SQLite na nuvem)
```bash
# SQLite compatível hospedado
pip install libsql-client
```

### 📝 Para Testes/Demo (SQLite Atual)

- ✅ Funciona para demonstração
- ✅ Bom para protótipos
- ❌ Dados não persistem entre deploys

---

## 🛠️ TROUBLESHOOTING

### Erro: "Missing Secrets"

**Problema:** Secrets não configurados

**Solução:**
1. Settings → Secrets
2. Cole o conteúdo do `.env` no formato TOML
3. Save e aguarde restart

### Erro: "ModuleNotFoundError"

**Problema:** Dependência faltando

**Solução:**
1. Verificar `requirements.txt` tem todas as dependências
2. Fazer commit e push
3. App reinicia automaticamente

### Erro: Login Não Funciona

**Problema:** Hash de senha incorreto

**Solução:**
1. Gerar novo hash: `python generate_password_hash.py`
2. Atualizar em Settings → Secrets
3. Testar novamente

### App Fica Reiniciando

**Problema:** Erro no código ou secrets

**Solução:**
1. Ver logs em **Manage app** → **Logs**
2. Corrigir erro
3. Fazer commit e push

---

## 📊 MONITORAMENTO

### Ver Logs em Tempo Real

1. **Manage app** → **Logs**
2. Ver erros e warnings
3. Debug de problemas

### Métricas de Uso

1. **Analytics** (se disponível)
2. Ver número de visitantes
3. Performance do app

### Reiniciar App Manualmente

1. **⋮** (três pontos) → **Reboot app**
2. Útil após mudanças em Secrets

---

## 🔄 ATUALIZAÇÕES

### Atualizar Código

```bash
# Fazer alterações locais
git add .
git commit -m "✨ Nova feature"
git push origin main

# Streamlit Cloud detecta e faz redeploy automático
```

### Atualizar Secrets

1. Settings → Secrets
2. Editar valores
3. Save (app reinicia automaticamente)

### Atualizar Dependências

1. Editar `requirements.txt`
2. Commit e push
3. Deploy automático

---

## 🔐 SEGURANÇA: CHECKLIST FINAL

Antes de publicar, verifique:

- [ ] `.env` NÃO está no repositório
- [ ] `.streamlit/secrets.toml` está no `.gitignore`
- [ ] Banco de dados está vazio (sem dados reais)
- [ ] Secrets configurados no Streamlit Cloud
- [ ] README não contém senhas
- [ ] Documentação sem credenciais
- [ ] Testado login no app publicado
- [ ] WhatsApp/Twilio com credenciais corretas

---

## 📱 TESTAR MOBILE

### Navegadores Suportados

✅ Chrome (Android/Desktop)  
✅ Safari (iOS/macOS)  
✅ Firefox (Android/Desktop)  
✅ Edge (Desktop)  

### Teste Responsivo

1. Abra a URL do app no celular
2. Teste todas as funcionalidades:
   - Login
   - Visualizar métricas
   - Scroll horizontal nas tabelas
   - Registrar novo lançamento
   - Editar lançamento
   - Sidebar (abrir/fechar)

---

## 🎯 URLs IMPORTANTES

### Streamlit Cloud
- **Dashboard:** https://share.streamlit.io/
- **Documentação:** https://docs.streamlit.io/streamlit-community-cloud

### Seu App
- **URL Pública:** `https://[seu-app].streamlit.app`
- **Settings:** Acessível pelo dashboard

### GitHub
- **Repositório:** https://github.com/ROBSONAUGUSTODIAS/DizimosOfertas
- **Settings:** Para configurar webhooks (opcional)

---

## 💡 DICAS PRO

### 1. Badge no README

Adicione um badge do status do app:

```markdown
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://[seu-app].streamlit.app)
```

### 2. Custom Domain

- Possível com plano pago
- Permite usar `dizimos.suaigreja.com`

### 3. Analytics

- Integrar Google Analytics
- Monitorar uso real

### 4. Backup Automático

- Script para backup do banco
- Salvar em Google Drive/Dropbox

### 5. Notificações

- Email quando app falha
- Webhook para Slack/Discord

---

## ✅ RESULTADO FINAL

Após concluir todos os passos:

✅ **App online** em `https://[seu-app].streamlit.app`  
✅ **Seguro:** Senhas com bcrypt, secrets protegidos  
✅ **Responsivo:** Funciona em mobile e desktop  
✅ **Atualização automática:** Push no GitHub = deploy automático  
✅ **Logs:** Monitoramento em tempo real  
✅ **SSL:** HTTPS automático  

---

## 🆘 SUPORTE

### Problemas com Deploy?

1. **Documentação Streamlit:** https://docs.streamlit.io/
2. **Fórum Streamlit:** https://discuss.streamlit.io/
3. **GitHub Issues:** Criar issue no seu repositório

### Problemas com o App?

1. Ver logs: Manage app → Logs
2. Testar localmente: `streamlit run app.py`
3. Verificar secrets: Formato TOML correto?

---

**🎉 Parabéns! Seu app está no ar!**

---

**Criado em:** 07 de Fevereiro de 2026  
**Versão:** 1.0  
**Autor:** Sistema de Gestão de Dízimos e Ofertas
