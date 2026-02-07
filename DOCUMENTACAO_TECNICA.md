# Documentação Técnica - Sistema de Notificações

## 📚 Visão Geral

Este documento detalha a implementação técnica do sistema de notificações por Email e SMS adicionado ao Sistema de Gestão de Dízimos e Ofertas.

## 🔧 Arquitetura da Solução

### 1. Estrutura de Arquivos Modificados/Criados

```
DizimosOfertas/
├── config.py                    # ✏️ MODIFICADO - Adicionadas configurações
├── database.py                  # ✏️ MODIFICADO - Novos campos na tabela
├── notifications.py             # ✨ NOVO - Sistema de notificações
├── modules/
│   ├── registrar.py            # ✏️ MODIFICADO - Formulário expandido
│   ├── visualizar.py           # ✏️ MODIFICADO - Exibir novos campos
│   └── editar.py               # ✏️ MODIFICADO - Editar contatos
├── utils.py                    # ✏️ MODIFICADO - Ajustes em calcular_totais
└── requirements.txt            # ✏️ MODIFICADO - Novas dependências
```

---

## 📋 Detalhamento por Módulo

### 1. config.py - Configurações

#### Adições Realizadas:

```python
# OPERADORAS DE CELULAR
OPERADORAS = [
    "Vivo", "Claro", "TIM", "Oi", "Algar", "Nextel", "Sercomtel", "Outra"
]
```
**Propósito**: Lista de operadoras brasileiras para seleção no formulário.

```python
# CONFIGURAÇÕES DE EMAIL (SMTP)
SMTP_SERVER = "smtp.gmail.com"      # Servidor SMTP
SMTP_PORT = 587                     # Porta TLS
EMAIL_REMETENTE = "seu-email@gmail.com"
EMAIL_SENHA = "sua-senha-app"
```
**Propósito**: Credenciais para envio de emails via SMTP (Gmail exemplo).

**Segurança**: 
- ⚠️ Em produção, usar variáveis de ambiente
- ✅ Para Gmail, usar "Senha de App" (não senha normal)

```python
# CONFIGURAÇÕES DE SMS (TWILIO)
TWILIO_ACCOUNT_SID = "seu_account_sid"
TWILIO_AUTH_TOKEN = "seu_auth_token"
TWILIO_PHONE_NUMBER = "+5511999999999"
```
**Propósito**: Credenciais da API Twilio para envio de SMS.

**Como Obter**:
1. Criar conta em www.twilio.com
2. Obter Account SID e Auth Token no dashboard
3. Comprar/configurar número de telefone Twilio

```python
# HABILITAR/DESABILITAR NOTIFICAÇÕES
NOTIFICACOES_HABILITADAS = True
ENVIAR_EMAIL_AUTO = True
ENVIAR_SMS_AUTO = True
```
**Propósito**: Flags globais para controlar sistema de notificações.

---

### 2. database.py - Banco de Dados

#### Schema Atualizado:

```python
CREATE TABLE IF NOT EXISTS lancamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL,
    nome TEXT NOT NULL,
    valor REAL NOT NULL,
    tipo TEXT NOT NULL,
    categoria TEXT NOT NULL,
    usuario TEXT NOT NULL,
    email TEXT,              # ✨ NOVO
    codigo_area TEXT,        # ✨ NOVO
    celular TEXT,            # ✨ NOVO
    operadora TEXT,          # ✨ NOVO
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

**Novos Campos**:
- `email`: Email do contribuinte (opcional)
- `codigo_area`: DDD do celular (2 dígitos)
- `celular`: Número do celular (8-9 dígitos)
- `operadora`: Nome da operadora

**Tipo de Dados**: TEXT permite NULL para campos opcionais.

#### Função `adicionar_lancamento()`:

```python
def adicionar_lancamento(
    data: str, 
    nome: str, 
    valor: float, 
    tipo: str, 
    categoria: str, 
    usuario: str, 
    email: str = None,           # ✨ NOVO parâmetro opcional
    codigo_area: str = None,     # ✨ NOVO parâmetro opcional
    celular: str = None,         # ✨ NOVO parâmetro opcional
    operadora: str = None        # ✨ NOVO parâmetro opcional
) -> bool:
```

**Mudanças**:
- Adicionados 4 novos parâmetros opcionais
- Valores padrão `None` permitem chamadas sem contatos
- SQL INSERT atualizado com novos campos

**Compatibilidade**: Função mantém retrocompatibilidade - pode ser chamada sem novos parâmetros.

#### Função `obter_lancamentos()`:

```python
# Para usuários não-admin:
SELECT id, data, nome, valor, tipo, categoria, 
       email, codigo_area, celular, operadora
