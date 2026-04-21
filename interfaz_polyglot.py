# -*- coding: utf-8 -*-
"""
interfaz_polyglot.py - Interfaz de Usuario Polyglot
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


# ==================== HEADER ====================
st.markdown('<p class="main-title">🌍 Polyglot</p>', unsafe_allow_html=True)
st.markdown('<p class="company-name">⚡ Global-Gadgets ⚡</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Convierte tu producto en ventas globales 🏆<br>Campaña de Marketing para Brasil | Japón | Alemania</p>', unsafe_allow_html=True)


# ==================== ENTRADA DEL PRODUCTO ====================
with st.container():
    st.markdown('<div class="product-card">', unsafe_allow_html=True)
    st.markdown("### 📦 ¿Qué producto quieres vender al mundo?")
    descripcion = st.text_area(
        "Descripción del producto",
        placeholder="Ej: Auriculares con cancelación de ruido, 40h de batería",
        height=80,
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)


# ==================== CONFIGURACIÓN ====================
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🎯 Mercado objetivo")
    st.markdown("Selecciona el país para la campaña")
    
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
    st.markdown("### 🤖 Motor de generación")
    st.markdown("Selecciona qué IA generará tu contenido")
    
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


# ==================== IDIOMA DE ENTRADA ====================
st.markdown("---")
st.markdown("### 🌐 Idioma de entrada")

col_idioma1, col_idioma2, col_idioma3 = st.columns([1, 2, 1])
with col_idioma2:
    idioma_entrada_opcion = st.radio(
        "¿En qué idioma describes tu producto?",
        ["Español", "Inglés"],
        index=0,
        horizontal=True
    )
    idioma_map = {"Español": "es", "Inglés": "en"}
    idioma_entrada = idioma_map[idioma_entrada_opcion]


# ==================== BOTÓN DE GENERACIÓN ====================
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    generar = st.button("✨ Generar campaña internacional ✨", type="primary", use_container_width=True)


# ==================== FUNCIONES DE VISUALIZACIÓN ====================
def mostrar_comparacion(resultado, mercado_nombre):
    st.markdown("---")
    st.markdown("## 🏆 Comparación de Motores de IA")
    
    if "post" not in resultado["contenido"]:
        st.warning("No hay datos de post para comparar")
        return
    
    posts = resultado["contenido"]["post"]
    
    color_fondo = "#d8e7f0"
    color_borde = "#FFD700"
    color_texto = "#1a1a2e"
    
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
                
                st.markdown("#### 📱 Post para Redes Sociales")
                container_post = st.empty()
                mostrar_con_efecto(respuesta_post, container_post, velocidad=0.01)
                
                if traduccion_post:
                    st.markdown("---")
                    st.markdown("**🇪🇸 Traducción al español:**")
                    container_trad = st.empty()
                    mostrar_con_efecto(traduccion_post, container_trad, velocidad=0.01)
                
                # ESLÓGANES
                if "eslogans" in resultado["contenido"]:
                    datos_eslogans = resultado["contenido"]["eslogans"].get(llm_nombre, {})
                    if datos_eslogans.get("exito"):
                        st.markdown("#### 💡 Eslogans Publicitarios")
                        container_eslogan = st.empty()
                        mostrar_con_efecto(datos_eslogans.get("respuesta", ""), container_eslogan, velocidad=0.01)
                        
                        if datos_eslogans.get("traduccion"):
                            st.markdown("---")
                            st.markdown("**🇪🇸 Traducción al español:**")
                            container_trad_eslogan = st.empty()
                            mostrar_con_efecto(datos_eslogans.get("traduccion", ""), container_trad_eslogan, velocidad=0.01)
                
                # EMAIL
                if "email" in resultado["contenido"]:
                    datos_email = resultado["contenido"]["email"].get(llm_nombre, {})
                    if datos_email.get("exito"):
                        st.markdown("#### 📧 Email Promocional")
                        container_email = st.empty()
                        mostrar_con_efecto(datos_email.get("respuesta", ""), container_email, velocidad=0.01)
                        
                        if datos_email.get("traduccion"):
                            st.markdown("---")
                            st.markdown("**🇪🇸 Traducción al español:**")
                            container_trad_email = st.empty()
                            mostrar_con_efecto(datos_email.get("traduccion", ""), container_trad_email, velocidad=0.01)
                
                st.markdown("---")


def mostrar_resultados_normales(resultado, llm_usado_texto):
    st.markdown(f"### Resultados generados por {llm_usado_texto}")
    
    tab1, tab2, tab3 = st.tabs(["📱 Redes Sociales", "📧 Email Promocional", "🎯 Eslogans"])
    
    with tab1:
        if "post" in resultado["contenido"]:
            for modelo, datos in resultado["contenido"]["post"].items():
                if datos.get("exito"):
                    with st.expander(f"📝 {modelo}", expanded=True):
                        st.markdown("**🌐 Original:**")
                        st.write(datos["respuesta"])
                        if datos.get("traduccion"):
                            st.markdown("---")
                            st.markdown("**🇪🇸 Traducción al español:**")
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
                            st.markdown("**🇪🇸 Traducción al español:**")
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
                            st.markdown("**🇪🇸 Traducción al español:**")
                            st.write(datos["traduccion"])
                        st.caption(f"⏱️ {datos['tiempo_ms']} ms")


# ==================== LÓGICA PRINCIPAL ====================
if generar:
    if not descripcion:
        st.error("❌ Por favor, describe tu producto para empezar")
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
                        st.success(f"✅ ¡Campaña generada exitosamente para {mercado_nombre}!")
                        
                        if llm == "todos":
                            mostrar_comparacion(resultado, mercado_nombre)
                        else:
                            mostrar_resultados_normales(resultado, llm_seleccionado)
                    else:
                        st.error(f"❌ Error: {resultado.get('error')}")
                else:
                    st.error(f"❌ Error de conexión: {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ No se pudo conectar al servidor")
            except Exception as e:
                st.error(f"❌ Error inesperado: {str(e)}")


# ==================== PIE DE PÁGINA ====================
st.markdown("---")
st.markdown(f'''
<div class="footer">
    🌍 <strong>Global-Gadgets</strong> - Polyglot Marketing Multilingüe<br>
    🇧🇷 Brasil | 🇯🇵 Japón | 🇩🇪 Alemania<br>
    Potenciado por Gemini | Deepseek | Mistral
</div>
''', unsafe_allow_html=True)
