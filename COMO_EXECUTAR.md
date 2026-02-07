# 🚀 Como Executar a Aplicação

Guia passo a passo para executar o Sistema de Gestão de Dízimos e Ofertas.

---

## 📋 Pré-requisitos

Antes de executar, certifique-se de ter instalado:

- ✅ **Python 3.8 ou superior**
  - Verificar versão: `python --version`
  - Download: https://www.python.org/downloads/

- ✅ **pip** (gerenciador de pacotes Python)
  - Geralmente vem com Python
  - Verificar: `pip --version`

---

## ⚡ Início Rápido (3 passos)

### 1️⃣ Instalar Dependências

Abra o terminal/PowerShell na pasta do projeto e execute:

```bash
pip install -r requirements.txt
```

**O que será instalado:**
- `streamlit` - Framework web
- `pandas` - Manipulação de dados
- `streamlit-option-menu` - Menu lateral
- `Pillow` - Processamento de imagens
- `twilio` - Integração WhatsApp

### 2️⃣ Executar o Sistema

```bash
streamlit run app.py
```

### 3️⃣ Acessar no Navegador

O navegador abrirá automaticamente em:
```
http://localhost:8501
```

Se não abrir automaticamente, copie e cole o link no navegador.

---

## 🔐 Login no Sistema

Use as credenciais padrão:

| Usuário | Senha | Nível de Acesso |
|---------|-------|-----------------|
| `admin` | `Admin@#` | Administrador (acesso completo) |
| `tesoureiro` | `teseoureiro@#` | Editor (visualizar + registrar) |
| `pastor` | `pastor@#` | Visualizador (apenas visualizar) |
| `diacono01` | `diacono01@#` | Administrador |
| `diacono02` | `diacono02@#` | Administrador |

**Recomendação de Segurança:** Altere as senhas padrão no arquivo `config.py` antes do uso em produção.

---

## 📱 Configurar WhatsApp (Opcional)

O sistema funciona perfeitamente **sem** WhatsApp configurado. 

**⚠️ IMPORTANTE**: WhatsApp é enviado **APENAS para pagamentos PIX**!

Para habilitar o envio de mensagens:

### Primeira Vez:

1. Siga o guia completo: **`WHATSAPP_SETUP.md`**
2. Configure as credenciais no arquivo `.env`
3. Reinicie o sistema

### Arquivo `.env`:

Crie um arquivo chamado `.env` na pasta do projeto:

```env
WHATSAPP_ENABLED=true
TWILIO_ACCOUNT_SID=seu_account_sid_aqui
TWILIO_AUTH_TOKEN=seu_auth_token_aqui
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

**Sem Twilio configurado:** O sistema funciona normalmente, apenas não enviará WhatsApp.

---

## 💻 Comandos Detalhados

### Windows (PowerShell/CMD):

```powershell
# Navegar até a pasta do projeto
cd D:\PROTOTIPO\DizimosOfertas

# Instalar dependências
pip install -r requirements.txt

# Executar aplicação
streamlit run app.py

# OU com porta específica
streamlit run app.py --server.port=8000

# OU usando módulo python
python -m streamlit run app.py
```

### Linux/Mac (Terminal):

```bash
# Navegar até a pasta do projeto
cd /caminho/para/DizimosOfertas

# Instalar dependências
pip install -r requirements.txt

# Executar aplicação
streamlit run app.py

# OU com porta específica
streamlit run app.py --server.port=8000
```

### Usando Ambiente Virtual (Recomendado):

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
## Windows:
venv\Scripts\activate

## Linux/Mac:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Executar aplicação
streamlit run app.py
```

---

## 🎯 Usando o Sistema

### 1. Visualizar Lançamentos

- Faça login
- Menu lateral → **"Visualizar"**
- Veja todos os lançamentos registrados
- Resumo financeiro com gráficos

### 2. Registrar Nova Contribuição

- Menu lateral → **"Registrar"** (apenas editor/admin)
- Preencha os dados:
  - Nome do contribuinte
  - Valor da contribuição
  - **Tipo de pagamento** (selecione PIX para habilitar WhatsApp)
  - Categoria (Dízimo/Oferta/Visitante)
  - **Celular** (obrigatório para WhatsApp)
  - Email (opcional)
- ⚠️ **Atenção**: Checkbox "Enviar confirmação via WhatsApp" **só aparece se tipo = PIX**
- Marque: ☑️ "Enviar confirmação via WhatsApp" (se PIX)
- Clique em **"Registrar Lançamento"**

### 3. Editar/Excluir Lançamentos

- Menu lateral → **"Editar"** (apenas admin)
- Selecione o lançamento
- Clique em **"Atualizar"** ou **"Excluir"**

---

## 🛠️ Solução de Problemas

### ❌ "streamlit: comando não encontrado"

**Problema:** Streamlit não está instalado ou não está no PATH.

**Solução:**
```bash
# Instalar streamlit
pip install streamlit

# OU usar módulo python
python -m streamlit run app.py
```

---

### ❌ "ModuleNotFoundError: No module named 'streamlit'"

**Problema:** Dependências não instaladas.

**Solução:**
```bash
pip install -r requirements.txt
```

---

### ❌ "Port 8501 is already in use"