FROM lancamentos 
WHERE usuario = ?

# Para admin:
SELECT id, data, nome, valor, tipo, categoria, usuario,
       email, codigo_area, celular, operadora
FROM lancamentos
```

**Mudanças**:
- SELECTs agora incluem novos campos de contato
- Ordem de campos ajustada para incluir informações de contato

---

### 3. notifications.py - Sistema de Notificações (NOVO)

Módulo completamente novo dedicado a notificações.

#### 3.1 Funções de Validação

##### `validar_email(email: str) -> bool`

```python
def validar_email(email: str) -> bool:
    """Valida formato básico de email"""
    if not email or '@' not in email or '.' not in email:
        return False
    return True
```

**Lógica**:
1. Verifica se email não é vazio
2. Verifica presença de `@`
3. Verifica presença de `.`

**Limitações**: Validação básica. Para produção, usar regex ou biblioteca especializada.

**Melhorias Futuras**:
```python
import re
email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
return re.match(email_regex, email) is not None
```

##### `validar_celular(codigo_area: str, celular: str) -> bool`

```python
def validar_celular(codigo_area: str, celular: str) -> bool:
    """Valida DDD e número de celular brasileiro"""
    if not codigo_area or not celular:
        return False
    
    # Remove não-numéricos
    codigo_area = ''.join(filter(str.isdigit, codigo_area))
    celular = ''.join(filter(str.isdigit, celular))
    
    # Valida tamanho
    if len(codigo_area) != 2:
        return False
    
    if len(celular) not in [8, 9]:  # 8 = fixo, 9 = celular
        return False
    
    return True
```

**Validações**:
- DDD: exatamente 2 dígitos
- Celular: 8 ou 9 dígitos (aceita fixos e móveis)
- Remove automaticamente caracteres não numéricos

**Exemplos Válidos**:
- `codigo_area="11"`, `celular="999999999"` ✅
- `codigo_area="21"`, `celular="88888888"` ✅
- `codigo_area="(11)"`, `celular="9-9999-9999"` ✅ (remove formatação)

**Exemplos Inválidos**:
- `codigo_area="1"` ❌ (1 dígito)
- `celular="9999"` ❌ (muito curto)

##### `formatar_telefone(codigo_area: str, celular: str) -> str`

```python
def formatar_telefone(codigo_area: str, celular: str) -> str:
    """Formata para padrão internacional +55DDNNNNNNNNN"""
    codigo_area = ''.join(filter(str.isdigit, codigo_area))
    celular = ''.join(filter(str.isdigit, celular))
    return f"+55{codigo_area}{celular}"
```

**Saída**: `+5511999999999` (formato E.164)

**Uso**: Obrigatório para envio de SMS via Twilio.

---

#### 3.2 Funções de Envio

##### `enviar_email()` - Email HTML

```python
def enviar_email(
    destinatario: str, 
    nome: str, 
    valor: float, 
    categoria: str, 
    data: str
) -> Dict[str, any]:
```

**Fluxo de Execução**:

1. **Verificação de Configuração**
```python
if not NOTIFICACOES_HABILITADAS or not ENVIAR_EMAIL_AUTO:
    return {"sucesso": False, "mensagem": "Envio desabilitado"}
```

2. **Validação de Email**
```python
if not validar_email(destinatario):
    return {"sucesso": False, "mensagem": "Email inválido"}
