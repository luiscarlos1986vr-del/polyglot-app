# -*- coding: utf-8 -*-
"""
interfaz_polyglot.py - Interfaz de Usuario Polyglot (Bilingüe)

Este es el archivo que ven nuestros usuarios cuando abren la aplicación.
Nuestro objetivo es crear una pantalla bonita, fácil de usar y completamente bilingüe
(español/inglés) donde puedan describir su producto y obtener contenido de marketing localizado.
"""

import streamlit as st  # Streamlit nos permite crear interfaces web fácilmente
import requests  # Requests nos ayuda a comunicarnos con nuestra API (el backend)
import time  # Time nos permite crear el efecto "máquina de escribir"


# ==================== CONFIGURACIÓN ====================
# La dirección donde está corriendo nuestra API (el backend)
API_URL = "https://polyglot-app-5crh.onrender.com"

# Configuramos la página: título, ícono y diseño ancho
st.set_page_config(
    page_title="Global-Gadgets | Polyglot",
    page_icon="🌍",
    layout="wide"  # Diseño ancho para aprovechar mejor el espacio
)


# ==================== ESTILOS CSS ====================
# Aquí personalizamos la apariencia de nuestra aplicación
# Los estilos CSS hacen que todo se vea más profesional y agradable
st.markdown("""
<style>
    /* Título principal - grande y llamativo */
    .main-title {
        text-align: center;
        font-size: 5rem;
        color: #6b9bc2;
        margin-bottom: 0;
    }
    .company-name {
        text-align: center;
        font-size: 1.2rem;
        color: #e88710;
        letter-spacing: 2px;
        margin-top: -10px;
        margin-bottom: 5px;
    }
    .subtitle {
        text-align: center;
        color: #888;
        margin-bottom: 2rem;
        font-size: 0.9rem;
    }
    
    /* Tarjeta de producto - un recuadro elegante para la descripción */
    .product-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 0.5rem;
        border-radius: 20px;
        border: 1px solid #333;
        margin-bottom: 0.5rem;
    }
    .product-card h3 {
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
        color: #ccc;
    }
    
    /* Estilos generales para que el texto no opaque el título */
    body, .stMarkdown, .stTextArea, .stSelectbox, .stRadio {
        font-size: 0.85rem;
    }
    
    /* Títulos de secciones más sutiles */
    h1, h2, h3 {
        color: #888;
    }
    h1 {
        font-size: 2rem;
    }
    h2 {
        font-size: 1.3rem;
    }
    h3 {
        font-size: 1.1rem;
        color: #aaa;
    }
    
    /* Footer - el pie de página */
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 0.5rem;
        color: #888;
        font-size: 0.7rem;
        border-top: 0.5px solid #444;
    }
    
    /* Botón principal - el que genera la campaña */
    .stButton > button {
        background: linear-gradient(90deg, #1a6b8a, #2a9d6e);
        color: white;
        font-weight: bold;
        border: none;
        padding: 0.6rem 1.5rem;
        border-radius: 30px;
        transition: transform 0.2s;
        font-size: 0.9rem;
    }
    .stButton > button:hover {
        transform: scale(1.02);  /* Efecto de crecimiento al pasar el mouse */
    }
    
    /* Botones de idioma más pequeños y discretos */
    .stButton > button[key="btn_es"], .stButton > button[key="btn_en"] {
        padding: 0.2rem 0.8rem !important;
        font-size: 0.8rem !important;
        background: #d8e7f0 !important;
        color: #1a1a2e !important;
        border: 1px solid #FFD700 !important;
        border-radius: 20px !important;
        box-shadow: none !important;
        margin: 0 !important;
    }
    .stButton > button[key="btn_es"]:hover, .stButton > button[key="btn_en"]:hover {
        background: #FFD700 !important;
        color: #1a1a2e !important;
        transform: scale(1.02);
    }
    
    /* Estilo para los radio buttons (opciones de selección) */
    div[role="radiogroup"] label {
        margin: 4px 0;
        padding: 5px 10px;
        border-radius: 8px;
        transition: all 0.2s ease;
        cursor: pointer;
        font-size: 0.85rem;
    }
    div[role="radiogroup"] label:hover {
        background-color: #d8e7f0 !important;
        transform: translateX(4px);  /* Se mueve ligeramente a la derecha */
    }
    div[role="radiogroup"] label[data-baseweb="radio"]:has(input:checked) {
        background-color: #d8e7f0 !important;
        font-weight: 500;
        border-left: 3px solid #FFD700;  /* Borde dorado a la izquierda cuando está seleccionado */
    }
    
    /* Expanders más sutiles (las secciones desplegables) */
    .streamlit-expanderHeader {
        font-size: 0.85rem;
        color: #6b9bc2;
        background: transparent;
    }
    
    /* Texto de ayuda más sutil */
    .stCaption, caption {
        font-size: 0.7rem;
        color: #888;
    }
</style>
""", unsafe_allow_html=True)


