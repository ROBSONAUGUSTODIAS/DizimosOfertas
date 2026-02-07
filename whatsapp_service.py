"""
Módulo de Integração com WhatsApp
Responsável pelo envio de mensagens via WhatsApp para os contribuintes
"""
import os
from typing import Optional
from twilio.rest import Client
from config import (
    TWILIO_ACCOUNT_SID, 
    TWILIO_AUTH_TOKEN, 
    TWILIO_WHATSAPP_NUMBER,
    WHATSAPP_ENABLED
)


class WhatsAppService:
    """
    Serviço para envio de mensagens via WhatsApp usando Twilio API
    
    Requisitos:
    1. Conta Twilio ativa (https://www.twilio.com)
    2. WhatsApp Business API configurado
    3. Número WhatsApp Twilio verificado
    4. Credenciais configuradas no arquivo .env ou config.py
    
    Fluxo de Funcionamento:
    1. Cliente configura credenciais Twilio
    2. Sistema formata número de telefone no padrão internacional
    3. Monta mensagem personalizada com dados da contribuição
    4. Envia mensagem via API Twilio
    5. Retorna status de sucesso ou erro
    """
    
    def __init__(self):
        """
        Inicializa o serviço WhatsApp com as credenciais Twilio
        
        Variáveis necessárias:
        - TWILIO_ACCOUNT_SID: ID da conta Twilio
        - TWILIO_AUTH_TOKEN: Token de autenticação
        - TWILIO_WHATSAPP_NUMBER: Número WhatsApp formato: whatsapp:+14155238886
        """
        self.enabled = WHATSAPP_ENABLED
        
        if self.enabled:
            try:
                self.client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
                self.from_number = TWILIO_WHATSAPP_NUMBER
            except Exception as e:
                print(f"Erro ao inicializar WhatsApp Service: {e}")
                self.enabled = False
    
    def formatar_numero_whatsapp(self, telefone: str) -> str:
        """
        Formata o número de telefone para o padrão WhatsApp internacional
        
        Args:
            telefone: Número no formato (DDD)99999-9999 ou similar
        
        Returns:
            Número formatado: whatsapp:+5511999999999
        
        Exemplo:
            Input: "(11) 98765-4321"
            Output: "whatsapp:+5511987654321"
        """
        # Remove caracteres não numéricos
        numeros = ''.join(filter(str.isdigit, telefone))
        
        # Adiciona código do Brasil (+55) se não tiver
        if not numeros.startswith('55'):
            numeros = '55' + numeros
        
        # Retorna no formato WhatsApp
        return f"whatsapp:+{numeros}"
    
    def enviar_confirmacao_contribuicao(self, telefone: str, nome: str, 
                                       valor: float, categoria: str, 
                                       data: str) -> tuple[bool, str]:
        """
        Envia mensagem de confirmação de contribuição via WhatsApp
        
        Args:
            telefone: Número de telefone do contribuinte
            nome: Nome do contribuinte
            valor: Valor da contribuição
            categoria: Categoria (Dízimo, Oferta, Visitante)
            data: Data da contribuição
        
        Returns:
            (sucesso: bool, mensagem: str): Status e mensagem de retorno
        
        Processo:
        1. Verifica se o serviço está habilitado
        2. Formata o número para padrão internacional
        3. Cria mensagem personalizada
        4. Envia via Twilio API
        5. Retorna resultado
        """
        if not self.enabled:
            return False, "Serviço WhatsApp não habilitado. Configure as credenciais Twilio."
        
        try:
            # Formata número para padrão WhatsApp
            numero_formatado = self.formatar_numero_whatsapp(telefone)
            
            # Monta mensagem personalizada
            mensagem = self._montar_mensagem_contribuicao(nome, valor, categoria, data)
            
            # Envia mensagem via Twilio
            message = self.client.messages.create(
                from_=self.from_number,
                body=mensagem,
                to=numero_formatado
            )
            
            return True, f"Mensagem enviada com sucesso! SID: {message.sid}"
            
        except Exception as e:
            erro = f"Erro ao enviar mensagem WhatsApp: {str(e)}"
            print(erro)
            return False, erro
    
    def _montar_mensagem_contribuicao(self, nome: str, valor: float, 
                                     categoria: str, data: str) -> str:
        """
        Monta mensagem personalizada de confirmação
        
        Args:
            nome: Nome do contribuinte
            valor: Valor da contribuição
            categoria: Categoria da contribuição
            data: Data da contribuição
        
        Returns:
            Mensagem formatada para WhatsApp
        """
        mensagem = f"""
🙏 *Ministério Dechonai*

Olá {nome}!

✅ Sua contribuição foi registrada com sucesso:

📋 *Detalhes:*
• Categoria: {categoria}
• Valor: R$ {valor:.2f}
• Data: {data}

Que Deus abençoe abundantemente sua vida!

_Esta é uma mensagem automática de confirmação._
        """
        return mensagem.strip()
    
    def enviar_mensagem_personalizada(self, telefone: str, mensagem: str) -> tuple[bool, str]:
        """
        Envia uma mensagem personalizada via WhatsApp
        
        Args:
            telefone: Número de telefone
            mensagem: Texto da mensagem
        
        Returns:
            (sucesso: bool, mensagem_retorno: str)
        """
        if not self.enabled:
            return False, "Serviço WhatsApp não habilitado."
        
        try:
            numero_formatado = self.formatar_numero_whatsapp(telefone)
            
            message = self.client.messages.create(
                from_=self.from_number,
                body=mensagem,
                to=numero_formatado
            )
            
            return True, f"Mensagem enviada! SID: {message.sid}"
            
        except Exception as e:
            return False, f"Erro ao enviar: {str(e)}"


# Instância global do serviço
whatsapp_service = WhatsAppService()


def enviar_whatsapp_contribuicao(telefone: str, nome: str, valor: float, 
                                categoria: str, data: str) -> tuple[bool, str]:
    """
    Função auxiliar para enviar confirmação de contribuição
    
    Args:
        telefone: Número de telefone
        nome: Nome do contribuinte
        valor: Valor da contribuição
        categoria: Categoria
        data: Data da contribuição
    
    Returns:
        (sucesso, mensagem)
    """
    return whatsapp_service.enviar_confirmacao_contribuicao(
        telefone, nome, valor, categoria, data
    )