```

3. **Criação da Mensagem MIME**
```python
mensagem = MIMEMultipart()
mensagem['From'] = EMAIL_REMETENTE
mensagem['To'] = destinatario
mensagem['Subject'] = f"Confirmação de {categoria}"
```

4. **Template HTML**
```html
<html>
  <body style="font-family: Arial; padding: 20px;">
    <div style="max-width: 600px; border: 1px solid #ddd;">
      <h2>🙏 Ministério Dechonai</h2>
      <p>Olá, <strong>{nome}</strong>!</p>
      <p>Agradecemos sua contribuição!</p>
      
      <div style="background: #f8f9fa; padding: 15px;">
        <h3>Detalhes da Contribuição</h3>
        <p><strong>Tipo:</strong> {categoria}</p>
        <p><strong>Valor:</strong> R$ {valor:.2f}</p>
        <p><strong>Data:</strong> {data}</p>
      </div>
      
      <p>"Deus ama quem dá com alegria" - 2 Cor 9:7</p>
    </div>
  </body>
</html>
```

**Características do Template**:
- ✅ Design responsivo
- ✅ Inline CSS (compatível com clientes de email)
- ✅ Informações destacadas
- ✅ Versículo bíblico
- ✅ Profissional e clean

5. **Envio SMTP** (Produção)
```python
# DESCOMENTAR EM PRODUÇÃO:
servidor = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
servidor.starttls()  # Criptografia TLS
servidor.login(EMAIL_REMETENTE, EMAIL_SENHA)
servidor.send_message(mensagem)
servidor.quit()
```

6. **Modo Simulação** (Desenvolvimento)
```python
# COMENTAR EM PRODUÇÃO:
print(f"[SIMULAÇÃO] Email enviado para {destinatario}")
```

**Retorno**:
```python
{
    "sucesso": True,
    "mensagem": "Email enviado com sucesso para joao@email.com"
}
```

---

##### `enviar_sms()` - SMS via Twilio

```python
def enviar_sms(
    codigo_area: str,
    celular: str,
    nome: str,
    valor: float,
    categoria: str
) -> Dict[str, any]:
```

**Fluxo de Execução**:

1. **Verificação e Validação**
```python
if not NOTIFICACOES_HABILITADAS or not ENVIAR_SMS_AUTO:
    return {"sucesso": False, ...}

if not validar_celular(codigo_area, celular):
    return {"sucesso": False, "mensagem": "Celular inválido"}
```

2. **Formatação do Número**
```python
numero_completo = formatar_telefone(codigo_area, celular)
# Resultado: +5511999999999
```

3. **Criação da Mensagem** (Otimizada para 160 caracteres)
```python
mensagem_sms = (
    f"Olá {nome}! Agradecemos sua contribuição de R$ {valor:.2f} "
    f"({categoria}). Que Deus abençoe! - Ministério Dechonai"
)
```

**Exemplo de Saída**:
```
Olá João Silva! Agradecemos sua contribuição de R$ 100.00 
(Dízimo). Que Deus abençoe! - Ministério Dechonai
```

**Comprimento**: ~120 caracteres (dentro do limite de 1 SMS)

4. **Envio via Twilio** (Produção)
```python
# DESCOMENTAR EM PRODUÇÃO:
from twilio.rest import Client

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
message = client.messages.create(
    body=mensagem_sms,
    from_=TWILIO_PHONE_NUMBER,  # Número Twilio
    to=numero_completo           # Número destino (+5511...)
)
```

5. **Modo Simulação**
```python
print(f"[SIMULAÇÃO] SMS enviado para {numero_completo}")
print(f"[SIMULAÇÃO] Mensagem: {mensagem_sms}")
```

**Custos**: Twilio cobra por SMS enviado (~$0.01-0.05 USD por mensagem).

---

##### `enviar_notificacoes()` - Orquestrador

```python
def enviar_notificacoes(
    nome: str,
    valor: float,
    categoria: str,
    data: str,
    email: Optional[str] = None,
    codigo_area: Optional[str] = None,
    celular: Optional[str] = None
) -> Dict[str, any]:
```

**Função**: Gerencia envio de email E SMS de uma vez.

**Lógica**:

```python
resultados = {
    "email": None,
    "sms": None,
    "algum_sucesso": False
}

# Tenta email se fornecido
if email:
    resultados["email"] = enviar_email(...)
    if resultados["email"]["sucesso"]:
        resultados["algum_sucesso"] = True

# Tenta SMS se fornecido
if codigo_area and celular:
    resultados["sms"] = enviar_sms(...)
    if resultados["sms"]["sucesso"]:
        resultados["algum_sucesso"] = True

