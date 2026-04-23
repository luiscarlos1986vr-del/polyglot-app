# interfaz_polyglot.py - VERSIÓN DEFINITIVA PARA WEB
# Funciona con Render (backend) y Streamlit Cloud (frontend)
# Incluye: Hilos para velocidad, selector de idioma, timeout 120s

import streamlit as st
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from functools import lru_cache
import hashlib

# ==================== CONFIGURACIÓN ====================
# IMPORTANTE: Esta es la URL de tu backend en RENDER
API_URL = "https://polyglot-app-5crh.onrender.com"

# Timeout de 120 segundos para dar tiempo a Render (plan gratuito) a despertar
REQUEST_TIMEOUT = 120

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

# ==================== CONFIGURACIÓN EN TRES COLUMNAS ====================
col1, col2, col3 = st.columns(3)

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

with col3:
    st.markdown("### 🌐 Idioma de entrada")
    st.markdown("¿En qué idioma escribiste tu producto?")
    idioma_opciones = {
        "🇪🇸 Español": "es",
        "🇬🇧 English": "en"
    }
    idioma_seleccionado = st.radio(
        "Idioma",
        options=list(idioma_opciones.keys()),
        index=0,
        label_visibility="collapsed"
    )
    idioma = idioma_opciones[idioma_seleccionado]

# ==================== BOTÓN ====================
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    generar = st.button("✨ Generar campaña internacional ✨", type="primary", use_container_width=True)


# ==================== CACHÉ PARA RESPUESTAS RÁPIDAS ====================
# Esto guarda resultados ya generados para que la segunda vez sea instantáneo
@lru_cache(maxsize=50)
def generar_hash(descripcion, mercado, llm, idioma):
    """Crea un hash único para cada combinación de parámetros"""
    texto = f"{descripcion}_{mercado}_{llm}_{idioma}"
    return hashlib.md5(texto.encode()).hexdigest()

# Diccionario manual para caché (más confiable en Streamlit Cloud)
CACHE_RESULTADOS = {}

def obtener_o_generar(descripcion, mercado, llm_usar, idioma, fuerza_generar=False):
    """Obtiene resultado del caché o lo genera nuevo"""
    clave = f"{descripcion}_{mercado}_{llm_usar}_{idioma}"
    
    if not fuerza_generar and clave in CACHE_RESULTADOS:
        st.caption("⚡ Resultado obtenido del caché (respuesta instantánea)")
        return CACHE_RESULTADOS[clave]
    
    resultado = llamar_api(descripcion, mercado, llm_usar, idioma)
    CACHE_RESULTADOS[clave] = resultado
    return resultado


# ==================== FUNCIONES PRINCIPALES ====================

def llamar_api(descripcion, mercado, llm_usar, idioma):
    """
    Llama a tu API en Render con timeout de 120 segundos
    """
    try:
        payload = {
            "descripcion_producto": descripcion,
            "mercado": mercado,
            "llm": llm_usar,
            "idioma_entrada": idioma
        }
        
        respuesta = requests.post(
            f"{API_URL}/generar",
            json=payload,
            timeout=REQUEST_TIMEOUT
        )
        
        if respuesta.status_code == 200:
            return respuesta.json()
        else:
            return {"exito": False, "error": f"HTTP {respuesta.status_code}: {respuesta.text[:100]}"}
    except requests.exceptions.Timeout:
        return {"exito": False, "error": f"⏰ El servidor tardó más de {REQUEST_TIMEOUT} segundos. Intenta nuevamente."}
    except requests.exceptions.ConnectionError:
        return {"exito": False, "error": "❌ No se pudo conectar al servidor. ¿El backend está corriendo?"}
    except Exception as e:
        return {"exito": False, "error": str(e)}

def generar_con_todos(descripcion, mercado, idioma):
    """
    Genera con los 3 LLMs en paralelo usando hilos
    """
    llms = ["gemini", "deepseek", "mistral"]
    resultados = {}
    
    # Barra de progreso
    progress_bar = st.progress(0)
    status_text = st.empty()
    status_text.info("🚀 Lanzando 3 motores de IA en paralelo...")
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        futuros = {}
        for i, llm_actual in enumerate(llms):
            futuro = executor.submit(obtener_o_generar, descripcion, mercado, llm_actual, idioma, False)
            futuros[futuro] = llm_actual
        
        completados = 0
        for futuro in as_completed(futuros):
            llm_actual = futuros[futuro]
            try:
                resultado = futuro.result(timeout=REQUEST_TIMEOUT + 10)
                resultados[llm_actual] = resultado
                status_text.success(f"✅ {llm_actual.capitalize()} completado ({completados+1}/{len(llms)})")
            except Exception as e:
                resultados[llm_actual] = {"exito": False, "error": str(e)}
                status_text.warning(f"⚠️ {llm_actual.capitalize()} falló")
            
            completados += 1
            progress_bar.progress(completados / len(llms))
    
    progress_bar.empty()
    status_text.empty()
    return resultados

