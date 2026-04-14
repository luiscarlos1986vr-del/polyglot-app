# interfaz_polyglot.py - VERSIÓN PROFESIONAL SIMPLIFICADA
# Requisito 4: Comparación y selección entre LLMs

import streamlit as st
import requests

# ==================== CONFIGURACIÓN ====================
API_URL = "https://polyglot-app-5crh.onrender.com"

st.set_page_config(
    page_title="Global-Gadgets | Polyglot",
    page_icon="🌍",
    layout="wide"
)

# ==================== ESTILOS CSS PERSONALIZADOS ====================
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
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    .stButton > button:hover {
        transform: scale(1.02);
        background: linear-gradient(90deg, #1e7a9e, #35b87a);
        color: white;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    div[role="radiogroup"] label {
        padding: 6px 0;
        font-size: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ==================== HEADER ====================
st.markdown('<p class="main-title">🌍 Polyglot</p>', unsafe_allow_html=True)
st.markdown('<p class="company-name">⚡ Global-Gadgets ⚡</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Convierte tu producto en ventas globales 🏆<br>Campaña de Marketing para Japón | Alemania | Brasil</p>', unsafe_allow_html=True)

# ==================== ENTRADA DEL PRODUCTO ====================
with st.container():
    st.markdown('<div class="product-card">', unsafe_allow_html=True)
    st.markdown("### 📦 ¿Qué producto quieres vender al mundo?")
    descripcion = st.text_area(
        "",
        placeholder="Ej: Auriculares con cancelación de ruido, 40h de batería",
        height=80,
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== CONFIGURACIÓN EN COLUMNAS ====================
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🎯 Mercado objetivo")
    st.markdown("Selecciona el país para la campaña")
    mercado_opciones = {
        "Brasil": "brasil",
        "Japón": "japon",
        "Alemania": "alemania"
    }
    mercado_seleccionado = st.radio(
        "Mercado",
        options=list(mercado_opciones.keys()),
        index=1,
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

# ==================== BOTÓN DE GENERACIÓN ====================
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    generar = st.button("✨ Generar campaña internacional ✨", type="primary", use_container_width=True)

# ==================== FUNCIONES DE VISUALIZACIÓN ====================

def mostrar_comparacion(resultado, mercado_nombre):
    """Muestra los resultados de los 3 LLMs para comparar y seleccionar"""

    st.markdown("---")
    st.markdown("## 🏆 Comparación de Motores de IA")
    st.markdown("Revisa el contenido completo de cada motor y selecciona el mejor")

    contenido = resultado.get("contenido", {})
    llms_orden = ["Deepseek", "Mistral", "Gemini"]
    #llm_iconos = {"Deepseek": "🔍", "Mistral": "🌊", "Gemini": "🤖"}
    colores = {"Deepseek": "#00C9FF", "Mistral": "#FF6B6B", "Gemini": "#92FE9D"}

    # --- Resumen lado a lado (vista rápida) ---
    st.markdown("### 📊 Vista rápida")
    cols = st.columns(3)

    for idx, llm_nombre in enumerate(llms_orden):
        with cols[idx]:
            color = colores.get(llm_nombre, "#00C9FF")

            post_datos = contenido.get("post", {}).get(llm_nombre, {})
            tiempo = post_datos.get("tiempo_ms", "—")
            exito = post_datos.get("exito", False)

            # Tarjeta sutil con gradiente tipo botón (teal/verde)
            st.markdown(f'''
            <div style="background: linear-gradient(100deg, #1a6b8a, #2a9d6e);
                        border-radius: 16px; padding: 1.2rem;
                        border: 1px solid rgba(255,255,255,0.1);
                        text-align: center; margin-bottom: 0.5rem;">
                <div style="font-size: 1.3rem; font-weight: bold; color: white;
                            margin-bottom: 0.3rem;">{llm_nombre}</div>
                <div style="font-size: 0.8rem; color: rgba(255,255,255,0.7);">
                    ⏱️ {tiempo} ms
                </div>
            </div>
            ''', unsafe_allow_html=True)

            if exito:
                with st.expander("📱 Post", expanded=False):
                    st.write(post_datos.get("respuesta", ""))

                email_datos = contenido.get("email", {}).get(llm_nombre, {})
                if email_datos.get("exito"):
                    with st.expander("📧 Email", expanded=False):
                        st.write(email_datos.get("respuesta", ""))

                eslogan_datos = contenido.get("eslogans", {}).get(llm_nombre, {})
                if eslogan_datos.get("exito"):
                    with st.expander("🎯 Eslogans", expanded=False):
                        st.write(eslogan_datos.get("respuesta", ""))
            else:
                st.error(f"❌ {post_datos.get('error', 'Error desconocido')}")

    

def mostrar_resultados_normales(resultado, llm_nombre):
    """Muestra los resultados en pestañas (modo normal)"""
    st.markdown(f"### Resultados generados por {llm_nombre}")

    tab1, tab2, tab3 = st.tabs(["📱 Redes Sociales", "📧 Email Promocional", "🎯 Eslogans"])

    with tab1:
        if "post" in resultado["contenido"]:
            for modelo, datos in resultado["contenido"]["post"].items():
                if datos.get("exito"):
                    with st.expander(f"📝 {modelo}", expanded=True):
                        st.write(datos["respuesta"])
                        st.caption(f"⏱️ {datos['tiempo_ms']} ms")

    with tab2:
        if "email" in resultado["contenido"]:
            for modelo, datos in resultado["contenido"]["email"].items():
                if datos.get("exito"):
                    with st.expander(f"📧 {modelo}"):
                        st.write(datos["respuesta"])

    with tab3:
        if "eslogans" in resultado["contenido"]:
            for modelo, datos in resultado["contenido"]["eslogans"].items():
                if datos.get("exito"):
                    with st.expander(f"💡 {modelo}"):
                        st.write(datos["respuesta"])

# ==================== LÓGICA PRINCIPAL ====================
if generar:
    if not descripcion:
        st.error("❌ Por favor, describe tu producto para empezar")
    else:
        with st.spinner(f"🚀 Generando contenido para {mercado_seleccionado} con {llm_seleccionado}..."):
            try:
                response = requests.post(
                    f"{API_URL}/generar",
                    json={
                        "descripcion_producto": descripcion,
                        "mercado": mercado,
                        "llm": llm
                    },
                    timeout=120
                )

                if response.status_code == 200:
                    resultado = response.json()

                    if resultado.get("exito"):
                        st.success(f"✅ ¡Campaña generada exitosamente para {mercado_seleccionado}!")

                        if llm == "todos":
                            mostrar_comparacion(resultado, mercado_seleccionado)
                        else:
                            mostrar_resultados_normales(resultado, llm_seleccionado)
                    else:
                        st.error(f"❌ Error: {resultado.get('error')}")
                else:
                    st.error(f"❌ Error de conexión: {response.status_code}")

            except requests.exceptions.ConnectionError:
                st.error("❌ No se pudo conectar al servidor. Asegúrate de que el backend esté corriendo.")
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
