# -*- coding: utf-8 -*-
"""
interfaz_polyglot.py - Interfaz de Usuario Polyglot (Bilingüe)
"""

import streamlit as st
import requests
import time

# ==================== CONFIGURACIÓN ====================
API_URL = "https://polyglot-app-5crh.onrender.com"

st.set_page_config(
    page_title="Global-Gadgets | Polyglot",
    page_icon="🌍",
    layout="wide"
)

# ==================== ESTILOS CSS ====================
st.markdown("""
<style>
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
        color: #666;
        margin-bottom: 2rem;
    }
    .product-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 0.5rem;
        border-radius: 20px;
        border: 1px solid #333;
        margin-bottom: 0.5rem;
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 0.5rem;
        color: #888;
        font-size: 0.8rem;
        border-top: 0.5px solid #444;
    }
    .stButton > button {
        background: linear-gradient(90deg, #1a6b8a, #2a9d6e);
        color: white;
        font-weight: bold;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 30px;
        transition: transform 0.2s;
    }
    .stButton > button:hover {
        transform: scale(1.02);
    }
    div[role="radiogroup"] label {
        margin: 5px 0;
        padding: 8px 12px;
        border-radius: 10px;
        transition: all 0.2s ease;
        cursor: pointer;
    }
    div[role="radiogroup"] label:hover {
        background-color: #d8e7f0 !important;
        transform: translateX(4px);
    }
    div[role="radiogroup"] label[data-baseweb="radio"]:has(input:checked) {
        background-color: #d8e7f0 !important;
        font-weight: 500;
        border-left: 3px solid #FFD700;
    }
</style>
""", unsafe_allow_html=True)


# ==================== FUNCIÓN EFECTO MÁQUINA DE ESCRIBIR ====================
def mostrar_con_efecto(texto, placeholder, velocidad=0.01):
    """Muestra el texto caracter por caracter (efecto máquina de escribir)"""
    texto_mostrado = ""
    for char in texto:
        texto_mostrado += char
        placeholder.markdown(texto_mostrado + "▌")
        time.sleep(velocidad)
    placeholder.markdown(texto_mostrado)


# ==================== INICIALIZAR IDIOMA ====================
if "idioma" not in st.session_state:
    st.session_state.idioma = "es"  # español por defecto