**Problema:** Porta já está sendo usada.

**Solução 1 - Usar outra porta:**
```bash
streamlit run app.py --server.port=8502
```

**Solução 2 - Fechar processo na porta:**
```powershell
# Windows
netstat -ano | findstr :8501
taskkill /PID <numero_do_pid> /F

# Linux/Mac
lsof -ti:8501 | xargs kill -9
```

---

### ❌ Erro ao enviar WhatsApp

**Problema:** Credenciais Twilio não configuradas.

**Solução:**
1. O sistema funciona SEM WhatsApp configurado
2. Para habilitar, siga: `WHATSAPP_SETUP.md`
3. Configure arquivo `.env` com credenciais Twilio

---

### ❌ Banco de dados corrompido

**Problema:** Erros ao acessar/salvar dados.

**Solução - Recriar banco:**
```bash
# ATENÇÃO: Isso apaga todos os dados!

# Windows (PowerShell)
Remove-Item -Force dizimos_ofertas.db

# Linux/Mac
rm dizimos_ofertas.db

# Reiniciar aplicação
streamlit run app.py
```

O banco será recriado automaticamente vazio.

---

### ❌ Logo não aparece

**Problema:** Arquivo de imagem não encontrado.

**Solução:**
1. Verifique se existe: `imagem/igrejadechomai.jpg`
2. Se não existir, o sistema mostra texto "MINISTÉRIO DECHONAI"
3. Adicione sua logo neste caminho

---

## ⚙️ Configurações Avançadas

### Alterar Porta do Servidor

```bash
streamlit run app.py --server.port=8000
```

### Permitir Acesso Externo (Rede Local)

```bash
streamlit run app.py --server.address=0.0.0.0
```

Acesse de outro dispositivo na mesma rede:
```
http://IP_DO_SERVIDOR:8501
```

Para descobrir seu IP:
```bash
# Windows
ipconfig

# Linux/Mac
ifconfig
```

### Executar em Background (Servidor)

**Linux/Mac:**
```bash
nohup streamlit run app.py &
```

**Windows (usando PowerShell):**
```powershell
Start-Process -NoNewWindow streamlit run app.py
```

---

## 📊 Estrutura do Banco de Dados

O sistema cria automaticamente o arquivo `dizimos_ofertas.db` (SQLite) com a seguinte estrutura:

```sql
CREATE TABLE lancamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL,
    nome TEXT NOT NULL,
    valor REAL NOT NULL,
    tipo TEXT NOT NULL,
    categoria TEXT NOT NULL,
    usuario TEXT NOT NULL,
    email TEXT,
    codigo_area TEXT,
    celular TEXT,
    operadora TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Localização:** Raiz do projeto (`DizimosOfertas/dizimos_ofertas.db`)

---

## 🔄 Atualizar o Sistema

### Atualizar Dependências:

```bash
pip install --upgrade -r requirements.txt
```

### Atualizar apenas Streamlit:

```bash
pip install --upgrade streamlit
```

### Verificar Versões Instaladas:

```bash
pip list
```

---

## 📦 Deploy em Produção

### Opção 1: Streamlit Cloud (Gratuito)

1. Faça upload do projeto no GitHub
2. Acesse: https://streamlit.io/cloud
3. Conecte seu repositório
4. Deploy automático!

**Vantagens:**
- ✅ Gratuito
- ✅ HTTPS automático
- ✅ Sempre online
- ✅ Fácil atualização

### Opção 2: Servidor Próprio

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar com nohup (Linux)
nohup streamlit run app.py --server.port=8501 --server.address=0.0.0.0 &

# Configurar proxy reverso (Nginx)
# Habilitar HTTPS com Let's Encrypt
```

### Opção 3: Docker

Crie `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Execute:
```bash
docker build -t dizimos-ofertas .
docker run -p 8501:8501 dizimos-ofertas
```

---

## 📝 Checklist de Primeira Execução

- [ ] Python 3.8+ instalado
- [ ] Navegou até a pasta do projeto
- [ ] Executou `pip install -r requirements.txt`
- [ ] Executou `streamlit run app.py`
- [ ] Acessou http://localhost:8501
- [ ] Fez login com `admin` / `Admin@#`
- [ ] Testou registrar uma contribuição
- [ ] (Opcional) Configurou WhatsApp

---

## 🆘 Precisa de Ajuda?

### Documentação do Projeto:
- **README.md** - Visão geral do sistema
- **WHATSAPP_SETUP.md** - Configurar WhatsApp
- **RESUMO_MODIFICACOES.md** - Detalhes técnicos

### Documentação Streamlit:
- https://docs.streamlit.io

### Logs do Sistema:
Os logs aparecem no terminal onde você executou o comando.

---

## ✅ Pronto!

Seu sistema está rodando em: **http://localhost:8501**

**Próximos Passos:**
1. ✅ Faça login
2. ✅ Registre uma contribuição de teste
3. ✅ (Opcional) Configure WhatsApp
4. ✅ Altere senhas padrão para mais segurança
5. ✅ Adicione o logo da sua igreja em `imagem/`

---

**Desenvolvido para o Ministério Dechonai**  
*Sistema de Gestão de Dízimos e Ofertas*
