# interfaz_polyglot.py - VERSIÓN CON HILOS ADAPTADA A TU BACKEND ORIGINAL
# No envía "tipo" porque tu backend genera todo junto
import streamlit as st
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# ==================== CONFIGURACIÓN ====================
API_URL = "https://polyglot-app-5crh.onrender.com"  # Tu URL de producción

st.set_page_config(
    page_title="Global-Gadgets | Polyglot",
    page_icon="🌍",
    layout="wide"
)

# ==================== ESTILOS CSS (TUS ESTILOS ORIGINALES) ====================
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


# ==================== FUNCIONES CON HILOS (RESPETAN TU BACKEND) ====================

def llamar_api_generar(descripcion, mercado, llm):
    """
    Llama a TU endpoint /generar original.
    Tu backend recibe: descripcion_producto, mercado, llm, idioma_entrada
    Tu backend devuelve: post, email, eslogans TODO EN UNA SOLA RESPUESTA
    """
    try:
        payload = {
            "descripcion_producto": descripcion,
            "mercado": mercado,
            "llm": llm,
            "idioma_entrada": "es"  # Español por defecto
        }
        
        respuesta = requests.post(
            f"{API_URL}/generar",
            json=payload,
            timeout=30
        )
        
        if respuesta.status_code == 200:
            return respuesta.json()
        else:
            return {
                "exito": False,
                "error": f"HTTP {respuesta.status_code}: {respuesta.text}"
            }
    except Exception as e:
        return {"exito": False, "error": str(e)}

def generar_todos_los_llms_en_paralelo(descripcion, mercado):
    """
    Para el modo "Todos": llama a los 3 LLMs en paralelo usando hilos.
    Cada llamada genera POST + EMAIL + SLOGAN para ese LLM.
    """
    llms = ["gemini", "deepseek", "mistral"]
    resultados = {}
    tiempo_inicio = time.time()
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        futuros = {}
        for llm_actual in llms:
            futuro = executor.submit(llamar_api_generar, descripcion, mercado, llm_actual)
            futuros[futuro] = llm_actual
        
        for futuro in as_completed(futuros):
            llm_actual = futuros[futuro]
            try:
                resultado = futuro.result(timeout=60)
                resultados[llm_actual.capitalize()] = resultado
            except Exception as e:
                resultados[llm_actual.capitalize()] = {"exito": False, "error": str(e)}
    
    tiempo_total = time.time() - tiempo_inicio
    
    # Organizo los resultados en el formato que esperan tus funciones de visualización
    organizado = {
        "exito": True,
        "contenido": {
            "post": {},
            "email": {},
            "eslogans": {}
        },
        "tiempo_total_seg": tiempo_total
    }
    
    for llm_nombre, resultado_llm in resultados.items():
        if resultado_llm.get("exito"):
            contenido = resultado_llm.get("contenido", {})
            # Post
            if "post" in contenido:
                organizado["contenido"]["post"][llm_nombre] = {
                    "exito": contenido["post"].get("exito", False),
                    "respuesta": contenido["post"].get("respuesta", ""),
                    "traduccion": contenido["post"].get("traduccion"),
                    "tiempo_ms": contenido["post"].get("tiempo_ms", 0)
                }
            # Email
            if "email" in contenido:
                organizado["contenido"]["email"][llm_nombre] = {
                    "exito": contenido["email"].get("exito", False),
                    "respuesta": contenido["email"].get("respuesta", ""),
                    "traduccion": contenido["email"].get("traduccion"),
                    "tiempo_ms": contenido["email"].get("tiempo_ms", 0)
                }
            # Eslogans
            if "eslogans" in contenido:
                organizado["contenido"]["eslogans"][llm_nombre] = {
                    "exito": contenido["eslogans"].get("exito", False),
                    "respuesta": contenido["eslogans"].get("respuesta", ""),
                    "traduccion": contenido["eslogans"].get("traduccion"),
                    "tiempo_ms": contenido["eslogans"].get("tiempo_ms", 0)
                }
        else:
            # Si el LLM falló, marco error en todos los tipos
            for tipo in ["post", "email", "eslogans"]:
                organizado["contenido"][tipo][llm_nombre] = {
                    "exito": False,
                    "error": resultado_llm.get("error", "Error desconocido")
                }
    
    return organizado

def generar_un_llm(descripcion, mercado, llm):
    """
    Para el modo normal: llama a un solo LLM.
    """
    tiempo_inicio = time.time()
    resultado = llamar_api_generar(descripcion, mercado, llm)
    tiempo_total = time.time() - tiempo_inicio
    
    if resultado.get("exito"):
        contenido = resultado.get("contenido", {})
        return {
            "exito": True,
            "contenido": {
                "post": contenido.get("post", {}),
                "email": contenido.get("email", {}),
                "slogan": contenido.get("eslogans", {})
            },
            "tiempo_total_seg": tiempo_total
        }
    else:
        return {
            "exito": False,
            "error": resultado.get("error"),
            "tiempo_total_seg": tiempo_total
        }


