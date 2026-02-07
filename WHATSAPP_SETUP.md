# 📱 Guia Completo de Configuração do WhatsApp

Este guia explica passo a passo como configurar o envio de mensagens WhatsApp no Sistema de Dízimos e Ofertas.

## 📑 Índice

1. [O que você precisa](#o-que-você-precisa)
2. [Criando conta Twilio](#criando-conta-twilio)
3. [Configurando WhatsApp Sandbox](#configurando-whatsapp-sandbox)
4. [Obtendo credenciais](#obtendo-credenciais)
5. [Configurando o sistema](#configurando-o-sistema)
6. [Testando o envio](#testando-o-envio)
7. [Resolvendo problemas](#resolvendo-problemas)
8. [Upgrade para produção](#upgrade-para-produção)

---

## O que você precisa

- ✅ Conta Twilio (gratuita para testes)
- ✅ Número de WhatsApp pessoal para testar
- ✅ 10-15 minutos para configuração inicial

**Sem custos iniciais** - Twilio oferece créditos gratuitos!

---

## Criando conta Twilio

### Passo 1: Acessar Twilio

1. Abra seu navegador
2. Acesse: https://www.twilio.com/try-twilio
3. Clique em **"Sign up"** ou **"Start for free"**

### Passo 2: Preencher cadastro

Preencha os dados:
- **First Name**: Seu primeiro nome
- **Last Name**: Seu sobrenome
- **Email**: Seu email (será usado para login)
- **Password**: Senha forte (mínimo 12 caracteres)

### Passo 3: Verificar conta

1. Você receberá um email de confirmação
2. Clique no link do email
3. Informe seu número de telefone
4. Receba e digite o código de verificação por SMS

### Passo 4: Configurar conta

Pergunta: "Which Twilio product are you here to use?"
- Selecione: **Messaging**

Pergunta: "What do you plan to build?"
- Selecione: **Alerts & Notifications**

Pergunta: "How do you want to build with Twilio?"
- Selecione: **With code**

Pergunta: "What is your preferred coding language?"
- Selecione: **Python**

**Parabéns!** Você ganhou **$15 USD em créditos gratuitos** 🎉

---

## Configurando WhatsApp Sandbox

O Sandbox permite testar WhatsApp gratuitamente SEM precisar de número comercial aprovado.

### Passo 1: Acessar WhatsApp Sandbox

No Console Twilio:
1. Menu lateral → **Messaging**
2. Clique em **"Try it out"**
3. Selecione **"Send a WhatsApp message"**

### Passo 2: Conectar seu WhatsApp

Você verá uma tela com:

```
Send this message from WhatsApp to:
+1 415 523 8886

join happy-cat
```

**Importante:** O código (`happy-cat`) é ÚNICO para sua conta.

### Passo 3: Enviar mensagem de ativação

1. Abra o **WhatsApp** no seu celular
2. Adicione o número `+1 415 523 8886` nos contatos (opcional)
3. Envie uma mensagem para esse número com o texto exato:
   ```
   join happy-cat
   ```
   (Use o código que apareceu na sua tela!)

### Passo 4: Confirmar ativação

Você receberá uma resposta do Twilio:

```
✅ Sandbox: Welcome to Twilio!
Your sandbox is now active.
```

**Pronto!** Seu WhatsApp está conectado ao Sandbox.

---

## Obtendo credenciais

Agora você precisa copiar 3 informações importantes:

### 1. Account SID

No Console Twilio (https://console.twilio.com):

1. Vá para **Dashboard** (página inicial)
2. Procure por **"Account Info"**
3. Copie o **Account SID**
   - Formato: `AC1234567890abcdef...` (32 caracteres)

### 2. Auth Token

Na mesma seção:

1. Procure por **"Auth Token"**
2. Clique em **"Show"** para revelar
3. Copie o **Auth Token**
   - Formato: sequência alfanumérica de 32 caracteres

⚠️ **IMPORTANTE**: Mantenha seu Auth Token em segredo!

### 3. WhatsApp Number

1. Volte para **Messaging** → **Try it Out** → **Send a WhatsApp message**
2. O número aparece no topo: geralmente `+1 415 523 8886`
3. Anote esse número

---

## Configurando o sistema

### Método 1: Arquivo .env (RECOMENDADO)

Este método é mais seguro pois as credenciais ficam fora do código.

#### Passo 1: Criar arquivo .env

Na pasta do projeto `DizimosOfertas`:

1. Copie o arquivo `.env.example`
2. Renomeie a cópia para `.env`
3. Abra o arquivo `.env` no editor de texto

#### Passo 2: Preencher credenciais

Edite o arquivo `.env`:

```env
# Habilitar WhatsApp
WHATSAPP_ENABLED=true

# Suas credenciais Twilio
TWILIO_ACCOUNT_SID=AC1234567890abcdef_COLE_SEU_SID_AQUI
TWILIO_AUTH_TOKEN=seu_auth_token_cole_aqui_32_caracteres
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

**Exemplo preenchido:**
```env
WHATSAPP_ENABLED=true
TWILIO_ACCOUNT_SID=AC12345678901234567890123456789012
TWILIO_AUTH_TOKEN=abcdef1234567890abcdef1234567890
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

#### Passo 3: Salvar arquivo

Salve o arquivo `.env` e feche.

---

### Método 2: Direto no config.py (Alternativo)

Se preferir, pode configurar direto no código:

1. Abra o arquivo `config.py`
2. Procure pela seção "CONFIGURAÇÕES DO WHATSAPP"
3. Substitua os valores:

```python
WHATSAPP_ENABLED = True
TWILIO_ACCOUNT_SID = 'AC12345678901234567890123456789012'
TWILIO_AUTH_TOKEN = 'abcdef1234567890abcdef1234567890'
TWILIO_WHATSAPP_NUMBER = 'whatsapp:+14155238886'
```

---

## Testando o envio

### Passo 1: Instalar dependências

Abra o terminal na pasta do projeto:

```bash
pip install -r requirements.txt
```

Isso instalará o pacote `twilio` necessário.

### Passo 2: Iniciar sistema

```bash
streamlit run app.py
```

### Passo 3: Fazer login

- Usuário: `admin`
- Senha: `Admin@#`

### Passo 4: Registrar contribuição

1. Clique em **"Registrar"** no menu
2. Preencha:
   - **Nome**: João da Silva
   - **Valor**: 100.00
   - **Categoria**: Dízimo
   - **Celular**: Seu número com DDD (ex: 11987654321)
3. Marque: ☑️ **Enviar confirmação via WhatsApp**
4. Clique em **"Registrar Lançamento"**

### Passo 5: Verificar WhatsApp

Em poucos segundos você receberá:

```
🙏 *Ministério Dechonai*

Olá João da Silva!

✅ Sua contribuição foi registrada com sucesso:

📋 *Detalhes:*
• Categoria: Dízimo
• Valor: R$ 100,00
• Data: 07/02/2026

Que Deus abençoe abundantemente sua vida!

_Esta é uma mensagem automática de confirmação._
```

**✅ Sucesso!** WhatsApp configurado corretamente!

---

## Resolvendo problemas

### 🔴 "Serviço WhatsApp não habilitado"

**Causa:** WhatsApp não está ativado

**Solução:**
1. Verifique arquivo `.env`: `WHATSAPP_ENABLED=true`
2. Reinicie o servidor Streamlit
3. Tente novamente

---

### 🔴 "Twilio authentication failed"

**Causa:** Credenciais incorretas

**Solução:**
1. Acesse https://console.twilio.com
2. Copie novamente Account SID e Auth Token
3. Cole no arquivo `.env` (sem espaços extras)
4. Reinicie o servidor

**Checklist:**
- ✅ Account SID tem 34 caracteres começando com AC
- ✅ Auth Token tem 32 caracteres
- ✅ Não há espaços no início ou fim dos valores
- ✅ Valores estão entre aspas se no config.py

---

### 🔴 "Error code 63016 - Unable to send message"

**Mensagem completa:**
```
The destination number has not joined your sandbox
```

**Causa:** Número não conectado ao Sandbox

**Solução:**
1. No WhatsApp do número que vai receber, envie:
   ```
   join happy-cat
   ```
   Para: `+1 415 523 8886`

2. Aguarde confirmação de ativação
3. Tente enviar novamente

**Nota:** Na conta gratuita (Sandbox), APENAS números que enviaram `join` podem receber mensagens.

---

### 🔴 "Invalid phone number format"

**Causa:** Número em formato incorreto

**Solução:**
Certifique-se que o número:
- ✅ Tem 11 dígitos (DDD + 9 dígitos)
- ✅ Terceiro dígito é 9 (celular)
- ✅ Exemplo correto: `11987654321` ou `(11) 98765-4321`

---

### 🔴 "Insufficient funds"

**Causa:** Créditos esgotados

**Solução:**
1. Acesse Console Twilio → Billing
2. Adicione créditos (mínimo $20 USD)
3. Ou aguarde renovação mensal dos créditos trial

---

## Upgrade para produção

### Limitações do Sandbox

❌ Apenas números verificados podem receber
❌ Mensagem deve ter prefixo (no envio manual)
❌ Não pode ter número próprio

### WhatsApp Business API (Produção)

✅ Enviar para qualquer número
✅ Número próprio da igreja
✅ Sem limite de destinatários
✅ Templates aprovados pelo WhatsApp

### Como fazer upgrade

#### 1. Ativar WhatsApp Business

Console Twilio:
1. **Messaging** → **WhatsApp**
2. **Get Started** → **Request Access**
3. Preencher formulário de negócio
4. Aguardar aprovação do Facebook/Meta

**Tempo:** 1-2 semanas

#### 2. Comprar número dedicado

1. Console Twilio → **Phone Numbers** → **Buy a number**
2. Filtrar por país: **Brazil (+55)**
3. Selecionar número com capacidade SMS/WhatsApp
4. Confirmar compra (~$10-15 USD/mês)

#### 3. Conectar número ao WhatsApp

1. Messaging → WhatsApp → **Senders**
2. Adicionar número comprado
3. Seguir etapas de verificação do Facebook

#### 4. Criar templates aprovados

WhatsApp Business exige templates pré-aprovados:

1. Console Twilio → **Messaging** → **Content Editor**
2. Criar template com variáveis:

```
Olá {{1}}!

Sua contribuição de {{2}} foi confirmada.

Categoria: {{3}}
Data: {{4}}

Que Deus abençoe!

_Ministério Dechonai_
```

3. Submeter para aprovação
4. Aguardar 24-48h

#### 5. Atualizar código

Modifique `whatsapp_service.py` para usar templates:

```python
message = client.messages.create(
    from_='whatsapp:+5511999999999',  # Seu número
    to=numero_formatado,
    content_sid='HXxxxxxxxxxxxxxxxxxxxx',  # ID do template
    content_variables={
        '1': nome,
        '2': f'R$ {valor:.2f}',
        '3': categoria,
        '4': data
    }
)
```

---

## Custos Estimados

### Conta Sandbox (Gratuita)
- **Custo**: $0
- **Crédito inicial**: $15 USD
- **Mensagens**: ~3.000 testes

### Conta Produção
- **Número dedicado**: ~$10-15 USD/mês
- **Por mensagem**: ~$0.012 USD (R$ 0,06)
- **100 mensagens/mês**: ~$1.20 USD (R$ 6,00)
- **1.000 mensagens/mês**: ~$12 USD (R$ 60,00)

**Muito acessível para igrejas!**

---

## Suporte

### Documentação Twilio
- Guias: https://www.twilio.com/docs/whatsapp
- API Reference: https://www.twilio.com/docs/sms/api

### Contato Twilio
- Support: support@twilio.com
- Chat: Disponível no console

### Dúvidas do Sistema
Consulte o README.md principal ou entre em contato com o desenvolvedor.

---

**✅ Configuração Concluída!**

Seu sistema agora está integrado com WhatsApp e pronto para enviar confirmações automáticas aos contribuintes!