# ==================== FUNCIÓN EFECTO MÁQUINA DE ESCRIBIR ====================
def mostrar_con_efecto(texto, placeholder, velocidad=0.01):
    """
    Esta función crea el efecto "máquina de escribir" que vemos en los chats de IA.
    Nuestro objetivo es que el texto aparezca caracter por caracter,
    dando una sensación más natural y atractiva para el usuario.
    """
    texto_mostrado = ""
    for char in texto:
        texto_mostrado += char
        placeholder.markdown(texto_mostrado + "▌")  # Mostramos un cursor parpadeante
        time.sleep(velocidad)  # Esperamos un poquito antes de mostrar el siguiente caracter
    placeholder.markdown(texto_mostrado)  # Al final, quitamos el cursor


# ==================== INICIALIZAR IDIOMA ====================
# Guardamos en la memoria de la aplicación qué idioma ha seleccionado el usuario
if "idioma" not in st.session_state:
    st.session_state.idioma = "es"  # español por defecto


# ==================== TEXTO BILINGÜE ====================
def t(clave):
    """
    Esta función es nuestro "traductor" interno.
    Nuestro objetivo es que todos los textos de la interfaz cambien automáticamente
    según el idioma que haya seleccionado el usuario (español o inglés).
    """
    textos = {
        # Header (cabecera)
        "titulo": {"es": "🌍 Polyglot", "en": "🌍 Polyglot"},
        "empresa": {"es": "⚡ Global-Gadgets ⚡", "en": "⚡ Global-Gadgets ⚡"},
        "subtitulo": {"es": "Convierte tu producto en ventas globales 🏆<br>Campaña de Marketing para Brasil | Japón | Alemania", 
                      "en": "Turn your product into global sales 🏆<br>Marketing Campaign for Brazil | Japan | Germany"},
        
        # Selector de idioma
        "idioma_titulo": {"es": "🌐 Idioma", "en": "🌐 Language"},
        "idioma_pregunta": {"es": "Selecciona el idioma", "en": "Select the language"},
        
        # Entrada del producto
        "producto_titulo": {"es": "📦 ¿Qué producto quieres vender al mundo?", 
                           "en": "📦 What product do you want to sell to the world?"},
        "producto_placeholder": {"es": "Ej: Auriculares con cancelación de ruido, 40h de batería",
                                "en": "Ex: Noise-cancelling headphones, 40h battery"},
        
        # Mercado objetivo
        "mercado_titulo": {"es": "🎯 Mercado objetivo", "en": "🎯 Target market"},
        "mercado_desc": {"es": "Selecciona el país para la campaña", "en": "Select the country for the campaign"},
        
        # Motor de generación (IA)
        "motor_titulo": {"es": "🤖 Motor de generación", "en": "🤖 Generation engine"},
        "motor_desc": {"es": "Selecciona qué IA generará tu contenido", "en": "Select which AI will generate your content"},
        
        # Botón principal
        "boton": {"es": "✨ Generar campaña internacional ✨", "en": "✨ Generate international campaign ✨"},
        
        # Resultados
        "comparacion_titulo": {"es": "🏆 Comparación de Motores de IA", "en": "🏆 AI Engines Comparison"},
        "post_titulo": {"es": "📱 Post para Redes Sociales", "en": "📱 Social Media Post"},
        "eslogans_titulo": {"es": "💡 Eslogans Publicitarios", "en": "💡 Advertising Slogans"},
        "email_titulo": {"es": "📧 Email Promocional", "en": "📧 Promotional Email"},
        "traduccion_label": {"es": "🇪🇸 Traducción al español", "en": "🇬🇧 English translation"},
        
        # Mensajes de error y éxito
        "error_producto": {"es": "❌ Por favor, describe tu producto para empezar", 
                          "en": "❌ Please describe your product to start"},
        "error_conexion": {"es": "❌ No se pudo conectar al servidor", 
                          "en": "❌ Could not connect to server"},
        "exito": {"es": "✅ ¡Campaña generada exitosamente para ", 
                 "en": "✅ Campaign successfully generated for "},
        
        # Spinner (mensaje de carga)
        "spinner": {"es": "🚀 Generando contenido para {} con {}...",
                   "en": "🚀 Generating content for {} with {}..."},
        
        # Footer (pie de página)
        "footer_empresa": {"es": "🌍 <strong>Global-Gadgets</strong> - Polyglot Marketing Multilingüe",
                          "en": "🌍 <strong>Global-Gadgets</strong> - Polyglot Multilingual Marketing"},
        "footer_poten": {"es": "Potenciado por Gemini | Deepseek | Mistral",
                        "en": "Powered by Gemini | Deepseek | Mistral"},
    }
    # Devolvemos el texto en el idioma seleccionado (si no existe, usamos español)
    return textos.get(clave, {}).get(st.session_state.idioma, textos.get(clave, {}).get("es", clave))