return resultados
```

**Retorno Exemplo**:
```python
{
    "email": {
        "sucesso": True,
        "mensagem": "Email enviado com sucesso"
    },
    "sms": {
        "sucesso": True,
        "mensagem": "SMS enviado com sucesso"
    },
    "algum_sucesso": True
}
```

**Vantagens**:
- ✅ Tenta ambos métodos independentemente
- ✅ Falha em um não bloqueia o outro
- ✅ Retorna status detalhado de cada

---

### 4. modules/registrar.py - Formulário de Registro

#### Interface do Usuário

**Seções do Formulário**:

1. **Dados do Lançamento** (Obrigatório)
```python
st.markdown("#### 📋 Dados do Lançamento")
data = st.date_input("Data", value=datetime.today())
nome = st.text_input("Nome Completo", max_chars=100)
valor = st.number_input("Valor (R$)", min_value=0.01, ...)
tipo = st.selectbox("Tipo de Pagamento", TIPOS_PAGAMENTO)
categoria = st.selectbox("Categoria", CATEGORIAS)
```

2. **Dados de Contato** (Opcional)
```python
st.markdown("#### 📞 Dados de Contato (Opcional)")
email = st.text_input("Email", placeholder="exemplo@email.com")

col1, col2, col3 = st.columns([1, 2, 2])
with col1:
    codigo_area = st.text_input("DDD", max_chars=2)
with col2:
    celular = st.text_input("Celular", max_chars=10)
with col3:
    operadora = st.selectbox("Operadora", OPERADORAS)
```

**Layout em Colunas**:
- DDD: 1/5 da largura (pequeno)
- Celular: 2/5 da largura (médio)
- Operadora: 2/5 da largura (médio)

3. **Opções de Notificação**
```python
st.markdown("#### 📧 Notificações")

col1, col2 = st.columns(2)
with col1:
    enviar_email_check = st.checkbox(
        "Enviar confirmação por Email",
        value=True
    )
with col2:
    enviar_sms_check = st.checkbox(
        "Enviar confirmação por SMS",
        value=True
    )
```

**Padrão**: Ambos marcados (True)

#### Processamento do Formulário

**Fluxo ao Submeter**:

1. **Validações Básicas**
```python
if not validar_nome(nome):
    st.error("❌ Nome deve ter pelo menos 2 caracteres")
    return

if not validar_valor(valor):
    st.error("❌ Valor deve ser maior que zero")
    return
```

2. **Validação de Email** (se fornecido)
```python
email_valido = None
if email.strip():
    if validar_email(email.strip()):
        email_valido = email.strip()
    else:
        st.warning("⚠️ Email inválido. Lançamento registrado sem email")
```

**Comportamento**: 
- Email inválido = warning (não bloqueia)
- Lançamento continua sem email

3. **Validação de Celular** (se fornecido)
```python
celular_valido = None
codigo_area_valido = None

if codigo_area.strip() and celular.strip():
    if validar_celular(codigo_area.strip(), celular.strip()):
        codigo_area_valido = codigo_area.strip()
        celular_valido = celular.strip()
        operadora_valida = operadora
    else:
        st.warning("⚠️ Celular inválido. Lançamento registrado sem celular")
```

4. **Salvar no Banco**
```python
sucesso = adicionar_lancamento(
    data.strftime("%Y-%m-%d"),
    nome.strip(),
    float(valor),
    tipo,
    categoria,
    st.session_state["usuario"],
    email=email_valido,
    codigo_area=codigo_area_valido,
    celular=celular_valido,
    operadora=operadora_valida
)
```

5. **Enviar Notificações**
```python
if sucesso:
    st.success("✅ Lançamento registrado com sucesso!")
    
    # Verificar se deve enviar notificações
    if (enviar_email_check and email_valido) or 
       (enviar_sms_check and celular_valido):
        
        with st.spinner("Enviando notificações..."):
            resultados = enviar_notificacoes(
                nome=nome.strip(),
                valor=float(valor),
                categoria=categoria,
                data=formatar_data(data.strftime("%Y-%m-%d")),
                email=email_valido if enviar_email_check else None,
                codigo_area=codigo_area_valido if enviar_sms_check else None,
                celular=celular_valido if enviar_sms_check else None
            )
