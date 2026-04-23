# interfaz_polyglot.py - VERSIÓN CORREGIDA CON DEPURACIÓN
import streamlit as st
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import json

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


# ==================== FUNCIONES PRINCIPALES ====================

def llamar_api(descripcion, mercado, llm_usar):
    """Llama a tu API y devuelve el resultado crudo"""
    try:
        payload = {
            "descripcion_producto": descripcion,
            "mercado": mercado,
            "llm": llm_usar,
            "idioma_entrada": "es"
        }
        
        st.write(f"📤 Enviando a {llm_usar}...")  # Debug
        
        respuesta = requests.post(
            f"{API_URL}/generar",
            json=payload,
            timeout=60
        )
        
        if respuesta.status_code == 200:
            datos = respuesta.json()
            st.write(f"✅ {llm_usar} respondió OK")  # Debug
            return datos
        else:
            st.write(f"❌ {llm_usar} error HTTP {respuesta.status_code}")
            return {"exito": False, "error": f"HTTP {respuesta.status_code}"}
    except Exception as e:
        st.write(f"❌ {llm_usar} excepción: {str(e)[:50]}")
        return {"exito": False, "error": str(e)}

def generar_con_todos(descripcion, mercado):
    """Genera con los 3 LLMs en paralelo"""
    llms = ["gemini", "deepseek", "mistral"]
    resultados = {}
    
    # Barra de progreso
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
            status_text.text(f"Completado {completados}/{len(llms)}: {llm_actual}")
    
    progress_bar.empty()
    status_text.empty()
    return resultados

def extraer_y_mostrar_resultados(resultados_por_llm):
    """Toma los resultados crudos y los muestra en formato comparativo"""
    
    st.markdown("---")
    st.markdown("## 🏆 Comparación de Motores de IA")
    
    # Obtener los nombres de los LLMs que tienen datos
    llms_presentes = list(resultados_por_llm.keys())
    
    if not llms_presentes:
        st.error("No hay resultados para mostrar")
        return
    
    # Crear columnas dinámicamente
    cols = st.columns(len(llms_presentes))
    
    for idx, llm_nombre in enumerate(llms_presentes):
        with cols[idx]:
            resultado_llm = resultados_por_llm[llm_nombre]
            
            if resultado_llm.get("exito"):
                # Mostrar tarjeta del LLM
                st.markdown(f"""
                <div style="background:#d8e7f0; border-radius:16px; padding:1rem; border-left:4px solid #FFD700; margin-bottom:1rem;">
                    <div style="text-align:center; font-size:1.2rem; font-weight:600;">{llm_nombre.capitalize()}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Extraer contenido
                contenido = resultado_llm.get("contenido", {})
                
                # Mostrar POST
                st.markdown("#### 📱 Post")
                post_data = contenido.get("post", {})
                if post_data.get("exito"):
                    with st.expander("Ver Post", expanded=True):
                        st.markdown("**🌐 Original:**")
                        st.write(post_data.get("respuesta", "No hay texto"))
                        if post_data.get("traduccion"):
                            st.markdown("**🇪🇸 Traducción:**")
                            st.write(post_data.get("traduccion"))
                        st.caption(f"⏱️ {post_data.get('tiempo_ms', 0)} ms")
                else:
                    st.warning(f"Error en Post: {post_data.get('error', 'Desconocido')}")
                
                # Mostrar EMAIL
                st.markdown("#### 📧 Email")
                email_data = contenido.get("email", {})
                if email_data.get("exito"):
                    with st.expander("Ver Email", expanded=True):
                        st.write(email_data.get("respuesta", "No hay texto"))
                else:
                    st.warning(f"Error en Email: {email_data.get('error', 'Desconocido')}")
                
                # Mostrar ESLÓGANES
                st.markdown("#### 💡 Eslogans")
                eslogans_data = contenido.get("eslogans", {})
                if eslogans_data.get("exito"):
                    with st.expander("Ver Eslogans", expanded=True):
                        st.write(eslogans_data.get("respuesta", "No hay texto"))
                else:
                    st.warning(f"Error en Eslogans: {eslogans_data.get('error', 'Desconocido')}")
                
            else:
                st.error(f"❌ {llm_nombre.capitalize()} falló:\n{resultado_llm.get('error', 'Error desconocido')}")

def generar_un_solo_llm(descripcion, mercado, llm):
    """Genera con un solo LLM y muestra resultados"""
    
    with st.spinner(f"Generando con {llm}..."):
        resultado = llamar_api(descripcion, mercado, llm)
    
    if resultado.get("exito"):
        st.success(f"✅ ¡Contenido generado exitosamente!")
        
        contenido = resultado.get("contenido", {})
        
        # Pestañas para organizar
        tab1, tab2, tab3 = st.tabs(["📱 Post", "📧 Email", "💡 Eslogans"])
        
        with tab1:
            post_data = contenido.get("post", {})
            if post_data.get("exito"):
                st.markdown("**🌐 Original:**")
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
        
        st.info(f"🎯 Generando para: **{mercado_nombre}** | 🤖 Usando: **{llm_seleccionado}**")
        
        try:
            if llm == "todos":
                # Modo comparación: 3 LLMs en paralelo
                resultados = generar_con_todos(descripcion, mercado)
                extraer_y_mostrar_resultados(resultados)
            else:
                # Modo normal: 1 LLM
                generar_un_solo_llm(descripcion, mercado, llm)
                
        except requests.exceptions.ConnectionError:
            st.error("❌ No se pudo conectar al servidor. ¿El backend está corriendo?")
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