# ==================== TEXTO BILINGÜE ====================
def t(clave):
    """Retorna el texto en el idioma seleccionado"""
    textos = {
        # Header
        "titulo": {"es": "🌍 Polyglot", "en": "🌍 Polyglot"},
        "empresa": {"es": "⚡ Global-Gadgets ⚡", "en": "⚡ Global-Gadgets ⚡"},
        "subtitulo": {"es": "Convierte tu producto en ventas globales 🏆<br>Campaña de Marketing para Brasil | Japón | Alemania", 
                      "en": "Turn your product into global sales 🏆<br>Marketing Campaign for Brazil | Japan | Germany"},
        
        # Selector de idioma
        "idioma_titulo": {"es": "🌐 Idioma", "en": "🌐 Language"},
        "idioma_pregunta": {"es": "Selecciona el idioma", "en": "Select the language"},
        
        # Producto
        "producto_titulo": {"es": "📦 ¿Qué producto quieres vender al mundo?", 
                           "en": "📦 What product do you want to sell to the world?"},
        "producto_placeholder": {"es": "Ej: Auriculares con cancelación de ruido, 40h de batería",
                                "en": "Ex: Noise-cancelling headphones, 40h battery"},
        
        # Mercado
        "mercado_titulo": {"es": "🎯 Mercado objetivo", "en": "🎯 Target market"},
        "mercado_desc": {"es": "Selecciona el país para la campaña", "en": "Select the country for the campaign"},
        
        # Motor IA
        "motor_titulo": {"es": "🤖 Motor de generación", "en": "🤖 Generation engine"},
        "motor_desc": {"es": "Selecciona qué IA generará tu contenido", "en": "Select which AI will generate your content"},
        
        # Botón
        "boton": {"es": "✨ Generar campaña internacional ✨", "en": "✨ Generate international campaign ✨"},
        
        # Resultados
        "comparacion_titulo": {"es": "🏆 Comparación de Motores de IA", "en": "🏆 AI Engines Comparison"},
        "post_titulo": {"es": "📱 Post para Redes Sociales", "en": "📱 Social Media Post"},
        "eslogans_titulo": {"es": "💡 Eslogans Publicitarios", "en": "💡 Advertising Slogans"},
        "email_titulo": {"es": "📧 Email Promocional", "en": "📧 Promotional Email"},
        "traduccion_label": {"es": "🇪🇸 Traducción al español", "en": "🇬🇧 English translation"},
        
        # Errores
        "error_producto": {"es": "❌ Por favor, describe tu producto para empezar", 
                          "en": "❌ Please describe your product to start"},
        "error_conexion": {"es": "❌ No se pudo conectar al servidor", 
                          "en": "❌ Could not connect to server"},
        "exito": {"es": "✅ ¡Campaña generada exitosamente para ", 
                 "en": "✅ Campaign successfully generated for "},
        
        # Footer
        "footer_empresa": {"es": "🌍 <strong>Global-Gadgets</strong> - Polyglot Marketing Multilingüe",
                          "en": "🌍 <strong>Global-Gadgets</strong> - Polyglot Multilingual Marketing"},
        "footer_poten": {"es": "Potenciado por Gemini | Deepseek | Mistral",
                        "en": "Powered by Gemini | Deepseek | Mistral"},
    }
    return textos.get(clave, {}).get(st.session_state.idioma, textos.get(clave, {}).get("es", clave))


# ==================== HEADER ====================
st.markdown(f'<p class="main-title">{t("titulo")}</p>', unsafe_allow_html=True)
st.markdown(f'<p class="company-name">{t("empresa")}</p>', unsafe_allow_html=True)
st.markdown(f'<p class="subtitle">{t("subtitulo")}</p>', unsafe_allow_html=True)


# ==================== SELECTOR DE IDIOMA ÚNICO ====================
st.markdown("---")
st.markdown(f"### {t('idioma_titulo')}")
st.markdown(t("idioma_pregunta"))

col_lang1, col_lang2, col_lang3, col_lang4, col_lang5 = st.columns([1, 1, 1, 1, 1])
with col_lang2:
    if st.button("🇪🇸 Español", key="btn_es", use_container_width=True):
        st.session_state.idioma = "es"
        st.rerun()
with col_lang3:
    if st.button("🇬🇧 English", key="btn_en", use_container_width=True):
        st.session_state.idioma = "en"
        st.rerun()

st.markdown("---")


# ==================== IDIOMA DE ENTRADA DEL PRODUCTO (mismo que interfaz) ====================
# El idioma de entrada del producto es el mismo que seleccionó el usuario
idioma_entrada = "es" if st.session_state.idioma == "es" else "en"


# ==================== ENTRADA DEL PRODUCTO ====================
with st.container():
    st.markdown('<div class="product-card">', unsafe_allow_html=True)
    st.markdown(f"### {t('producto_titulo')}")
    descripcion = st.text_area(
        "Descripción del producto",
        placeholder=t("producto_placeholder"),
        height=80,
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)


# ==================== CONFIGURACIÓN EN COLUMNAS ====================
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"### {t('mercado_titulo')}")
    st.markdown(t("mercado_desc"))
    
    mercado_opciones = {
        "🇧🇷 Brasil": "brasil",
        "🇯🇵 Japón": "japon",
        "🇩🇪 Alemania": "alemania"
    }
    
    mercado_seleccionado = st.radio(
        "Mercado",
        options=list(mercado_opciones.keys()),
        index=0,
        label_visibility="collapsed"
    )
    mercado = mercado_opciones[mercado_seleccionado]

