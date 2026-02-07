# 🔧 SOLUÇÃO: Erro de Autenticação no Streamlit Cloud

## ❌ Problema
Não consigo fazer login em: https://dizimosofertas-dechomai.streamlit.app/

## ✅ Solução: Configurar Secrets

### PASSO 1: Acessar App Settings

1. Acesse: https://share.streamlit.io/
2. Faça login com GitHub
3. Localize o app **DizimosOfertas**
4. Clique nos **3 pontos (⋮)** → **Settings**

### PASSO 2: Configurar Secrets

1. No menu lateral, clique em **Secrets**
2. **Cole EXATAMENTE este conteúdo** na caixa de texto:

```toml
[passwords]
USER_ADMIN_HASH = "$2b$12$kKdAncvxkviV412Bj.WuMe2ve/Qaqkn4sq1CiFXh.QeWF6Bp1hXbq"
USER_DIACONO01_HASH = "$2b$12$7erenEeA2eP5HecUUGGtp.LRxYuxXqYWKb/zNwT8VOIpM6UyeWMEy"
USER_DIACONO02_HASH = "$2b$12$7rxfZGjQqq9cOnpaiRvRnu9vLhNKmKVAFh2zwEvfC9fdaaqmEfSN."
```

3. Clique em **Save**
4. O app irá **reiniciar automaticamente**

### PASSO 3: Testar Login

Aguarde 30-60 segundos e tente fazer login:

```
Usuário: admin
Senha: AdminSeguro@2026
```

Outros usuários para teste:
```
Usuário: diacono01
Senha: Diacono01@2026

Usuário: diacono02
Senha: Diacono02@2026
```

---

## 📋 Checklist de Verificação

Se ainda não funcionar, verifique:

### ✅ Formato dos Secrets

**CORRETO:**
```toml
[passwords]
USER_ADMIN_HASH = "$2b$12$kKdAncvxkviV412Bj.WuMe2ve/Qaqkn4sq1CiFXh.QeWF6Bp1hXbq"
```

**ERRADO:** ❌
```toml
# Sem seção [passwords]
USER_ADMIN_HASH = "$2b$12$..."

# Sem aspas duplas
USER_ADMIN_HASH = $2b$12$...

# Aspas simples (errado!)
USER_ADMIN_HASH = '$2b$12$...'
```

### ✅ Copiar Exatamente

- ✅ Incluir a linha `[passwords]`
- ✅ Usar **aspas duplas** `"` nos valores
- ✅ Não adicionar espaços extras
- ✅ Copiar hashCompleto (começa com `$2b$12$`)
- ✅ Clicar em **Save** após colar

### ✅ Aguardar Restart

- Após salvar, o app mostra: **"App is restarting..."**
- Aguarde a mensagem: **"Your app is running!"**
- Recarregue a página (F5)

---

## 🔍 Como Verificar se Secrets Foram Carregados

### Adicionar Debug Temporário

1. No Streamlit Cloud, vá em **Logs**
2. Procure por erros relacionados a `secrets`
3. Se aparecer `KeyError: 'passwords'` → Secrets não configurados

---

## 🆘 Troubleshooting Avançado

### Problema: Secrets Não Aparecem na Interface

**Solução:**
1. Feche e abra novamente Settings
2. Verifique se você tem permissão de edição no repositório
3. Tente fazer logout e login novamente no Streamlit Cloud

### Problema: App Fica Reiniciando

**Solução:**
1. Vá em **Logs** para ver o erro
2. Se aparecer erro de sintaxe TOML:
   - Verifique aspas duplas
   - Verifique colchetes `[passwords]`
   - Remova espaços no início das linhas

### Problema: Login Funciona Local mas Não na Cloud

**Causa:** Secrets não configurados ou formato incorreto

**Solução:**
1. Delete todo conteúdo da caixa Secrets
2. Cole novamente (copie do box acima)
3. Save e aguarde restart

---

## 📸 Guia Visual

### Como Deve Ficar a Tela de Secrets:

```
┌─────────────────────────────────────┐
│ Secrets                             │
├─────────────────────────────────────┤
│ [passwords]                         │
│ USER_ADMIN_HASH = "$2b$12$kKdA..." │
│ USER_DIACONO01_HASH = "$2b$12$..." │
│ USER_DIACONO02_HASH = "$2b$12$..." │
│                                     │
│         [Save]  [Cancel]            │
└─────────────────────────────────────┘
```

---

## ⚡ Solução Rápida (Copy/Paste)

**Copie este bloco completo:**

```toml
[passwords]
USER_ADMIN_HASH = "$2b$12$kKdAncvxkviV412Bj.WuMe2ve/Qaqkn4sq1CiFXh.QeWF6Bp1hXbq"
USER_DIACONO01_HASH = "$2b$12$7erenEeA2eP5HecUUGGtp.LRxYuxXqYWKb/zNwT8VOIpM6UyeWMEy"
USER_DIACONO02_HASH = "$2b$12$7rxfZGjQqq9cOnpaiRvRnu9vLhNKmKVAFh2zwEvfC9fdaaqmEfSN."
```

---

## 🎯 Próximos Passos

Depois de configurar os Secrets:

1. ✅ Login funcionando? → Teste todas as funcionalidades
2. ✅ WhatsApp/PIX? → Adicione secrets do Twilio (se necessário)
3. ✅ Produção? → Troque as senhas de exemplo!

---

## 🔐 IMPORTANTE: Trocar Senhas em Produção

As senhas atuais são de **TESTE**:
- ❌ AdminSeguro@2026
- ❌ Diacono01@2026
- ❌ Diacono02@2026

**Para trocar:**

1. Rode localmente:
```bash
python generate_password_hash.py
```

2. Gere novos hashes

3. Atualize os Secrets no Streamlit Cloud

---

**🎉 Após configurar os Secrets, o login funcionará!**

**URL do App:** https://dizimosofertas-dechomai.streamlit.app/
