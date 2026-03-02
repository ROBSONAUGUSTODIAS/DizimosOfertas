# Sistema de Gestão de Dízimos e Ofertas

Sistema web desenvolvido em Python com Streamlit para gerenciamento de dízimos, ofertas e contribuições de uma igreja.

## � Documentação

- **[🔐 GUIA DE SEGURANÇA](GUIA_SEGURANCA.md)** - Guia completo de configuração e uso do sistema seguro
- **[📋 RESUMO DE SEGURANÇA](RESUMO_SEGURANCA.md)** - Resumo rápido das implementações de segurança
- **[🔧 IMPLEMENTAÇÃO TÉCNICA](SEGURANCA_IMPLEMENTACAO.md)** - Detalhes técnicos das mudanças
- **[📚 Documentação Técnica](DOCUMENTACAO_TECNICA.md)** - Documentação completa do sistema

## �📋 Funcionalidades

### Gestão de Lançamentos
- **Autenticação de Usuários**: Sistema de login com diferentes níveis de acesso
- **Registro de Lançamentos**: Cadastro completo de dízimos, ofertas e contribuições
- **Cadastro de Contatos**: Telefone/celular e Email opcionais
- **Visualização**: Consulta de lançamentos com histórico completo ou últimos 30 dias
- **Edição e Exclusão**: Gerenciamento completo de registros (apenas admin)
- **Relatórios**: Totais por dia, mês e categoria
- **Gráficos**: Visualização de distribuição de entradas

## 🔐 Segurança e Autenticação

### Sistema de Autenticação Seguro

A aplicação implementa um sistema robusto de autenticação adequado para publicação no Streamlit Cloud:

#### ✅ Recursos de Segurança Implementados

1. **Hash de Senhas com Bcrypt**
   - Senhas nunca são armazenadas em texto plano
   - Utiliza algoritmo bcrypt com salt automático
   - Proteção contra ataques de força bruta e rainbow tables

2. **Variáveis de Ambiente**
   - Credenciais sensíveis armazenadas em arquivo `.env`
   - Arquivo `.env` incluído no `.gitignore` (nunca enviado ao GitHub)
   - Suporta configuração via Streamlit Cloud Secrets

3. **Separação de Configuração**
   - Código-fonte não contém senhas ou credenciais
   - Exemplos fornecidos em `.env.example`
   - Cada instalação usa suas próprias credenciais

#### 🔑 Configuração Inicial de Senhas

**IMPORTANTE**: Antes de executar a aplicação pela primeira vez, você DEVE configurar senhas seguras!

**Passo 1: Instalar Dependências**
```bash
pip install -r requirements.txt
```

**Passo 2: Gerar Hashes de Senhas**
```bash
python generate_password_hash.py
```

O script irá solicitar:
- Nome de usuário
- Senha desejada

E gerará uma linha como:
```
USER_ADMIN_HASH=$2b$12$xK3hQmJ8L7kDYhZ4vFNDquU5yRZB8rOJ7Pv9nQ0hX4WwYqCvE8Kxy
```

**Passo 3: Configurar Arquivo .env**

1. Copie o arquivo de exemplo:
```bash
copy .env.example .env    # Windows
cp .env.example .env      # Linux/Mac
```

2. Edite o arquivo `.env` e substitua os hashes de exemplo pelos gerados:
```env
# Hashes gerados pelo script
USER_ADMIN_HASH=$2b$12$seu_hash_aqui_gerado_pelo_script
USER_DIACONO01_HASH=$2b$12$seu_hash_aqui_gerado_pelo_script
USER_DIACONO02_HASH=$2b$12$seu_hash_aqui_gerado_pelo_script
```

**Passo 4: Verificar .gitignore**

Confirme que o arquivo `.env` está no `.gitignore`:
```gitignore
.env
*.env
!.env.example
```

#### 🚀 Publicação no Streamlit Cloud

Para publicar a aplicação com segurança:

1. **NÃO envie o arquivo .env para o GitHub**
   - O arquivo `.gitignore` já protege contra isso
   - Apenas o `.env.example` deve estar no repositório

2. **Configure Secrets no Streamlit Cloud**:
   - Acesse seu app em share.streamlit.io
   - Vá em: **Settings → Secrets**
   - Cole o conteúdo do seu arquivo `.env`:
   
   ```toml
   USER_ADMIN_HASH = "$2b$12$seu_hash_aqui"
   USER_DIACONO01_HASH = "$2b$12$seu_hash_aqui"
   USER_DIACONO02_HASH = "$2b$12$seu_hash_aqui"
   ```

