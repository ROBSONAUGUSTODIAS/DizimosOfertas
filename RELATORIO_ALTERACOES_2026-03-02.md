# Relatório de Alterações — 02/03/2026

## Objetivo da solicitação
Implementar no menu **Visualizar** uma opção de consulta de **histórico completo** de lançamentos, remover fluxos de **envio de mensagens**, e limpar itens não utilizados.

## Alterações implementadas

### 1) Consulta de histórico no menu Visualizar
Arquivo: `modules/visualizar.py`

- Alterado o título para **Consulta de Lançamentos**.
- Adicionada seleção de período com duas opções:
  - **Histórico completo**
  - **Últimos 30 dias**
- Incluído filtro de data para os últimos 30 dias.
- Exibição da quantidade de registros encontrados para o período selecionado.
- Mantido o resumo financeiro e tabela conforme o conjunto filtrado.

### 2) Remoção de envio de mensagens no registro
Arquivo: `modules/registrar.py`

- Removido import e uso do `whatsapp_service`.
- Removida lógica de checkbox e envio automático por WhatsApp.
- Campo de celular passou de obrigatório para **opcional**.
- Validação do celular agora ocorre somente quando o campo é preenchido.
- Mantida a gravação de contato no banco quando informado.

### 3) Limpeza de módulo de notificações
Arquivo: `notifications.py`

- Removidas funções de envio (`email` e `sms`).
- Mantidas apenas funções utilitárias usadas no sistema:
  - `validar_email`
  - `validar_celular`

### 4) Limpeza de configurações não usadas
Arquivo: `config.py`

- Removidas configurações de WhatsApp/Twilio.
- Removidas configurações de notificações automáticas (email/sms) que não são mais utilizadas.
- Mantidas apenas configurações realmente consumidas pela aplicação.

### 5) Dependências
Arquivo: `requirements.txt`

- Removida dependência `twilio` por não haver mais envio de mensagens no sistema.

### 6) Documentação ajustada
Arquivos:
- `README.md`
- `COMO_EXECUTAR.md`

- Removidas instruções e referências a recursos de WhatsApp.
- Atualizado texto de funcionalidades para refletir consulta histórica e contatos opcionais.

## Arquivos removidos (não utilizados após limpeza)

- `whatsapp_service.py`
- `enviar_whatsapp_massa.py`
- `enviar_whatsapp_por_data.py`
- `exemplo_envio_hoje.py`
- `exemplo_whatsapp_template.py`
- `testar_whatsapp.py`
- `verificar_whatsapp.py`
- `README_WHATSAPP.md`
- `WHATSAPP_SETUP.md`
- `GUIA_WHATSAPP_COMPLETO.md`
- `ENVIO_POR_DATA.md`

## Validação executada

- Verificação de erros do workspace: **sem erros reportados**.
- Busca por referências de envio/mensageria em arquivos Python: **nenhuma referência restante**.

## Resultado final

- O menu **Visualizar** agora permite consultar explicitamente o **histórico completo**.
- Toda lógica de **envio de mensagens** foi removida do sistema.
- Estrutura foi enxugada, removendo código e arquivos sem uso após a mudança.