def mostrar_comparacion(resultados_por_llm):
    """
    Muestra resultados de los 3 LLMs lado a lado
    """
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
                
                # POST
                st.markdown("#### 📱 Post")
                post_data = contenido.get("post", {})
                if post_data.get("exito"):
                    with st.expander("Ver Post", expanded=True):
                        st.markdown("**🌐 Original:**")
                        st.write(post_data.get("respuesta", ""))
                        if post_data.get("traduccion"):
                            st.markdown("---")
                            st.markdown("**🇪🇸 Traducción:**")
                            st.write(post_data.get("traduccion"))
                        st.caption(f"⏱️ {post_data.get('tiempo_ms', 0)} ms")
                else:
                    st.caption(f"⚠️ Error: {post_data.get('error', 'Desconocido')[:80]}")
                
                # EMAIL
                st.markdown("#### 📧 Email")
                email_data = contenido.get("email", {})
                if email_data.get("exito"):
                    with st.expander("Ver Email", expanded=True):
                        st.write(email_data.get("respuesta", ""))
                else:
                    st.caption(f"⚠️ Error: {email_data.get('error', 'Desconocido')[:80]}")
                
                # ESLÓGANES
                st.markdown("#### 💡 Eslogans")
                eslogans_data = contenido.get("eslogans", {})
                if eslogans_data.get("exito"):
                    with st.expander("Ver Eslogans", expanded=True):
                        st.write(eslogans_data.get("respuesta", ""))
                else:
                    st.caption(f"⚠️ Error: {eslogans_data.get('error', 'Desconocido')[:80]}")
                
            else:
                st.error(f"❌ {llm_nombre.capitalize()} falló")
                st.caption(f"Error: {resultado_llm.get('error', 'Desconocido')[:100]}")

def mostrar_un_llm(resultado, llm_nombre):
    """
    Muestra resultados de un solo LLM
    """
    if resultado.get("exito"):
        st.success(f"✅ ¡Contenido generado con {llm_nombre}!")
        
        contenido = resultado.get("contenido", {})
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
        # Limpiar caché si el usuario quiere forzar nueva generación
        if st.sidebar.button("🗑️ Limpiar caché"):
            CACHE_RESULTADOS.clear()
            generar_hash.cache_clear()
            st.success("Caché limpiado. Las próximas generaciones serán desde cero.")
        
        mercado_nombre = mercado_seleccionado.replace("🇧🇷 ", "").replace("🇯🇵 ", "").replace("🇩🇪 ", "")
        idioma_nombre = "Español" if idioma == "es" else "English"
        
        st.info(f"🎯 **Mercado:** {mercado_nombre} | **IA:** {llm_seleccionado} | **Idioma entrada:** {idioma_nombre}")
        st.caption(f"⏱️ Timeout configurado a {REQUEST_TIMEOUT} segundos (para dar tiempo a Render en plan gratuito)")
        
        try:
            tiempo_inicio = time.time()
            
            if llm == "todos":
                # Modo comparación: 3 LLMs en paralelo
                resultados = generar_con_todos(descripcion, mercado, idioma)
                mostrar_comparacion(resultados)
            else:
                # Modo normal: 1 LLM
                resultado = obtener_o_generar(descripcion, mercado, llm, idioma, False)
                mostrar_un_llm(resultado, llm_seleccionado)
            
            tiempo_total = time.time() - tiempo_inicio
            st.caption(f"⏱️ Tiempo total: {tiempo_total:.1f} segundos")
                
        except requests.exceptions.ConnectionError:
            st.error("❌ No se pudo conectar al servidor en Render. ¿Está corriendo?")
            st.info("💡 En Render plan gratuito, el servidor puede tardar 30-60 segundos en despertar. Intenta nuevamente.")
        except Exception as e:
            st.error(f"❌ Error inesperado: {str(e)}")

# ==================== PIE DE PÁGINA ====================
st.markdown("---")
st.markdown(f'''
<div class="footer">
    🌍 <strong>Global-Gadgets</strong> - Polyglot Marketing Multilingüe<br>
    🇧🇷 Brasil | 🇯🇵 Japón | 🇩🇪 Alemania<br>
    Potenciado por Gemini | Deepseek | Mistral<br>
    ⚡ Generación paralela con hilos | Timeout: {REQUEST_TIMEOUT}s
</div>
''', unsafe_allow_html=True)

# ==================== SIDEBAR CON INFORMACIÓN ====================
with st.sidebar:
    st.markdown("## ⚙️ Información")
    st.markdown(f"**Timeout actual:** {REQUEST_TIMEOUT} segundos")
    st.markdown("**Modo:** Generación paralela con hilos")
    st.markdown("**Caché:** Activado (respuestas repetidas son instantáneas)")
    
    st.markdown("---")
    st.markdown("### 💡 Tips para presentación")
    st.markdown("""
    1. **Antes de presentar:** Haz una prueba para despertar el servidor
    2. **Durante la presentación:** Todo irá rápido
    3. **Si ves timeout:** Espera 30s y reintenta
    """)
