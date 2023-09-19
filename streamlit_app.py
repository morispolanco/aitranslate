import streamlit as st
import requests
from PyPDF2 import PdfFileReader, PdfFileWriter
from io import BytesIO

# Cambiar el título en la pestaña del navegador
st.set_page_config(page_title="AiTranslate")

# URL base de la API de AI Translate
BASE_URL = "https://ai-translate.pro/api"

# Función para traducir texto
def translate_text(text, lang_from, lang_to, secret_key):
    url = f"{BASE_URL}/{secret_key}/{lang_from}-{lang_to}"
    headers = {'Content-Type': 'application/json'}
    data = {"text": text}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()["result"]
        available_chars = response.json()["available_chars"]
        return result, available_chars
    else:
        return None, None

# Título de la aplicación
st.title("AITranslate")

# Agregar título y texto en la parte superior de la columna
st.markdown("# La mejor traducción automática del mundo")
st.markdown("Las redes neuronales de AITranslate son capaces de captar hasta los más mínimos matices y reproducirlos en la traducción a diferencia de cualquier otro servicio. Para evaluar la calidad de nuestros modelos de traducción automática, realizamos regularmente pruebas a ciegas. En las pruebas a ciegas, los traductores profesionales seleccionan la traducción más precisa sin saber qué empresa la produjo. AITranslate supera a la competencia por un factor de 3:1. ")

# Campo de entrada para la clave API
secret_key = st.text_input("Ingrese su clave API de AITranslate", type="password")

# Explicación sobre cómo obtener la clave API
st.markdown("Para obtener la clave API de AI Translate, por favor envíe un correo electrónico a info@editorialarje.com.")

# Cargar archivo PDF
uploaded_file = st.file_uploader("Cargar archivo PDF", type=["pdf"])

# Selección de idiomas
lang_from = st.selectbox("Seleccione el idioma de origen:", ["en", "es"])
lang_to = st.selectbox("Seleccione el idioma de destino:", ["en", "es"])

# Botón para traducir
if st.button("Traducir"):
    if secret_key and uploaded_file is not None:
        # Leer el contenido del archivo PDF
        pdf_reader = PdfFileReader(uploaded_file)
        num_pages = pdf_reader.getNumPages()

        # Extraer el texto de cada página del PDF
        text = ""
        for page_num in range(num_pages):
            page = pdf_reader.getPage(page_num)
            text += page.extractText()

        translation, available_chars = translate_text(text, lang_from, lang_to, secret_key)
        if translation:
            # Crear un nuevo archivo PDF con la traducción
            translated_pdf = PdfFileWriter()
            for page_num in range(num_pages):
                page = pdf_reader.getPage(page_num)
                translated_page = PdfFileReader(BytesIO(translation.encode())).getPage(0)
                page.mergePage(translated_page)
                translated_pdf.addPage(page)

            # Guardar el archivo PDF traducido en un objeto BytesIO
            pdf_buffer = BytesIO()
            translated_pdf.write(pdf_buffer)
            pdf_buffer.seek(0)

            # Descargar el archivo PDF
            st.download_button("Descargar traducción", data=pdf_buffer, file_name="traduccion.pdf")

            st.success("La traducción se ha guardado en el archivo 'traduccion.pdf'")
            st.info(f"Caracteres disponibles: {available_chars}")
        else:
            st.error("Error al traducir el texto. Verifique su clave API o intente nuevamente.")
    else:
        st.error("Por favor, ingrese su clave API de AI Translate y cargue un archivo PDF.")
