# interfaz_polyglot.py - VERSIÓN WEB CON HILOS
import streamlit as st
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# ==================== CONFIGURACIÓN ====================
# IMPORTANTE: Esta URL debe ser la de tu backend en RENDER
API_URL = "https://polyglot-app-5crh.onrender.com"  # ← TU URL DE RENDER

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
    }
    .stButton > button:hover {
        transform: scale(1.02);
        background: linear-gradient(90deg, #1e7a9e, #35b87a);
    }
    div[role="radiogroup"] label:hover {
        background-color: #d8e7f0 !important;
        transform: translateX(4px);
    }
    div[role="radiogroup"] label[data-baseweb="radio"]:has(input:checked) {
        background-color: #d8e7f0 !important;
        border-left: 3px solid #FFD700;
    }
</style>
""", unsafe_allow_html=True)

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

# ==================== BOTÓN ====================
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    generar = st.button("✨ Generar campaña internacional ✨", type="primary", use_container_width=True)


# ==================== FUNCIONES CON HILOS ====================

def llamar_api(descripcion, mercado, llm_usar):
    """Llama a tu API en Render"""
    try:
        payload = {
            "descripcion_producto": descripcion,
            "mercado": mercado,
            "llm": llm_usar,
            "idioma_entrada": "es"
        }
        
        respuesta = requests.post(
            f"{API_URL}/generar",
            json=payload,
            timeout=60
        )
        
        if respuesta.status_code == 200:
            return respuesta.json()
        else:
            return {"exito": False, "error": f"HTTP {respuesta.status_code}"}
    except Exception as e:
        return {"exito": False, "error": str(e)}

def generar_con_todos(descripcion, mercado):
    """Genera con los 3 LLMs en paralelo"""
    llms = ["gemini", "deepseek", "mistral"]
    resultados = {}
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        futuros = {}
        for i, llm_actual in enumerate(llms):
            futuro = executor.submit(llamar_api, descripcion, mercado, llm_actual)
            futuros[futuro] = llm_actual
        
        completados = 0
        for futuro in as_completed(futuros):
            llm_actual = futuros[futuro]
            try:
                resultado = futuro.result(timeout=70)
                resultados[llm_actual] = resultado
            except Exception as e:
                resultados[llm_actual] = {"exito": False, "error": str(e)}
            
            completados += 1
            progress_bar.progress(completados / len(llms))
            status_text.text(f"✅ {llm_actual.capitalize()} listo ({completados}/{len(llms)})")
    
    progress_bar.empty()
    status_text.empty()
    return resultados

def mostrar_comparacion(resultados_por_llm):
    """Muestra resultados de los 3 LLMs"""
    st.markdown("---")
    st.markdown("## 🏆 Comparación de Motores de IA")
    
    llms_presentes = list(resultados_por_llm.keys())
    cols = st.columns(len(llms_presentes))
    
    for idx, llm_nombre in enumerate(llms_presentes):
        with cols[idx]:
            resultado_llm = resultados_por_llm[llm_nombre]
            
            if resultado_llm.get("exito"):
                st.markdown(f"""
                <div style="background:#d8e7f0; border-radius:16px; padding:1rem; border-left:4px solid #FFD700; margin-bottom:1rem;">
                    <div style="text-align:center; font-size:1.2rem; font-weight:600;">{llm_nombre.capitalize()}</div>
                </div>
                """, unsafe_allow_html=True)
                
                contenido = resultado_llm.get("contenido", {})
                
                # Post
                st.markdown("#### 📱 Post")
                post_data = contenido.get("post", {})
                if post_data.get("exito"):
                    with st.expander("Ver Post", expanded=True):
                        st.write(post_data.get("respuesta", ""))
                        if post_data.get("traduccion"):
                            st.markdown("---")
                            st.markdown("**🇪🇸 Traducción:**")
                            st.write(post_data.get("traduccion"))
                        st.caption(f"⏱️ {post_data.get('tiempo_ms', 0)} ms")
                else:
                    st.warning("Error en Post")
                
                # Email
                st.markdown("#### 📧 Email")
                email_data = contenido.get("email", {})
                if email_data.get("exito"):
                    with st.expander("Ver Email", expanded=True):
                        st.write(email_data.get("respuesta", ""))
                else:
                    st.warning("Error en Email")
                
                # Eslogans
                st.markdown("#### 💡 Eslogans")
                eslogans_data = contenido.get("eslogans", {})
                if eslogans_data.get("exito"):
                    with st.expander("Ver Eslogans", expanded=True):
                        st.write(eslogans_data.get("respuesta", ""))
                else:
                    st.warning("Error en Eslogans")
            else:
                st.error(f"❌ {llm_nombre.capitalize()} falló")

def mostrar_un_llm(resultado, llm_nombre):
    """Muestra resultados de un solo LLM"""
    if resultado.get("exito"):
        st.success(f"✅ ¡Contenido generado con {llm_nombre}!")
        
        contenido = resultado.get("contenido", {})
        tab1, tab2, tab3 = st.tabs(["📱 Post", "📧 Email", "💡 Eslogans"])
        
        with tab1:
            post_data = contenido.get("post", {})
            if post_data.get("exito"):
                st.write(post_data.get("respuesta", ""))
                if post_data.get("traduccion"):
                    st.markdown("---")
                    st.markdown("**🇪🇸 Traducción:**")
                    st.write(post_data.get("traduccion"))
                st.caption(f"⏱️ {post_data.get('tiempo_ms', 0)} ms")
            else:
                st.error(f"Error: {post_data.get('error', 'Desconocido')}")
        
        with tab2:
            email_data = contenido.get("email", {})
            if email_data.get("exito"):
                st.write(email_data.get("respuesta", ""))
            else:
                st.error(f"Error: {email_data.get('error', 'Desconocido')}")
        
        with tab3:
            eslogans_data = contenido.get("eslogans", {})
            if eslogans_data.get("exito"):
                st.write(eslogans_data.get("respuesta", ""))
            else:
                st.error(f"Error: {eslogans_data.get('error', 'Desconocido')}")
    else:
        st.error(f"❌ Error: {resultado.get('error', 'Desconocido')}")


# ==================== LÓGICA PRINCIPAL ====================
if generar:
    if not descripcion:
        st.error("❌ Por favor, describe tu producto")
    else:
        mercado_nombre = mercado_seleccionado.replace("🇧🇷 ", "").replace("🇯🇵 ", "").replace("🇩🇪 ", "")
        
        with st.spinner(f"🚀 Generando campaña para {mercado_nombre}..."):
            try:
                if llm == "todos":
                    resultados = generar_con_todos(descripcion, mercado)
                    mostrar_comparacion(resultados)
                else:
                    resultado = llamar_api(descripcion, mercado, llm)
                    mostrar_un_llm(resultado, llm_seleccionado)
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ No se pudo conectar al servidor en Render")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# ==================== PIE DE PÁGINA ====================
st.markdown("---")
st.markdown(f'''
<div class="footer">
    🌍 <strong>Global-Gadgets</strong> - Polyglot Marketing Multilingüe<br>
    🇧🇷 Brasil | 🇯🇵 Japón | 🇩🇪 Alemania<br>
    Potenciado por Gemini | Deepseek | Mistral
</div>
''', unsafe_allow_html=True)