# ==================== HEADER (CABECERA) ====================
# Mostramos el título, el nombre de la empresa y el subtítulo
st.markdown(f'<p class="main-title">{t("titulo")}</p>', unsafe_allow_html=True)
st.markdown(f'<p class="company-name">{t("empresa")}</p>', unsafe_allow_html=True)
st.markdown(f'<p class="subtitle">{t("subtitulo")}</p>', unsafe_allow_html=True)


# ==================== SELECTOR DE IDIOMA ÚNICO ====================
# Esta sección permite al usuario cambiar el idioma de toda la interfaz
st.markdown("---")
st.markdown(f"### {t('idioma_titulo')}")
st.markdown(t("idioma_pregunta"))

# Creamos una fila con columnas para centrar los botones de idioma
col_lang1, col_lang2, col_lang3, col_lang4, col_lang5 = st.columns([2, 1, 1, 1, 2])
with col_lang2:
    if st.button("🇪🇸 Español", key="btn_es", use_container_width=True):
        st.session_state.idioma = "es"
        st.rerun()  # Recargamos la página para aplicar el cambio
with col_lang3:
    if st.button("🇬🇧 English", key="btn_en", use_container_width=True):
        st.session_state.idioma = "en"
        st.rerun()

st.markdown("---")


# ==================== IDIOMA DE ENTRADA DEL PRODUCTO ====================
# El idioma en que el usuario escribe la descripción es el mismo que seleccionó para la interfaz
idioma_entrada = "es" if st.session_state.idioma == "es" else "en"


# ==================== ENTRADA DEL PRODUCTO ====================
# Aquí el usuario escribe la descripción de su producto
with st.container():
    st.markdown('<div class="product-card">', unsafe_allow_html=True)
    st.markdown(f"### {t('producto_titulo')}")
    descripcion = st.text_area(
        "Descripción del producto",
        placeholder=t("producto_placeholder"),
        height=80,
        label_visibility="collapsed"  # Ocultamos la etiqueta porque ya tenemos un título
    )
    st.markdown('</div>', unsafe_allow_html=True)


# ==================== CONFIGURACIÓN EN COLUMNAS ====================
# Dividimos la pantalla en dos columnas: una para el mercado, otra para la IA
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"### {t('mercado_titulo')}")
    st.markdown(t("mercado_desc"))
    
    # Opciones de mercado con banderas (emojis)
    mercado_opciones = {
        "🇧🇷 Brasil": "brasil",
        "🇯🇵 Japón": "japon",
        "🇩🇪 Alemania": "alemania"
    }
    
    # Radio button para seleccionar el país
    mercado_seleccionado = st.radio(
        "Mercado",
        options=list(mercado_opciones.keys()),
        index=0,  # Brasil seleccionado por defecto
        label_visibility="collapsed"
    )
    mercado = mercado_opciones[mercado_seleccionado]

with col2:
    st.markdown(f"### {t('motor_titulo')}")
    st.markdown(t("motor_desc"))
    
    # Opciones de IA disponibles
    llm_opciones = {
        "Gemini (Google)": "gemini",
        "Deepseek (DeepSeek)": "deepseek",
        "Mistral (Mistral AI)": "mistral",
        "Todos (Comparar)": "todos"
    }
    
    # Radio button para seleccionar la IA
    llm_seleccionado = st.radio(
        "LLM",
        options=list(llm_opciones.keys()),
        index=0,  # Gemini seleccionado por defecto
        label_visibility="collapsed"
    )
    llm = llm_opciones[llm_seleccionado]