with col2:
    st.markdown(f"### {t('motor_titulo')}")
    st.markdown(t("motor_desc"))
    
    llm_opciones = {
        "Gemini (Google)": "gemini",
        "Deepseek (DeepSeek)": "deepseek",
        "Mistral (Mistral AI)": "mistral",
        "Todos (Comparar)": "todos"
    }
    
    llm_seleccionado = st.radio(
        "LLM",
        options=list(llm_opciones.keys()),
        index=0,
        label_visibility="collapsed"
    )
    llm = llm_opciones[llm_seleccionado]


# ==================== BOTÓN DE GENERACIÓN ====================
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    generar = st.button(t("boton"), type="primary", use_container_width=True)


# ==================== FUNCIONES DE VISUALIZACIÓN ====================
def mostrar_comparacion(resultado, mercado_nombre):
    st.markdown("---")
    st.markdown(f"## {t('comparacion_titulo')}")
    
    if "post" not in resultado["contenido"]:
        st.warning("No hay datos de post para comparar")
        return
    
    posts = resultado["contenido"]["post"]
    
    color_fondo = "#d8e7f0"
    color_borde = "#FFD700"
    color_texto = "#1a1a2e"
    
    # Texto de traducción según idioma seleccionado
    texto_traduccion = t("traduccion_label")
    
    col1, col2, col3 = st.columns(3)
    llms_orden = ["Deepseek", "Mistral", "Gemini"]
    
    for idx, llm_nombre in enumerate(llms_orden):
        with [col1, col2, col3][idx]:
            datos_post = posts.get(llm_nombre, {})
            
            if datos_post.get("exito"):
                st.markdown(f"""
                <div style="background: {color_fondo}; border-radius: 16px; padding: 1rem; margin: 0.5rem 0; border-left: 4px solid {color_borde};">
                    <div style="text-align: center; font-size: 1.2rem; font-weight: 600; color: {color_texto};">{llm_nombre}</div>
                    <div style="text-align: center; font-size: 0.8rem; color: #555;">⏱️ {datos_post.get("tiempo_ms", 0)} ms</div>
                </div>
                """, unsafe_allow_html=True)
                
                # POST
                respuesta_post = datos_post.get("respuesta", "")
                traduccion_post = datos_post.get("traduccion", "")
                
                st.markdown(f"#### {t('post_titulo')}")
                container_post = st.empty()
                mostrar_con_efecto(respuesta_post, container_post, velocidad=0.01)
                
                if traduccion_post:
                    st.markdown("---")
                    st.markdown(f"**{texto_traduccion}:**")
                    container_trad = st.empty()
                    mostrar_con_efecto(traduccion_post, container_trad, velocidad=0.01)
                
                # ESLÓGANES
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
                
                # EMAIL
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
    st.markdown(f"### Resultados generados por {llm_usado_texto}")
    
    # Texto de traducción según idioma seleccionado
    texto_traduccion = t("traduccion_label")
    
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
if generar:
    if not descripcion:
        st.error(t("error_producto"))
    else:
        mercado_nombre = mercado_seleccionado.replace("🇧🇷 ", "").replace("🇯🇵 ", "").replace("🇩🇪 ", "")
        
        with st.spinner(f"🚀 Generando contenido para {mercado_nombre} con {llm_seleccionado}..."):
            try:
                response = requests.post(
                    f"{API_URL}/generar",
                    json={
                        "descripcion_producto": descripcion,
                        "mercado": mercado,
                        "llm": llm,
                        "idioma_entrada": idioma_entrada
                    },
                    timeout=120
                )
                
                if response.status_code == 200:
                    resultado = response.json()
                    
                    if resultado.get("exito"):
                        st.success(f"{t('exito')} {mercado_nombre}!")
                        
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
st.markdown("---")
st.markdown(f'''
<div class="footer">
    {t("footer_empresa")}<br>
    🇧🇷 Brasil | 🇯🇵 Japón | 🇩🇪 Alemania<br>
    {t("footer_poten")}
</div>
''', unsafe_allow_html=True)