# ==================== FUNCIONES DE VISUALIZACIÓN (TUS ORIGINALES) ====================

def mostrar_comparacion(resultado, mercado_nombre):
    """Muestra los resultados de los 3 LLMs lado a lado"""
    st.markdown("---")
    st.markdown("## 🏆 Comparación de Motores de IA")
    
    posts = resultado["contenido"]["post"]
    color_fondo = "#d8e7f0"
    color_borde = "#FFD700"
    
    col1, col2, col3 = st.columns(3)
    llms_orden = ["Deepseek", "Mistral", "Gemini"]
    
    for idx, llm_nombre in enumerate(llms_orden):
        with [col1, col2, col3][idx]:
            datos_post = posts.get(llm_nombre, {})
            
            if datos_post.get("exito"):
                st.markdown(f"""
                <div style="background:{color_fondo}; border-radius:16px; padding:1rem; border-left:4px solid {color_borde};">
                    <div style="text-align:center; font-size:1.2rem; font-weight:600;">{llm_nombre}</div>
                    <div style="text-align:center; font-size:0.8rem;">⏱️ {datos_post.get('tiempo_ms', 0)} ms</div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("#### 📱 Post")
                with st.expander("Ver contenido", expanded=True):
                    st.markdown("**🌐 Original:**")
                    st.write(datos_post.get("respuesta", ""))
                    if datos_post.get("traduccion"):
                        st.markdown("**🇪🇸 Traducción:**")
                        st.write(datos_post.get("traduccion"))
                
                if "eslogans" in resultado["contenido"]:
                    datos_eslogans = resultado["contenido"]["eslogans"].get(llm_nombre, {})
                    if datos_eslogans.get("exito"):
                        st.markdown("#### 💡 Eslogans")
                        with st.expander("Ver contenido", expanded=True):
                            st.write(datos_eslogans.get("respuesta", ""))
                
                if "email" in resultado["contenido"]:
                    datos_email = resultado["contenido"]["email"].get(llm_nombre, {})
                    if datos_email.get("exito"):
                        st.markdown("#### 📧 Email")
                        with st.expander("Ver contenido", expanded=True):
                            st.write(datos_email.get("respuesta", ""))
            else:
                st.markdown(f"""
                <div style="background:#f0f0f0; border-radius:16px; padding:1rem; text-align:center;">
                    <div style="font-size:1.2rem;">{llm_nombre}</div>
                    <div style="color:#c00;">Error</div>
                </div>
                """, unsafe_allow_html=True)

def mostrar_resultados_normales(resultado, llm_usado):
    """Muestra resultados para un solo LLM"""
    st.markdown(f"### Resultados generados por {llm_usado}")
    
    tab1, tab2, tab3 = st.tabs(["📱 Post", "📧 Email", "💡 Eslogans"])
    
    with tab1:
        datos = resultado["contenido"].get("post", {})
        if datos.get("exito"):
            st.markdown("**🌐 Original:**")
            st.write(datos.get("respuesta", ""))
            if datos.get("traduccion"):
                st.markdown("**🇪🇸 Traducción:**")
                st.write(datos.get("traduccion"))
            st.caption(f"⏱️ {datos.get('tiempo_ms', 0)} ms")
        else:
            st.warning(f"Error: {datos.get('error', 'Desconocido')}")
    
    with tab2:
        datos = resultado["contenido"].get("email", {})
        if datos.get("exito"):
            st.write(datos.get("respuesta", ""))
        else:
            st.warning(f"Error: {datos.get('error', 'Desconocido')}")
    
    with tab3:
        datos = resultado["contenido"].get("slogan", {})
        if datos.get("exito"):
            st.write(datos.get("respuesta", ""))
        else:
            st.warning(f"Error: {datos.get('error', 'Desconocido')}")


# ==================== LÓGICA PRINCIPAL ====================
if generar:
    if not descripcion:
        st.error("❌ Por favor, describe tu producto")
    else:
        mercado_nombre = mercado_seleccionado.replace("🇧🇷 ", "").replace("🇯🇵 ", "").replace("🇩🇪 ", "")
        
        with st.spinner(f"🚀 Generando contenido para {mercado_nombre} con {llm_seleccionado}..."):
            try:
                if llm == "todos":
                    resultado = generar_todos_los_llms_en_paralelo(descripcion, mercado)
                else:
                    resultado = generar_un_llm(descripcion, mercado, llm)
                
                if resultado.get("exito"):
                    st.success(f"✅ ¡Campaña generada en {resultado.get('tiempo_total_seg', 0):.1f} segundos!")
                    
                    if llm == "todos":
                        mostrar_comparacion(resultado, mercado_nombre)
                    else:
                        mostrar_resultados_normales(resultado, llm_seleccionado)
                else:
                    st.error(f"❌ Error: {resultado.get('error', 'Desconocido')}")
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ No se pudo conectar al servidor. ¿El backend está corriendo?")
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