# ==================== BOTÓN DE GENERACIÓN ====================
# Centramos el botón principal en la pantalla
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    generar = st.button(t("boton"), type="primary", use_container_width=True)


# ==================== FUNCIONES DE VISUALIZACIÓN ====================
def mostrar_comparacion(resultado, mercado_nombre):
    """
    Esta función muestra los resultados cuando el usuario eligió "Todos (Comparar)".
    Nuestro objetivo es presentar las respuestas de las tres IAs lado a lado
    para que el usuario pueda compararlas fácilmente y elegir la mejor.
    """
    st.markdown("---")
    st.markdown(f"## {t('comparacion_titulo')}")
    
    # Verificamos que haya datos para mostrar
    if "post" not in resultado["contenido"]:
        st.warning("No hay datos de post para comparar")
        return
    
    posts = resultado["contenido"]["post"]
    
    # Colores y estilos para las tarjetas de comparación
    color_fondo = "#d8e7f0"
    color_borde = "#FFD700"
    color_texto = "#1a1a2e"
    
    texto_traduccion = t("traduccion_label")
    
    # Creamos tres columnas, una para cada IA
    col1, col2, col3 = st.columns(3)
    llms_orden = ["Deepseek", "Mistral", "Gemini"]
    
    for idx, llm_nombre in enumerate(llms_orden):
        with [col1, col2, col3][idx]:
            datos_post = posts.get(llm_nombre, {})
            
            if datos_post.get("exito"):
                # Tarjeta con la información de la IA
                st.markdown(f"""
                <div style="background: {color_fondo}; border-radius: 16px; padding: 0.8rem; margin: 0.5rem 0; border-left: 4px solid {color_borde};">
                    <div style="text-align: center; font-size: 1rem; font-weight: 600; color: {color_texto};">{llm_nombre}</div>
                    <div style="text-align: center; font-size: 0.7rem; color: #555;">⏱️ {datos_post.get("tiempo_ms", 0)} ms</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Mostramos el post generado
                respuesta_post = datos_post.get("respuesta", "")
                traduccion_post = datos_post.get("traduccion", "")
                
                st.markdown(f"#### {t('post_titulo')}")
                container_post = st.empty()
                mostrar_con_efecto(respuesta_post, container_post, velocidad=0.01)
                
                # Mostramos la traducción si existe
                if traduccion_post:
                    st.markdown("---")
                    st.markdown(f"**{texto_traduccion}:**")
                    container_trad = st.empty()
                    mostrar_con_efecto(traduccion_post, container_trad, velocidad=0.01)
                
                # Mostramos los eslóganes si existen
                if "eslogans" in resultado["contenido"]:
                    datos_eslogans = resultado["contenido"]["eslogans"].get(llm_nombre, {})
                    if datos_eslogans.get("exito"):
                        st.markdown(f"#### {t('eslogans_titulo')}")
                        container_eslogan = st.empty()
                        mostrar_con_efecto(datos_eslogans.get("respuesta", ""), container_eslogan, velocidad=0.01)
                        
                        if datos_eslogans.get("traduccion"):
                            st.markdown("---")
                            st.markdown(f"**{texto_traduccion}:**")
                            container_trad_eslogan = st.empty()
                            mostrar_con_efecto(datos_eslogans.get("traduccion", ""), container_trad_eslogan, velocidad=0.01)
                
                # Mostramos el email si existe
                if "email" in resultado["contenido"]:
                    datos_email = resultado["contenido"]["email"].get(llm_nombre, {})
                    if datos_email.get("exito"):
                        st.markdown(f"#### {t('email_titulo')}")
                        container_email = st.empty()
                        mostrar_con_efecto(datos_email.get("respuesta", ""), container_email, velocidad=0.01)
                        
                        if datos_email.get("traduccion"):
                            st.markdown("---")
                            st.markdown(f"**{texto_traduccion}:**")
                            container_trad_email = st.empty()
                            mostrar_con_efecto(datos_email.get("traduccion", ""), container_trad_email, velocidad=0.01)
                
                st.markdown("---")


def mostrar_resultados_normales(resultado, llm_usado_texto):
    """
    Esta función muestra los resultados cuando el usuario eligió una sola IA.
    Nuestro objetivo es presentar el contenido generado en pestañas organizadas:
    una para el post, otra para el email y otra para los eslóganes.
    """
    st.markdown(f"### Resultados generados por {llm_usado_texto}")
    
    texto_traduccion = t("traduccion_label")
    
    # Creamos tres pestañas para organizar el contenido
    tab1, tab2, tab3 = st.tabs([t("post_titulo"), t("email_titulo"), t("eslogans_titulo")])
    
    with tab1:
        if "post" in resultado["contenido"]:
            for modelo, datos in resultado["contenido"]["post"].items():
                if datos.get("exito"):
                    with st.expander(f"📝 {modelo}", expanded=True):
                        st.markdown("**🌐 Original:**")
                        st.write(datos["respuesta"])
                        if datos.get("traduccion"):
                            st.markdown("---")
                            st.markdown(f"**{texto_traduccion}:**")
                            st.write(datos["traduccion"])
                        st.caption(f"⏱️ {datos['tiempo_ms']} ms")
    
    with tab2:
        if "email" in resultado["contenido"]:
            for modelo, datos in resultado["contenido"]["email"].items():
                if datos.get("exito"):
                    with st.expander(f"📧 {modelo}", expanded=True):
                        st.markdown("**🌐 Original:**")
                        st.write(datos["respuesta"])
                        if datos.get("traduccion"):
                            st.markdown("---")
                            st.markdown(f"**{texto_traduccion}:**")
                            st.write(datos["traduccion"])
    
    with tab3:
        if "eslogans" in resultado["contenido"]:
            for modelo, datos in resultado["contenido"]["eslogans"].items():
                if datos.get("exito"):
                    with st.expander(f"💡 {modelo}", expanded=True):
                        st.markdown("**🌐 Original:**")
                        st.write(datos["respuesta"])
                        if datos.get("traduccion"):
                            st.markdown("---")
                            st.markdown(f"**{texto_traduccion}:**")
                            st.write(datos["traduccion"])
                        st.caption(f"⏱️ {datos['tiempo_ms']} ms")


# ==================== LÓGICA PRINCIPAL ====================
# Esta es la parte que se ejecuta cuando el usuario hace clic en el botón "Generar"
if generar:
    if not descripcion:
        # Si el usuario no escribió nada, mostramos un error
        st.error(t("error_producto"))
    else:
        # Preparamos el nombre del mercado sin los emojis para mostrarlo bonito
        mercado_nombre = mercado_seleccionado.replace("🇧🇷 ", "").replace("🇯🇵 ", "").replace("🇩🇪 ", "")
        
        # Texto del spinner (mensaje de carga) traducido
        spinner_text = t("spinner").format(mercado_nombre, llm_seleccionado)
        
        # Mostramos un spinner mientras esperamos la respuesta del servidor
        with st.spinner(spinner_text):
            try:
                # Llamamos a nuestra API (backend) para generar la campaña
                response = requests.post(
                    f"{API_URL}/generar",
                    json={
                        "descripcion_producto": descripcion,
                        "mercado": mercado,
                        "llm": llm,
                        "idioma_entrada": idioma_entrada
                    },
                    timeout=120  # Tiempo máximo de espera: 120 segundos
                )
                
                if response.status_code == 200:
                    resultado = response.json()
                    
                    if resultado.get("exito"):
                        # Todo salió bien, mostramos mensaje de éxito
                        st.success(f"{t('exito')} {mercado_nombre}!")
                        
                        # Mostramos los resultados según el modo elegido
                        if llm == "todos":
                            mostrar_comparacion(resultado, mercado_nombre)
                        else:
                            mostrar_resultados_normales(resultado, llm_seleccionado)
                    else:
                        st.error(f"❌ Error: {resultado.get('error')}")
                else:
                    st.error(f"❌ Error de conexión: {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                st.error(t("error_conexion"))
            except Exception as e:
                st.error(f"❌ Error inesperado: {str(e)}")


# ==================== PIE DE PÁGINA ====================
# Mostramos información adicional en el footer
st.markdown("---")
st.markdown(f'''
<div class="footer">
    {t("footer_empresa")}<br>
    🇧🇷 Brasil | 🇯🇵 Japón | 🇩🇪 Alemania<br>
    {t("footer_poten")}
</div>
''', unsafe_allow_html=True)