```

**Spinner**: Mostra "Enviando notificações..." durante envio.

6. **Feedback Visual**
```python
# Email
if resultados.get("email"):
    if resultados["email"]["sucesso"]:
        st.success(f"📧 {resultados['email']['mensagem']}")
    else:
        st.warning(f"⚠️ Email: {resultados['email']['mensagem']}")

# SMS
if resultados.get("sms"):
    if resultados["sms"]["sucesso"]:
        st.success(f"📱 {resultados['sms']['mensagem']}")
    else:
        st.warning(f"⚠️ SMS: {resultados['sms']['mensagem']}")

# Resumo
if notificacoes_enviadas:
    st.info(f"✉️ Notificações enviadas: {', '.join(notificacoes_enviadas)}")

# Celebração!
st.balloons()
st.rerun()
```

**Elementos Visuais**:
- ✅ `st.success()`: Verde para sucessos
- ⚠️ `st.warning()`: Amarelo para avisos
- ℹ️ `st.info()`: Azul para informações
- 🎈 `st.balloons()`: Animação de comemoração

---

### 5. modules/visualizar.py - Visualização

**Mudanças na Tabela**:

```python
# Antes: 6 colunas
columns = ["ID", "Data", "Nome", "Valor (R$)", "Tipo", "Categoria"]

# Depois: 8-9 colunas
columns = ["ID", "Data", "Nome", "Valor (R$)", "Tipo", "Categoria", 
           "Email", "Celular"]
# Admin: + "Usuário"
```

**Formatação de Celular**:
```python
codigo_area = lanc[7]
celular = lanc[8]

if codigo_area and celular:
    celular_formatado = f"({codigo_area}) {celular}"
else:
    celular_formatado = "-"
```

**Saída**: `(11) 999999999` ou `-` se vazio

---

### 6. modules/editar.py - Edição

**Formulário Expandido**:

```python
# Dados básicos (sempre presentes)
data, nome, valor, tipo, categoria

# Dados de contato (novos)
email = st.text_input("Email", value=email_atual or "")

codigo_area = st.text_input("DDD", value=codigo_area_atual or "")
celular = st.text_input("Celular", value=celular_atual or "")
operadora = st.selectbox("Operadora", OPERADORAS, index=index_operadora)
```

**Pre-preenchimento**: 
- Busca valores atuais do banco
- Exibe em campos editáveis
- Aceita valores vazios (limpar)

**Atualização**:
```python
sucesso = atualizar_lancamento(
    id_selecionado,
    data.strftime("%Y-%m-%d"),
    nome.strip(),
    float(valor),
    tipo,
    categoria,
    email=email_valido,
    codigo_area=codigo_area_valido,
    celular=celular_valido,
    operadora=operadora_valida
)
```

---

## 🔄 Fluxo Completo de Uso

### Cenário: Registro com Notificações

**1. Usuário Acessa Sistema**
```
Login → admin/Admin@# → Menu: Registrar
```

**2. Preenche Formulário**
```
Data: 07/02/2026
Nome: João Silva
Valor: R$ 100,00
Tipo: Pix
Categoria: Dízimo
Email: joao@email.com
DDD: 11
Celular: 999999999
Operadora: Vivo
[x] Enviar Email
[x] Enviar SMS
```

**3. Clica "Registrar"**

**4. Sistema Valida**
```python
✅ Nome válido (11 caracteres)
✅ Valor válido (100.00 > 0)
✅ Email válido (contém @ e .)
✅ Celular válido (DDD 2 dígitos, cel 9 dígitos)
```

**5. Sistema Salva no Banco**
```sql
INSERT INTO lancamentos (
    data, nome, valor, tipo, categoria, usuario,
    email, codigo_area, celular, operadora
) VALUES (
    '2026-02-07', 'João Silva', 100.00, 'Pix', 'Dízimo', 'admin',
    'joao@email.com', '11', '999999999', 'Vivo'
)
```

**6. Sistema Envia Notificações**

**Email:**
```
De: seu-email@gmail.com
Para: joao@email.com
Assunto: Confirmação de Dízimo - Ministério Dechonai

