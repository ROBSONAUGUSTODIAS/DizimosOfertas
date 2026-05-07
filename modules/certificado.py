"""
Página de Certificado
Exibe o certificado de batismo e permite baixar em PDF A4 (210 x 297 mm).
"""

import io
import os

import streamlit as st
from PIL import Image, ImageFilter
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


def _obter_caminho_certificado() -> str:
    """Retorna o caminho absoluto da imagem do certificado."""
    raiz_projeto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(raiz_projeto, "imagem", "Certificado-Batismo-Dechomai.png")


def _preparar_imagem_alta_resolucao(caminho_imagem: str) -> Image.Image:
    """Prepara a imagem para melhor definição em tela e impressão."""
    largura_a4_px_300dpi = 2480
    altura_a4_px_300dpi = 3508

    imagem_pil = Image.open(caminho_imagem).convert("RGB")

    # Mantem o certificado em orientacao vertical.
    if imagem_pil.width > imagem_pil.height:
        imagem_pil = imagem_pil.rotate(90, expand=True)

    # Eleva a resolução de referencia para impressão A4 em 300 DPI quando necessário.
    escala = max(1.0, min(
        largura_a4_px_300dpi / imagem_pil.width,
        altura_a4_px_300dpi / imagem_pil.height,
    ))
    if escala > 1.0:
        novo_tamanho = (
            int(round(imagem_pil.width * escala)),
            int(round(imagem_pil.height * escala)),
        )
        imagem_pil = imagem_pil.resize(novo_tamanho, Image.Resampling.LANCZOS)

    # Realca levemente contornos para impressão sem exagero.
    imagem_pil = imagem_pil.filter(ImageFilter.UnsharpMask(radius=1.2, percent=130, threshold=3))
    return imagem_pil


def _preparar_imagem_compacta(caminho_imagem: str) -> Image.Image:
    """Prepara a imagem para um PDF menor, mantendo boa legibilidade."""
    largura_a4_px_150dpi = 1240
    altura_a4_px_150dpi = 1754

    imagem_pil = Image.open(caminho_imagem).convert("RGB")

    # Mantem o certificado em orientacao vertical.
    if imagem_pil.width > imagem_pil.height:
        imagem_pil = imagem_pil.rotate(90, expand=True)

    # Reduz para referencia de 150 DPI, ajudando a diminuir o tamanho final.
    escala = min(
        largura_a4_px_150dpi / imagem_pil.width,
        altura_a4_px_150dpi / imagem_pil.height,
    )
    if escala < 1.0:
        novo_tamanho = (
            int(round(imagem_pil.width * escala)),
            int(round(imagem_pil.height * escala)),
        )
        imagem_pil = imagem_pil.resize(novo_tamanho, Image.Resampling.LANCZOS)

    return imagem_pil


def _gerar_pdf_a4_com_imagem(imagem_pil: Image.Image) -> bytes:
    """Gera um PDF A4 vertical (210 x 297 mm) otimizado para impressão."""
    largura_a4 = 210 * mm
    altura_a4 = 297 * mm

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=(largura_a4, altura_a4))
    pdf.setPageCompression(1)

    imagem = ImageReader(imagem_pil)
    largura_img, altura_img = imagem.getSize()

    # Ajusta para caber no A4 vertical sem cortar conteúdo.
    escala = min(largura_a4 / largura_img, altura_a4 / altura_img)
    largura_final = largura_img * escala
    altura_final = altura_img * escala

    pos_x = (largura_a4 - largura_final) / 2
    pos_y = (altura_a4 - altura_final) / 2

    pdf.drawImage(
        imagem,
        pos_x,
        pos_y,
        width=largura_final,
        height=altura_final,
        preserveAspectRatio=True,
        mask="auto",
    )
    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    return buffer.getvalue()


def exibir_pagina_certificado():
    """Renderiza a tela de certificado no menu."""
    st.title("📜 Certificado")
    st.markdown("Visualização e download do certificado em PDF A4 (210 x 297 mm).")

    caminho_certificado = _obter_caminho_certificado()

    if not os.path.exists(caminho_certificado):
        st.error("Arquivo de certificado não encontrado na pasta imagem.")
        st.info("Caminho esperado: imagem/Certificado-Batismo-Dechomai.png")
        return

    imagem_alta = _preparar_imagem_alta_resolucao(caminho_certificado)
    st.image(imagem_alta, caption="Certificado de Batismo", use_container_width=True)

    st.markdown("### Download do PDF")
    st.caption("Escolha entre máxima qualidade para impressão ou arquivo compacto.")

    col_alta, col_compacta = st.columns(2)

    with col_alta:
        pdf_alta = _gerar_pdf_a4_com_imagem(imagem_alta)
        st.download_button(
            label="⬇️ Alta qualidade (300 DPI)",
            data=pdf_alta,
            file_name="certificado_batismo_a4_alta_300dpi.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

    with col_compacta:
        imagem_compacta = _preparar_imagem_compacta(caminho_certificado)
        pdf_compacto = _gerar_pdf_a4_com_imagem(imagem_compacta)
        st.download_button(
            label="⬇️ Compacto (150 DPI)",
            data=pdf_compacto,
            file_name="certificado_batismo_a4_compacto_150dpi.pdf",
            mime="application/pdf",
            use_container_width=True,
        )