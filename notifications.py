"""
Módulo de Notificações - Envio de SMS e Email
Responsável por enviar notificações aos contribuintes após cadastro
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, Dict
from config import (
    SMTP_SERVER, SMTP_PORT, EMAIL_REMETENTE, EMAIL_SENHA,
    TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER,
    NOTIFICACOES_HABILITADAS, ENVIAR_EMAIL_AUTO, ENVIAR_SMS_AUTO
)


def validar_email(email: str) -> bool:
    """
    Valida se o formato do email é válido
    
    Args:
        email: Endereço de email a ser validado
    
    Returns:
        True se válido, False caso contrário
    """
    if not email or '@' not in email or '.' not in email:
        return False
    return True


def validar_celular(codigo_area: str, celular: str) -> bool:
    """
    Valida se o código de área e celular são válidos
    
    Args:
        codigo_area: Código de área (DDD)
        celular: Número do celular
    
    Returns:
        True se válido, False caso contrário
    """
    if not codigo_area or not celular:
        return False
    
    # Remover caracteres não numéricos
    codigo_area = ''.join(filter(str.isdigit, codigo_area))
    celular = ''.join(filter(str.isdigit, celular))
    
    # Validar comprimento
    if len(codigo_area) != 2:
        return False
    
    if len(celular) not in [8, 9]:  # Aceita celular com 8 ou 9 dígitos
        return False
    
    return True


def formatar_telefone(codigo_area: str, celular: str) -> str:
    """
    Formata o número de telefone no padrão internacional
    
    Args:
        codigo_area: Código de área (DDD)
        celular: Número do celular
    
    Returns:
        Telefone formatado no padrão +55DDNNNNNNNNN
    """
    # Remover caracteres não numéricos
    codigo_area = ''.join(filter(str.isdigit, codigo_area))
    celular = ''.join(filter(str.isdigit, celular))
    
    return f"+55{codigo_area}{celular}"


def enviar_email(
    destinatario: str, 
    nome: str, 
    valor: float, 
    categoria: str, 
    data: str
) -> Dict[str, any]:
    """
    Envia email de confirmação de contribuição
    
    Args:
        destinatario: Email do destinatário
        nome: Nome do contribuinte
        valor: Valor da contribuição
        categoria: Categoria (Dízimo, Oferta, Visitante)
        data: Data da contribuição
    
    Returns:
        Dicionário com status e mensagem
    """
    # Verificar se notificações estão habilitadas
    if not NOTIFICACOES_HABILITADAS or not ENVIAR_EMAIL_AUTO:
        return {
            "sucesso": False,
            "mensagem": "Envio de email desabilitado nas configurações"
        }
    
    # Validar email
    if not validar_email(destinatario):
        return {
            "sucesso": False,
            "mensagem": "Email inválido"
        }
    
    try:
        # Criar mensagem
        mensagem = MIMEMultipart()
        mensagem['From'] = EMAIL_REMETENTE
        mensagem['To'] = destinatario
        mensagem['Subject'] = f"Confirmação de {categoria} - Ministério Dechonai"
        
        # Corpo do email em HTML
        corpo_html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; border: 1px solid #ddd; padding: 20px; border-radius: 10px;">
                    <h2 style="color: #2c3e50; text-align: center;">🙏 Ministério Dechonai</h2>
                    <hr style="border: 1px solid #eee;">
                    
                    <p style="font-size: 16px;">Olá, <strong>{nome}</strong>!</p>
                    
                    <p style="font-size: 14px;">
                        Agradecemos sua contribuição! Que Deus multiplique essa semente plantada.
                    </p>
                    
                    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <h3 style="color: #2c3e50; margin-top: 0;">Detalhes da Contribuição</h3>
                        <p><strong>Tipo:</strong> {categoria}</p>
                        <p><strong>Valor:</strong> R$ {valor:.2f}</p>
                        <p><strong>Data:</strong> {data}</p>
                    </div>
                    
                    <p style="font-size: 14px; color: #666;">
                        "Cada um dê conforme determinou em seu coração, não com pesar ou por obrigação, 
                        pois Deus ama quem dá com alegria." - 2 Coríntios 9:7
                    </p>
                    
                    <hr style="border: 1px solid #eee; margin-top: 20px;">
                    <p style="font-size: 12px; color: #999; text-align: center;">
                        Este é um email automático. Por favor, não responda.
                    </p>
                </div>
            </body>
        </html>
        """
        
        mensagem.attach(MIMEText(corpo_html, 'html'))
        
        # Conectar ao servidor SMTP e enviar
        # NOTA: Em produção, usar credenciais reais configuradas
        # servidor = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        # servidor.starttls()
        # servidor.login(EMAIL_REMETENTE, EMAIL_SENHA)
        # servidor.send_message(mensagem)
        # servidor.quit()
        
        # Simulação de envio (remover em produção)
        print(f"[SIMULAÇÃO] Email enviado para {destinatario}")
        
        return {
            "sucesso": True,
            "mensagem": f"Email enviado com sucesso para {destinatario}"
        }
        
    except Exception as e:
        return {
            "sucesso": False,
            "mensagem": f"Erro ao enviar email: {str(e)}"
        }