[HTML Template com dados]
```

**SMS:**
```
De: +5511999999999 (Twilio)
Para: +5511999999999 (João)
Texto: "Olá João Silva! Agradecemos sua contribuição de R$ 100.00 
(Dízimo). Que Deus abençoe! - Ministério Dechonai"
```

**7. Feedback ao Usuário**
```
✅ Lançamento registrado com sucesso!
📧 Email enviado com sucesso para joao@email.com
📱 SMS enviado com sucesso para +5511999999999
ℹ️ Notificações enviadas: Email, SMS
🎈 [Balloons animation]
```

**8. Recarrega Página**
```
st.rerun() → Formulário limpo e pronto para novo registro
```

---

## 🧪 Testes e Validações

### Testes Unitários Recomendados

```python
# test_notifications.py

def test_validar_email():
    assert validar_email("user@domain.com") == True
    assert validar_email("invalido") == False
    assert validar_email("sem@ponto") == False

def test_validar_celular():
    assert validar_celular("11", "999999999") == True
    assert validar_celular("1", "999999999") == False
    assert validar_celular("11", "999") == False

def test_formatar_telefone():
    assert formatar_telefone("11", "999999999") == "+5511999999999"
    assert formatar_telefone("(21)", "8-8888-8888") == "+552188888888"
```

### Testes de Integração

```python
def test_adicionar_lancamento_com_contato():
    sucesso = adicionar_lancamento(
        data="2026-02-07",
        nome="Teste",
        valor=50.00,
        tipo="Dinheiro",
        categoria="Oferta",
        usuario="admin",
        email="test@test.com",
        codigo_area="11",
        celular="999999999",
        operadora="Vivo"
    )
    assert sucesso == True
    
    # Verificar se salvou
    lanc = obter_lancamento_por_id(1)
    assert lanc[7] == "test@test.com"
    assert lanc[8] == "11"
```

---

## 📊 Métricas e Monitoramento

### Logs Recomendados

```python
import logging

logging.info(f"Email enviado: {destinatario} - Categoria: {categoria}")
logging.warning(f"Falha ao enviar SMS: {erro}")
logging.error(f"Erro crítico no envio: {exception}")
```

### Estatísticas

```python
# Quantas notificações foram enviadas hoje?
SELECT COUNT(*) FROM lancamentos 
WHERE email IS NOT NULL 
AND data = CURRENT_DATE;

# Taxa de cadastros com contato
SELECT 
    COUNT(*) as total,
    SUM(CASE WHEN email IS NOT NULL THEN 1 ELSE 0 END) as com_email,
    SUM(CASE WHEN celular IS NOT NULL THEN 1 ELSE 0 END) as com_celular
FROM lancamentos;
```

---

## 🚀 Deploy em Produção

### Checklist Pré-Deploy

- [ ] Configurar variáveis de ambiente
- [ ] Descomentar código de envio real
- [ ] Testar SMTP com credenciais reais
- [ ] Verificar saldo Twilio
- [ ] Implementar rate limiting
- [ ] Configurar logs
- [ ] Backup do banco de dados
- [ ] Testar em staging
- [ ] Documentar credenciais (seguro)

### Variáveis de Ambiente (Exemplo)

```.env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587  
EMAIL_REMETENTE=sistema@igreja.com
EMAIL_SENHA=abc123apppassword

TWILIO_ACCOUNT_SID=ACxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxx
TWILIO_PHONE_NUMBER=+5511999999999
```

**Carregar em Python**:
```python
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_REMETENTE = os.getenv('EMAIL_REMETENTE')
EMAIL_SENHA = os.getenv('EMAIL_SENHA')
```

---

## 📝 Conclusão

O sistema de notificações foi implementado de forma:

✅ **Modular**: Código isolado em `notifications.py`  
✅ **Opcional**: Funciona com ou sem dados de contato  
✅ **Configurável**: Flags para ativar/desativar  
✅ **Seguro**: Validações de entrada  
✅ **Testável**: Modo simulação para desenvolvimento  
✅ **Escalável**: Fácil adicionar novos canais (WhatsApp, Push, etc)  
✅ **Documentado**: Comentários e docstrings em todo código  

**Próximos Passos Sugeridos**:
1. Implementar testes automatizados
2. Adicionar queue para envios assíncronos
3. Dashboard de métricas de notificações
4. Templates personalizáveis
5. Integração com WhatsApp Business

---

**Desenvolvido com ❤️ para o Ministério Dechonai**