3. **Clique em "Save"** e reinicie a aplicação

#### 🔒 Boas Práticas de Senha

Ao criar senhas para os usuários, use:

✅ **Senha Forte:**
- Mínimo de 12 caracteres
- Letras maiúsculas e minúsculas
- Números
- Caracteres especiais (@, #, $, %, etc.)

✅ **Exemplos de Senhas Fortes:**
- `Admin@Seguro#2026`
- `Diacono$Forte!123`
- `Igreja#Segura@2026`

❌ **Evite:**
- Senhas simples como "123456" ou "senha"
- Informações pessoais (nome, data de nascimento)
- Palavras do dicionário
- Senhas iguais para diferentes usuários

#### 👥 Gerenciamento de Usuários

Os usuários são configurados em [config.py](config.py):

```python
USUARIOS_HASHES = {
    "admin": os.getenv('USER_ADMIN_HASH'),
    "diacono01": os.getenv('USER_DIACONO01_HASH'),
    "diacono02": os.getenv('USER_DIACONO02_HASH')
}

NIVEIS_ACESSO = {
    "admin": "admin",
    "diacono01": "admin",
    "diacono02": "admin"
}

NOMES_USUARIOS = {
    "admin": "Administrador",
    "diacono01": "Diácono01",
    "diacono02": "Diácono02"
}
```

**Para adicionar novos usuários:**

1. Adicione o usuário em `USUARIOS_HASHES`, `NIVEIS_ACESSO` e `NOMES_USUARIOS`
2. Gere o hash da senha usando `generate_password_hash.py`
3. Adicione o hash no arquivo `.env`:
   ```env
   USER_NOVOUSUARIO_HASH=$2b$12$hash_gerado
   ```

#### 🛡️ Níveis de Acesso

- **admin**: Acesso completo (visualizar, registrar, editar, excluir)
- **editor**: Pode visualizar e registrar novos lançamentos
- **visualizador**: Apenas visualiza lançamentos

## 📱 Responsividade Mobile

### Sistema Otimizado para Celular e Tablet

A aplicação foi **totalmente otimizada** para proporcionar uma excelente experiência em dispositivos móveis:

#### ✅ Recursos Mobile
- **Layout Responsivo**: Colunas que empilham verticalmente em telas pequenas
- **Botões Touch-Friendly**: Tamanho mínimo de 44px para fácil toque
- **Inputs Otimizados**: Font-size 16px+ previne zoom automático (iOS/Android)
- **Tabelas com Scroll**: Scroll horizontal suave para visualizar todas as colunas
- **Sidebar Colapsável**: Fechada por padrão em mobile para máximo espaço
- **CSS Customizado**: Mais de 200 linhas de CSS otimizado para mobile
- **Métricas Empilhadas**: Cards financeiros empilham verticalmente
- **Formulários Adaptivos**: Campos se reorganizam para telas pequenas

#### 📊 Breakpoint Mobile
```css
@media (max-width: 768px) {
  /* Todas as otimizações são aplicadas */
}
```

#### 🧪 Como Testar no Celular

**Opção 1: DevTools do Navegador (Rápido)**
1. Execute: `streamlit run app.py`
2. Abra F12 (DevTools)
3. Clique no ícone de celular 📱
4. Selecione: iPhone, Samsung ou iPad
5. Teste a navegação!

**Opção 2: Dispositivo Real**
1. Execute: `streamlit run app.py --server.address=0.0.0.0`
2. Descubra seu IP: `ipconfig` (Windows) ou `ifconfig` (Linux/Mac)
3. No celular: `http://SEU_IP:8501`

**📖 Guia Completo:** Veja [TESTAR_MOBILE.md](TESTAR_MOBILE.md)

#### 📋 Checklist Mobile Aprovado
- ✅ Login centralizado e responsivo
- ✅ Métricas financeiras empilhadas
- ✅ Tabelas com scroll horizontal
- ✅ Formulários otimizados para toque
- ✅ Botões grandes (44px+)
- ✅ Gráficos ocupam largura total
- ✅ Logo responsiva
- ✅ Sidebar colapsável
- ✅ Zero zoom automático em inputs

## 🏗️ Arquitetura

O projeto segue uma arquitetura modular com separação de responsabilidades:

```
DizimosOfertas/
├── app.py                  # Aplicação principal
├── config.py               # Configurações e constantes
├── database.py             # Gerenciamento do banco de dados
├── auth.py                 # Autenticação e autorização
├── utils.py                # Funções utilitárias
├── modules/                # Módulos da aplicação
│   ├── __init__.py
│   ├── visualizar.py       # Módulo de visualização
│   ├── registrar.py        # Módulo de registro
│   └── editar.py           # Módulo de edição
├── imagem/                 # Recursos de imagem
├── requirements.txt        # Dependências
├── .env.example            # Exemplo de configuração (NOVO)
└── README.md              # Este arquivo
```

## 📱 Integração WhatsApp - Guia Completo

### ⚠️ REGRA IMPORTANTE: WhatsApp apenas para PIX

**O sistema envia confirmação via WhatsApp SOMENTE quando o tipo de pagamento for PIX.**

**Por quê?**
- 🏦 **Rastreabilidade**: Pagamentos PIX são instantâneos e confirmados automaticamente
- ⚡ **Agilidade**: PIX cai na hora, permitindo confirmação imediata ao contribuinte
- ✅ **Automação**: Ideal para notificações automáticas em tempo real
- 📊 **Controle**: Facilita a gestão de contribuições digitais

**Outros tipos de pagamento** (Dinheiro, Cartão, Transferência, Cheque):
- ✅ São registrados normalmente no sistema
- ❌ NÃO recebem confirmação automática via WhatsApp
- ℹ️ Mensagem informativa é exibida ao contribuinte

### O que é necessário?

Para enviar mensagens via WhatsApp, o sistema utiliza a **Twilio API**, um serviço profissional e confiável para comunicação.

### Passo a Passo para Configuração

#### 1️⃣ Criar Conta Twilio (Gratuita)

1. Acesse: https://www.twilio.com/try-twilio
2. Clique em "Sign up" e preencha seus dados
3. Confirme seu email
4. Você receberá créditos gratuitos para testes (cerca de $15 USD)

#### 2️⃣ Configurar WhatsApp Sandbox

O WhatsApp Sandbox permite testar gratuitamente antes de configurar um número oficial:

1. No Console Twilio, vá para: **Messaging** → **Try it out** → **Send a WhatsApp message**
2. Você verá um código do tipo: `join <palavra-código>`
3. **No seu WhatsApp pessoal**, envie uma mensagem para o número Twilio mostrado com o código
4. Exemplo: Se aparecer `join happy-cat`, envie: `join happy-cat` para `+1 415 523 8886`
5. Você receberá uma confirmação no WhatsApp

#### 3️⃣ Obter Credenciais

No Console Twilio (https://console.twilio.com):

1. Copie o **Account SID** (começa com AC...)
2. Copie o **Auth Token** (clique em "Show" para visualizar)
3. Anote o **número WhatsApp Twilio**: geralmente `+1 415 523 8886`

#### 4️⃣ Configurar no Sistema

**Método 1: Arquivo .env (Recomendado)**

1. Copie o arquivo `.env.example` e renomeie para `.env`
2. Edite o arquivo `.env` e preencha:

```env
WHATSAPP_ENABLED=true
TWILIO_ACCOUNT_SID=AC1234567890abcdef...
TWILIO_AUTH_TOKEN=seu_token_aqui
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

**Método 2: Direto no config.py**

Edite o arquivo `config.py` e substitua:

```python
WHATSAPP_ENABLED = True
TWILIO_ACCOUNT_SID = 'seu_account_sid_aqui'
TWILIO_AUTH_TOKEN = 'seu_auth_token_aqui'
TWILIO_WHATSAPP_NUMBER = 'whatsapp:+14155238886'
```

#### 5️⃣ Testar o Sistema

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Execute o sistema:
```bash
streamlit run app.py
```

3. Faça login e registre uma nova contribuição
4. **IMPORTANTE**: Selecione **"Pix"** como tipo de pagamento
5. Marque a opção "📲 Enviar confirmação via WhatsApp" (só aparece para PIX)
6. Preencha um número de celular válido
7. Clique em "Registrar"
8. O WhatsApp será enviado automaticamente!

### Como Funciona o Envio de WhatsApp?

#### Fluxo Técnico:

```
1. Usuário preenche formulário de cadastro
   ├── Nome do contribuinte
   ├── Valor da contribuição
   ├── Tipo de pagamento: **PIX** (obrigatório para WhatsApp)
   ├── Celular (obrigatório)
   └── Email (opcional)
   
2. Sistema valida o tipo de pagamento
   ├── Se tipo == "Pix":
   │   ├── Checkbox WhatsApp é exibido
   │   └── Usuário pode marcar para enviar
   └── Se tipo != "Pix":
       └── Mensagem informativa: "WhatsApp disponível apenas para PIX"

3. Sistema valida o número de celular
   ├── Verifica formato brasileiro (11 dígitos)
   ├── Valida DDD
   └── Confirma que é celular (inicia com 9)
   
4. Dados são salvos no banco SQLite
   
5. Se WhatsApp estiver habilitado E tipo == "Pix":
   ├── Sistema formata número para padrão internacional
   │   Exemplo: (11) 98765-4321 → whatsapp:+5511987654321
   │
   ├── Monta mensagem personalizada:
   │   🙏 *Ministério Dechonai*
   │   Olá João!
   │   ✅ Sua contribuição foi registrada com sucesso:
   │   • Categoria: Dízimo
   │   • Valor: R$ 100,00
   │   • Data: 07/02/2026
   │
   ├── Envia via Twilio API
   │   POST https://api.twilio.com/2010-04-01/Accounts/{SID}/Messages.json
   │
   └── Retorna confirmação ou erro
```

#### Código Comentado (`whatsapp_service.py`):

```python
def enviar_confirmacao_contribuicao(telefone, nome, valor, categoria, data):
    """
    Envia mensagem WhatsApp de confirmação
    
    Processo:
    1. Valida se serviço está habilitado
    2. Formata número brasileiro → internacional
    3. Cria mensagem personalizada
    4. Envia via Twilio API
    5. Retorna status
    """
    
    # 1. Formatar número
    numero_formatado = formatar_numero_whatsapp(telefone)
    # Input: "(11) 98765-4321"
    # Output: "whatsapp:+5511987654321"
    
    # 2. Montar mensagem
    mensagem = f"""
    🙏 *Ministério Dechonai*
    Olá {nome}!
    ✅ Sua contribuição foi registrada:
    • Categoria: {categoria}
    • Valor: R$ {valor:.2f}
    • Data: {data}
    """
    
    # 3. Enviar via Twilio
    message = client.messages.create(
        from_=TWILIO_WHATSAPP_NUMBER,
        body=mensagem,
        to=numero_formatado
    )
    
    # 4. Retornar sucesso
    return True, f"Enviado! SID: {message.sid}"
```

### Validação de Telefone

O sistema valida automaticamente:

✅ **Formato aceito**: `(11) 98765-4321` ou `11987654321`
✅ **Requisitos**: 
- 11 dígitos (DDD + número)
- Terceiro dígito deve ser 9 (celular)
- DDD válido (11-99)

❌ **Rejeitados**:
- Telefone fixo (sem o 9)
- Menos de 11 dígitos
- Formato inválido

### Custos e Limites

#### Conta Gratuita (Trial):
- **Crédito inicial**: ~$15 USD
- **Custo por mensagem**: ~$0.005 USD
- **Limite**: ~3.000 mensagens com crédito inicial
- **Restrição**: Apenas números verificados no Sandbox

#### Conta Paga:
- **Plano pré-pago**: Sem mensalidade, paga por uso
- **Custo Brasil**: ~$0.012 USD por mensagem
- **WhatsApp Business**: Número oficial da igreja
- **Sem restrições**: Envia para qualquer número

### Troubleshooting (Solução de Problemas)

#### 🔴 "Serviço WhatsApp não habilitado"
- Verifique se `WHATSAPP_ENABLED=true` no `.env`
- Confirme se as credenciais estão corretas

#### 🔴 "Twilio authentication failed"
- Verifique Account SID e Auth Token
- Acesse console.twilio.com e confirme valores

#### 🔴 "Recipient not opted in"
- O número não confirmou no Sandbox
- Envie `join <código>` para o número Twilio primeiro

#### 🔴 "Invalid phone number"
- Verifique formato do telefone
- Use padrão brasileiro: 55 + DDD + número

### Upgrade para Produção

Para uso profissional com número próprio:

1. **Ativar WhatsApp Business API**:
   - Console Twilio → Messaging → WhatsApp
   - Seguir processo de aprovação do Facebook

2. **Obter Número Dedicado**:
   - Comprar número Twilio no Brasil
   - Ou conectar número existente

3. **Templates Aprovados**:
   - Submeter templates de mensagem
   - Aguardar aprovação do WhatsApp

## 📦 Módulos do Sistema

### 📌 Atualização importante

As rotinas de envio de mensagens (WhatsApp/SMS/Email) foram removidas da aplicação para manter foco no registro e consulta de lançamentos.

#### 1. `config.py` - Configurações
Centraliza todas as configurações do sistema:
- Usuários e níveis de acesso
- Tipos de pagamento e categorias
- Operadoras de celular

#### 2. `database.py` - Banco de Dados
Gerencia todas as operações com o banco SQLite:
- `init_db()`: Inicializa o banco com schema atualizado
- `adicionar_lancamento()`: Adiciona novo lançamento com contatos
- `obter_lancamentos()`: Busca lançamentos com filtros
- `atualizar_lancamento()`: Atualiza lançamento incluindo contatos
- `excluir_lancamento()`: Remove lançamento
- `obter_lancamento_por_id()`: Busca lançamento específico

#### 3. `auth.py` - Autenticação
Sistema de controle de acesso:
- `verificar_login()`: Valida credenciais
- `tem_permissao()`: Verifica permissões hierárquicas
- `pode_editar()`: Verifica permissão de edição
- `pode_administrar()`: Verifica permissão administrativa

#### 4. `utils.py` - Utilitários
Funções auxiliares do sistema:
- `display_logo()`: Exibe logo da igreja
- `formatar_valor()`: Formata valores monetários
- `formatar_data()`: Formata datas
- `validar_nome()`: Valida nomes de contribuintes
- `validar_valor()`: Valida valores numéricos
- `calcular_totais()`: Calcula estatísticas financeiras
- `exibir_usuario_info()`: Exibe informações do usuário logado

#### 5. `notifications.py` - Validações de Contato
Responsável por validações utilitárias de email e celular usadas na edição de lançamentos.

**Funções de Validação:**
- `validar_email()`: Valida formato de email
- `validar_celular()`: Valida DDD e número de celular
- `formatar_telefone()`: Formata para padrão internacional

**Funções de Envio:**
- `enviar_email()`: Envia email HTML personalizado
  - Template responsivo
  - Dados da contribuição
  - Versículo bíblico
  - Conexão SMTP configurável
  
- `enviar_sms()`: Envia SMS de confirmação
  - Mensagem otimizada (160 caracteres)
  - Integração com Twilio
  - Formatação de número internacional
  
- `enviar_notificacoes()`: Envia ambas notificações
  - Gerencia email e SMS em conjunto
  - Retorna status de cada envio
  - Tratamento de erros individual

## 🚀 Como Executar

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

1. **Clone o repositório ou baixe os arquivos**

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **⚠️ CONFIGURE AS SENHAS (OBRIGATÓRIO):**

   **a) Copie o arquivo de exemplo:**
   ```bash
   copy .env.example .env    # Windows
   cp .env.example .env      # Linux/Mac
   ```

   **b) Gere hashes de senhas seguras:**
   ```bash
   python generate_password_hash.py
   ```

   **c) Adicione os hashes gerados ao arquivo `.env`:**
   ```env
   USER_ADMIN_HASH=$2b$12$hash_gerado_pelo_script
   USER_DIACONO01_HASH=$2b$12$hash_gerado_pelo_script
   USER_DIACONO02_HASH=$2b$12$hash_gerado_pelo_script
   ```

   **d) Verifique que o `.env` está no `.gitignore`** (já deve estar!)

4. **(Opcional) Para usar notificações reais:**
```bash
# As dependências já estão no requirements.txt
# Basta configurar as credenciais no .env
```

### Configuração de Notificações

### Configuração de Notificações

#### Email (SMTP)
Edite o arquivo `config.py` com suas credenciais:

```python
# Para Gmail:
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_REMETENTE = "seu-email@gmail.com"
EMAIL_SENHA = "sua-senha-de-app"  # Gere em: https://myaccount.google.com/apppasswords
```

**IMPORTANTE**: Para Gmail, use "Senha de App", não sua senha normal.

#### SMS (Twilio)
1. Crie uma conta em: https://www.twilio.com/
2. Obtenha suas credenciais
3. Configure em `config.py`:

```python
TWILIO_ACCOUNT_SID = "seu_account_sid"
TWILIO_AUTH_TOKEN = "seu_auth_token"
TWILIO_PHONE_NUMBER = "+5511999999999"  # Número Twilio
```

#### Habilitar/Desabilitar Notificações
Em `config.py`:

```python
NOTIFICACOES_HABILITADAS = True  # True = ativo, False = desativado
ENVIAR_EMAIL_AUTO = True         # Envio automático de email
ENVIAR_SMS_AUTO = True           # Envio automático de SMS
```

### Execução

Execute o comando:
```bash
streamlit run app.py
```

Ou utilize a configuração personalizada:
```bash
python -m streamlit run app.py --server.port=8501
```

A aplicação estará disponível em: http://localhost:8501 (ou porta 8000 se usar o comando acima)

## 👥 Usuários e Níveis de Acesso

### Níveis de Acesso:
- **Visualizador**: Apenas visualiza seus próprios lançamentos
- **Editor**: Visualiza e registra novos lançamentos
- **Admin**: Acesso completo (visualizar, registrar, editar e excluir)

### Usuários Configurados:

O sistema possui 3 usuários pré-configurados:

| Usuário | Nível | Nome |
|---------|-------|------|
| admin | Admin | Administrador |
| diacono01 | Admin | Diácono01 |
| diacono02 | Admin | Diácono02 |

### ⚠️ IMPORTANTE: Configuração de Senhas

**As senhas NÃO estão mais armazenadas em texto plano!**

Para configurar as senhas dos usuários:

1. **Execute o gerador de hashes:**
   ```bash
   python generate_password_hash.py
   ```

2. **O script irá solicitar:**
   - Nome do usuário (admin, diacono01, diacono02)
   - Senha desejada (crie uma senha forte!)

3. **Copie o hash gerado e adicione ao arquivo `.env`:**
   ```env
   USER_ADMIN_HASH=$2b$12$hash_gerado_aqui
   USER_DIACONO01_HASH=$2b$12$hash_gerado_aqui
   USER_DIACONO02_HASH=$2b$12$hash_gerado_aqui
   ```

4. **Salve o arquivo `.env`**

**Consulte a seção 🔐 Segurança e Autenticação acima para instruções completas.**

## 📊 Banco de Dados

O sistema utiliza SQLite para armazenamento local dos dados. O banco de dados é criado automaticamente na primeira execução.

### Estrutura da Tabela `lancamentos`:
- `id`: Identificador único (auto-incremento)
- `data`: Data do lançamento (YYYY-MM-DD)
- `nome`: Nome completo do contribuinte
- `valor`: Valor da contribuição (REAL)
- `tipo`: Tipo de pagamento (Dinheiro, Cartão, Transferência, Cheque, Pix)
- `categoria`: Categoria (Dízimo, Oferta, Visitante)
- `usuario`: Usuário que registrou o lançamento
- **`email`**: Email do contribuinte (OPCIONAL - NOVO)
- **`codigo_area`**: DDD do celular (OPCIONAL - NOVO)
- **`celular`**: Número do celular (OPCIONAL - NOVO)
- **`operadora`**: Operadora do celular (OPCIONAL - NOVO)
- `created_at`: Timestamp de criação automática

### Operações Disponíveis:

**Inserir Lançamento:**
```python
adicionar_lancamento(
    data="2026-02-07",
    nome="João Silva",
    valor=100.00,
    tipo="Pix",
    categoria="Dízimo",
    usuario="admin",
    email="joao@email.com",  # Opcional
    codigo_area="11",         # Opcional
    celular="999999999",      # Opcional
    operadora="Vivo"          # Opcional
)
```

**Buscar Lançamentos:**
```python
# Admin vê todos
lancamentos = obter_lancamentos()

# Usuário comum vê apenas os seus
lancamentos = obter_lancamentos("usuario123", "visualizador")
```

**Atualizar Lançamento:**
```python
atualizar_lancamento(
    id_lancamento=1,
    data="2026-02-07",
    nome="João Silva Atualizado",
    valor=150.00,
    tipo="Dinheiro",
    categoria="Oferta",
    email="novo@email.com",
    codigo_area="21",
    celular="988888888",
    operadora="Claro"
)
```

## 📧 Sistema de Notificações - Detalhes Técnicos

### Fluxo de Envio

1. **Usuário preenche formulário** de registro com dados opcionais de contato
2. **Sistema valida** email e celular
3. **Lançamento é salvo** no banco de dados
4. **Notificações são enviadas** (se habilitadas e dados válidos)
5. **Feedback visual** para o usuário sobre status do envio

### Validações Implementadas

#### Email:
- Verifica presença de `@` e `.`
- Formato básico de email válido

#### Celular:
- DDD deve ter 2 dígitos
- Celular deve ter 8 ou 9 dígitos
- Remove caracteres não numéricos automaticamente

### Templates de Mensagens

#### Email HTML
```html
Template responsivo com:
- Cabeçalho personalizado
- Dados da contribuição em destaque
- Versículo bíblico (2 Coríntios 9:7)
- Rodapé informativo
```

#### SMS Texto
```
Olá {nome}! Agradecemos sua contribuição de R$ {valor} 
({categoria}). Que Deus abençoe! - Ministério Dechonai
```

### Modo Simulação

Por padrão, o sistema opera em **modo simulação** (para desenvolvimento/testes):
- Mensagens são impressas no console
- Nenhum email/SMS real é enviado
- Retorna sucesso para testes

Para **ativar envios reais**, edite `notifications.py`:

1. **Email** - Descomente as linhas:
```python
servidor = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
servidor.starttls()
servidor.login(EMAIL_REMETENTE, EMAIL_SENHA)
servidor.send_message(mensagem)
servidor.quit()
```

2. **SMS** - Descomente as linhas:
```python
from twilio.rest import Client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
message = client.messages.create(
    body=mensagem_sms,
    from_=TWILIO_PHONE_NUMBER,
    to=numero_completo
)
```

## 💡 Exemplos de Uso

### Registrar Contribuição com Notificações

1. Faça login como `admin` ou `tesoureiro`
2. Vá em **"Registrar"**
3. Preencha os dados básicos:
   - Data
   - Nome completo
   - Valor
   - Tipo de pagamento
   - Categoria
4. Preencha os dados de contato (opcional):
   - Email
   - DDD + Celular
   - Operadora
5. Marque as opções de notificação desejadas
6. Clique em **"Registrar Lançamento"**
7. Sistema envia notificações e exibe confirmação

### Visualizar Lançamentos com Contatos

1. Vá em **"Visualizar"**
2. Veja a tabela com colunas adicionais:
   - Email
   - Celular formatado: (DDD) NÚMERO
3. Confira resumo financeiro atualizado

### Editar Informações de Contato

1. Login como `admin`
2. Vá em **"Editar"**
3. Selecione o lançamento
4. Atualize email ou celular
5. Salve as alterações

## 🔒 Segurança

**IMPORTANTE**: Este é um protótipo para ambiente de desenvolvimento/testes. Para uso em produção, recomenda-se:

### Autenticação e Senhas
- ✅ **Usar variáveis de ambiente** para credenciais
- ✅ **Implementar hash de senhas** (bcrypt, argon2)
- ✅ **Autenticação OAuth** ou JWT
- ✅ **Implementar 2FA** (autenticação de dois fatores)

### Comunicação e Dados
- ✅ **Configurar HTTPS** em produção
- ✅ **Criptografar dados sensíveis** no banco
- ✅ **Usar variáveis de ambiente** para configurações SMTP/Twilio
- ✅ **Validar e sanitizar** todas as entradas de usuário

### Logs e Auditoria
- ✅ **Implementar logs de auditoria** para todas as operações
- ✅ **Rastrear alterações** em lançamentos
- ✅ **Monitorar tentativas de login** falhadas
- ✅ **Backup automático** do banco de dados

### Proteção de Dados Pessoais (LGPD)
- ✅ **Solicitar consentimento** para envio de notificações
- ✅ **Permitir exclusão** de dados pessoais
- ✅ **Armazenar logs** de consentimento
- ✅ **Criptografar informações** de contato

## 🛠️ Tecnologias Utilizadas

### Core
- **Python 3.8+**: Linguagem base
- **Streamlit 1.28+**: Framework web interativo
- **SQLite**: Banco de dados relacional embutido
- **Pandas 2.0+**: Análise e manipulação de dados

### UI/UX
- **Streamlit Option Menu**: Menu lateral customizado
- **Pillow 10.0+**: Processamento de imagens (logo)

### Notificações (Opcional)
- **smtplib**: Envio de emails (biblioteca padrão Python)
- **email.mime**: Criação de mensagens HTML
- **Twilio SDK**: Envio de SMS (requer instalação)

## 📝 Melhorias Futuras

### Funcionalidades
- [ ] Exportação de relatórios (PDF, Excel, CSV)
- [ ] Filtros avançados de busca e data
- [ ] Dashboard com gráficos interativos
- [ ] Relatórios mensais/anuais automatizados
- [ ] Sistema de metas de arrecadação
- [ ] Categorias personalizáveis

### Notificações
- [ ] Templates de email customizáveis
- [ ] Agendamento de envio de relatórios
- [ ] Notificações push (PWA)
- [ ] WhatsApp Business API
- [ ] Confirmação de recebimento

### Infraestrutura
- [ ] Backup automático em nuvem
- [ ] Migração para PostgreSQL
- [ ] Deploy em cloud (AWS, Azure, Heroku)
- [ ] Containerização (Docker)
- [ ] CI/CD pipeline
- [ ] Modo escuro/claro

### Segurança
- [ ] Autenticação com OAuth2
- [ ] Rate limiting
- [ ] Logs de auditoria completos
- [ ] Criptografia de dados sensíveis
- [ ] Compliance com LGPD

## 🐛 Solução de Problemas

### Erro ao enviar email

**Problema**: "Erro ao enviar email: Authentication failed"

**Solução**:
1. Para Gmail, gere uma "Senha de App" em https://myaccount.google.com/apppasswords
2. Não use sua senha normal do Gmail
3. Verifique se 2FA está ativado na sua conta Google
4. Atualize `EMAIL_SENHA` em `config.py`

### Erro ao enviar SMS

**Problema**: "Erro ao enviar SMS: Unable to create record"

**Solução**:
1. Verifique suas credenciais do Twilio
2. Confirme que seu número Twilio está ativo
3. Verifique saldo da conta Twilio
4. Teste com um número verificado primeiro

### Banco de dados não cria

**Problema**: Tabelas não são criadas automaticamente

**Solução**:
```bash
# Delete o banco antigo
rm dizimos_ofertas.db

# Execute novamente
python -m streamlit run app.py
```

### Campos de contato não aparecem

**Problema**: Colunas Email/Celular não mostram na tabela

**Solução**:
1. Verifique se o banco foi atualizado
2. Delete `dizimos_ofertas.db` e reinicie
3. Sistema criará schema atualizado automaticamente

## 📞 Suporte e Contato

Para dúvidas ou sugestões sobre o sistema:

- **Igreja**: Ministério Dechonai
- **Desenvolvedor**: Sistema desenvolvido em Python/Streamlit
- **Versão**: 2.0 (com Sistema de Notificações)
- **Última Atualização**: Fevereiro 2026

## 📄 Licença

Este projeto é de código aberto e está disponível para uso e modificação.

**Uso Livre** para:
- Igrejas e organizações religiosas
- Estudos e aprendizado
- Modificação e customização

**Recomendações**:
- Manter créditos aos desenvolvedores
- Compartilhar melhorias com a comunidade
- Usar de acordo com princípios éticos e cristãos

## ✨ Créditos

Desenvolvido para o **Ministério Dechonai**

**Features desenvolvidas**:
- ✅ Sistema de autenticação multi-nível
- ✅ Gestão completa de lançamentos
- ✅ Relatórios financeiros automáticos
- ✅ **Sistema de notificações Email/SMS (NOVO)**
- ✅ **Cadastro de contatos (NOVO)**
- ✅ **Validações de email e celular (NOVO)**
- ✅ Arquitetura modular e escalável
- ✅ Interface intuitiva e responsiva

---

**"Cada um dê conforme determinou em seu coração, não com pesar ou por obrigação, pois Deus ama quem dá com alegria." - 2 Coríntios 9:7**

---

## 🚀 Quick Start

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Configurar notificações (opcional)
# Editar config.py com suas credenciais SMTP/Twilio

# 3. Executar aplicação
python -m streamlit run app.py

# 4. Acessar no navegador
# http://localhost:8501

# 5. Login inicial
# Usuário: admin
# Senha: Admin@#
```

**Pronto! Sistema funcionando! 🎉**

Este projeto é de código aberto e está disponível para uso e modificação.

## ✨ Autor

Desenvolvido para o Ministério Dechonai