def enviar_sms(
    codigo_area: str,
    celular: str,
    nome: str,
    valor: float,
    categoria: str
) -> Dict[str, any]:
    """
    Envia SMS de confirmação de contribuição
    
    Args:
        codigo_area: Código de área (DDD)
        celular: Número do celular
        nome: Nome do contribuinte
        valor: Valor da contribuição
        categoria: Categoria (Dízimo, Oferta, Visitante)
    
    Returns:
        Dicionário com status e mensagem
    """
    # Verificar se notificações estão habilitadas
    if not NOTIFICACOES_HABILITADAS or not ENVIAR_SMS_AUTO:
        return {
            "sucesso": False,
            "mensagem": "Envio de SMS desabilitado nas configurações"
        }
    
    # Validar celular
    if not validar_celular(codigo_area, celular):
        return {
            "sucesso": False,
            "mensagem": "Número de celular inválido"
        }
    
    try:
        # Formatar número completo
        numero_completo = formatar_telefone(codigo_area, celular)
        
        # Mensagem SMS (máximo 160 caracteres)
        mensagem_sms = (
            f"Olá {nome}! Agradecemos sua contribuição de R$ {valor:.2f} "
            f"({categoria}). Que Deus abençoe! - Ministério Dechonai"
        )
        
        # NOTA: Integração com Twilio (descomentar em produção com credenciais válidas)
        # from twilio.rest import Client
        # client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        # message = client.messages.create(
        #     body=mensagem_sms,
        #     from_=TWILIO_PHONE_NUMBER,
        #     to=numero_completo
        # )
        
        # Simulação de envio (remover em produção)
        print(f"[SIMULAÇÃO] SMS enviado para {numero_completo}")
        print(f"[SIMULAÇÃO] Mensagem: {mensagem_sms}")
        
        return {
            "sucesso": True,
            "mensagem": f"SMS enviado com sucesso para {numero_completo}"
        }
        
    except Exception as e:
        return {
            "sucesso": False,
            "mensagem": f"Erro ao enviar SMS: {str(e)}"
        }


def enviar_notificacoes(
    nome: str,
    valor: float,
    categoria: str,
    data: str,
    email: Optional[str] = None,
    codigo_area: Optional[str] = None,
    celular: Optional[str] = None
) -> Dict[str, any]:
    """
    Envia notificações (Email e SMS) de uma só vez
    
    Args:
        nome: Nome do contribuinte
        valor: Valor da contribuição
        categoria: Categoria da contribuição
        data: Data da contribuição
        email: Email do destinatário (opcional)
        codigo_area: Código de área do celular (opcional)
        celular: Número do celular (opcional)
    
    Returns:
        Dicionário com resultados de ambos os envios
    """
    resultados = {
        "email": None,
        "sms": None,
        "algum_sucesso": False
    }
    
    # Tentar enviar email se fornecido
    if email:
        resultados["email"] = enviar_email(email, nome, valor, categoria, data)
        if resultados["email"]["sucesso"]:
            resultados["algum_sucesso"] = True
    
    # Tentar enviar SMS se fornecido
    if codigo_area and celular:
        resultados["sms"] = enviar_sms(codigo_area, celular, nome, valor, categoria)
        if resultados["sms"]["sucesso"]:
            resultados["algum_sucesso"] = True
    
    return resultados
