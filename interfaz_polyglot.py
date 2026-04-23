# interfaz_polyglot.py - VERSIÓN CON HILOS (Usa tu endpoint /generar original)
# Requisito 4: Comparación y selección entre LLMs
# OPTIMIZACIÓN: Uso hilos para generar contenido en paralelo
import streamlit as st
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# ==================== CONFIGURACIÓN ====================
API_URL = "https://polyglot-app-5crh.onrender.com"  # Tu URL de producción en Render

st.set_page_config(
    page_title="Global-Gadgets | Polyglot",
    page_icon="🌍",
    layout="wide"
)

# ==================== ESTILOS CSS PERSONALIZADOS ====================
# MANTENGO TUS ESTILOS EXACTAMENTE IGUALES
st.markdown("""
<style>
    /* Título principal */
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
    /* Tarjeta de producto */
    .product-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 0.5rem;
        border-radius: 20px;
        border: 1px solid #333;
        margin-bottom: 0.5rem;
    }
    /* Tarjetas de comparación */
    .llm-card {
        background: rgba(30, 30, 46, 0.7);
        border-radius: 16px;
        padding: 1rem;
        border: 1px solid #2a2a3e;
        transition: all 0.2s ease;
        height: 100%;
    }
    .llm-card:hover {
        background: rgba(45, 45, 65, 0.8);
        border-color: #6b9bc2;
        transform: translateY(-2px);
    }
    .winner-badge {
        background: linear-gradient(135deg, #FFD700, #FFA500);
        color: #000;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 0.5rem;
    }
    .llm-icon {
        font-size: 2rem;
        text-align: center;
        margin-bottom: 0.3rem;
        opacity: 0.8;
    }
    .llm-name {
        text-align: center;
        font-size: 1.1rem;
        font-weight: 500;
        margin-bottom: 0.3rem;
        color: #c0c0c0;
    }
    .llm-time {
        text-align: center;
        font-size: 0.7rem;
        color: #888;
        margin-bottom: 0.8rem;
        border-bottom: 1px solid #2a2a3e;
        padding-bottom: 0.5rem;
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 0.5rem;
        color: #888;
        font-size: 0.8rem;
        border-top: 0.5px solid #444;
    }
    /* Botón principal */
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

    .streamlit-expanderHeader {
        font-size: 0.85rem;
        color: #6b9bc2;
        background: transparent;
    }
    
       /* Ajuste para los radio buttons */
    div[role="radiogroup"] label {
        margin: 5px 0;
        padding: 8px 12px;
        border-radius: 10px;
        transition: all 0.2s ease;
        cursor: pointer;
    }
    
    /* Efecto al pasar el mouse */
    div[role="radiogroup"] label:hover {
        background-color: #d8e7f0 !important;
        color: white !important;
        transform: translateX(4px);
    }
    
    /* Estilo para la opción SELECCIONADA */
    div[role="radiogroup"] label[data-baseweb="radio"]:has(input:checked) {
        background-color: #d8e7f0 !important;
        color: white !important;
        font-weight: 500;
        border-left: 3px solid #FFD700;
    }
    
    /* Círculo del radio cuando está seleccionado */
    div[role="radiogroup"] label[data-baseweb="radio"]:has(input:checked) .st-emotion-cache-1b0udgb {
        border-color: #FFD700 !important;
    }
    
    div[role="radiogroup"] label[data-baseweb="radio"]:has(input:checked) .st-emotion-cache-1b0udgb svg {
        fill: #FFD700 !important;
    }
    
</style>
""", unsafe_allow_html=True)

# ==================== HEADER CON EMPRESA ====================
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

# ==================== CONFIGURACIÓN EN COLUMNAS ====================
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

# ==================== BOTÓN DE GENERACIÓN ====================
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    generar = st.button("✨ Generar campaña internacional ✨", type="primary", use_container_width=True)


# ==================== NUEVAS FUNCIONES CON HILOS (USANDO TU ENDPOINT /generar) ====================
# Yo, Luis Carlos, adapté estas funciones para usar tu endpoint /generar original

def llamar_api_para_tipo(tipo_contenido, descripcion, mercado, llm):
    """
    Llama a tu API /generar para UN SOLO tipo de contenido.
    Esta función se ejecutará en un hilo separado.
    """
    try:
        # Construyo el payload EXACTAMENTE como lo espera tu backend
        payload = {
            "descripcion_producto": descripcion,
            "mercado": mercado,
            "tipo": tipo_contenido,  # "post", "email" o "slogan"
            "llm": llm
        }
        
        # Llamo a tu endpoint /generar
        respuesta = requests.post(
            f"{API_URL}/generar",
            json=payload,
            timeout=25
        )
        
        if respuesta.status_code == 200:
            datos = respuesta.json()
            
            # Tu backend devuelve algo como: {"exito": true, "contenido": {...}, "tiempo_ms": 123}
            if datos.get("exito"):
                # Extraigo el contenido según el tipo
                contenido = datos.get("contenido", {})
                
                # Dependiendo del tipo, la respuesta puede estar en diferentes campos
                if tipo_contenido == "post":
                    respuesta_texto = contenido.get("post", "")
                elif tipo_contenido == "email":
                    respuesta_texto = contenido.get("email", "")
                elif tipo_contenido == "slogan":
                    respuesta_texto = contenido.get("slogan", "")
                else:
                    respuesta_texto = str(contenido)
                
                return {
                    "tipo": tipo_contenido,
                    "exito": True,
                    "respuesta": respuesta_texto,
                    "tiempo_ms": datos.get("tiempo_ms", 0),
                    "raw": datos
                }
            else:
                return {
                    "tipo": tipo_contenido,
                    "exito": False,
                    "error": datos.get("error", "Error desconocido")
                }
        else:
            return {
                "tipo": tipo_contenido,
                "exito": False,
                "error": f"HTTP {respuesta.status_code}"
            }
    except Exception as e:
        return {
            "tipo": tipo_contenido,
            "exito": False,
            "error": str(e)
        }

def generar_contenido_con_hilos(descripcion, mercado, llm):
    """
    Genera los 3 tipos de contenido (post, email, slogan) EN PARALELO usando hilos.
    Cada tipo se envía a tu endpoint /generar por separado.
    """
    tipos = ["post", "email", "slogan"]
    resultados = {"exito": True, "contenido": {}}
    tiempo_inicio = time.time()
    
    # Creo un pool de hasta 3 hilos (uno por cada tipo de contenido)
    with ThreadPoolExecutor(max_workers=3) as executor:
        futuros = {}
        for tipo in tipos:
            futuro = executor.submit(llamar_api_para_tipo, tipo, descripcion, mercado, llm)
            futuros[futuro] = tipo
        
        # Recolecto resultados a medida que terminan
        for futuro in as_completed(futuros):
            tipo = futuros[futuro]
            try:
                resultado = futuro.result(timeout=30)
                if resultado and resultado.get("exito"):
                    resultados["contenido"][tipo] = resultado
                else:
                    resultados["contenido"][tipo] = {
                        "exito": False,
                        "error": resultado.get("error", "Error desconocido") if resultado else "Sin respuesta"
                    }
            except Exception as e:
                resultados["contenido"][tipo] = {
                    "exito": False,
                    "error": str(e)
                }
    
    tiempo_total = (time.time() - tiempo_inicio) * 1000
    resultados["tiempo_total_ms"] = int(tiempo_total)
    return resultados

def generar_todos_los_llms_con_hilos(descripcion, mercado):
    """
    Para el modo "Todos (Comparar)": genera contenido con los 3 LLMs EN PARALELO.
    Cada LLM genera sus 3 tipos de contenido en paralelo también.
    """
    llms = ["gemini", "deepseek", "mistral"]
    resultado_final = {
        "exito": True,
        "contenido": {
            "post": {},
            "email": {},
            "eslogans": {}
        }
    }
    
    tiempo_inicio = time.time()
    
    # Creo un pool de hasta 3 hilos (uno por cada LLM)
    with ThreadPoolExecutor(max_workers=3) as executor:
        futuros = {}
        for llm_actual in llms:
            futuro = executor.submit(generar_contenido_con_hilos, descripcion, mercado, llm_actual)
            futuros[futuro] = llm_actual
        
        # Recolecto resultados
        for futuro in as_completed(futuros):
            llm_actual = futuros[futuro]
            llm_nombre = llm_actual.capitalize()
            
            try:
                resultado_llm = futuro.result(timeout=60)
                
                # Organizo los resultados por tipo y LLM
                for tipo, datos in resultado_llm.get("contenido", {}).items():
                    if tipo == "post":
                        resultado_final["contenido"]["post"][llm_nombre] = {
                            "exito": datos.get("exito", False),
                            "respuesta": datos.get("respuesta", ""),
                            "traduccion": None,
                            "tiempo_ms": datos.get("tiempo_ms", 0)
                        }
                    elif tipo == "email":
                        resultado_final["contenido"]["email"][llm_nombre] = {
                            "exito": datos.get("exito", False),
                            "respuesta": datos.get("respuesta", ""),
                            "traduccion": None,
                            "tiempo_ms": datos.get("tiempo_ms", 0)
                        }
                    elif tipo == "slogan":
                        resultado_final["contenido"]["eslogans"][llm_nombre] = {
                            "exito": datos.get("exito", False),
                            "respuesta": datos.get("respuesta", ""),
                            "traduccion": None,
                            "tiempo_ms": datos.get("tiempo_ms", 0)
                        }
            except Exception as e:
                # Si un LLM falla, marco error pero continúo con los otros
                for tipo in ["post", "email", "eslogans"]:
                    if tipo == "eslogans":
                        resultado_final["contenido"][tipo][llm_nombre] = {
                            "exito": False,
                            "error": str(e)
                        }
                    else:
                        resultado_final["contenido"][tipo][llm_nombre] = {
                            "exito": False,
                            "error": str(e)
                        }
    
    tiempo_total = (time.time() - tiempo_inicio) * 1000
    resultado_final["tiempo_total_ms"] = int(tiempo_total)
    return resultado_final


# ==================== FUNCIONES DE VISUALIZACIÓN ====================
# MANTENGO TUS FUNCIONES EXACTAMENTE IGUALES

def mostrar_comparacion(resultado, mercado_seleccionado_nombre):
    """Muestra los resultados de los 3 LLMs lado a lado para comparar"""
    
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
                <div style="
                    background: {color_fondo};
                    border-radius: 16px;
                    padding: 1rem;
                    margin: 0.5rem 0;
                    border-left: 4px solid {color_borde};
                    transition: all 0.2s ease;
                ">
                    <div style="text-align: center; font-size: 1.2rem; font-weight: 600; color: {color_texto}; margin: 0.3rem 0;">{llm_nombre}</div>
                    <div style="text-align: center; font-size: 0.8rem; color: #555; border-bottom: 1px solid #c0d0e0; padding-bottom: 0.5rem; margin-bottom: 0.5rem;">⏱️ {datos_post.get("tiempo_ms", 0)} ms</div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("#### 📱 Post para Redes Sociales")
                with st.expander("Ver contenido", expanded=True):
                    st.markdown("**🌐 Original:**")
                    st.write(datos_post.get("respuesta", ""))
                    if datos_post.get("traduccion"):
                        st.markdown("---")
                        st.markdown("**🇪🇸 Traducción al español:**")
                        st.write(datos_post.get("traduccion"))
                    st.caption(f"⏱️ {datos_post.get('tiempo_ms', 0)} ms")
                
                if "eslogans" in resultado["contenido"]:
                    datos_eslogans = resultado["contenido"]["eslogans"].get(llm_nombre, {})
                    if datos_eslogans.get("exito"):
                        st.markdown("#### 💡 Eslogans Publicitarios")
                        with st.expander("Ver contenido", expanded=True):
                            st.markdown("**🌐 Original:**")
                            st.write(datos_eslogans.get("respuesta", ""))
                            if datos_eslogans.get("traduccion"):
                                st.markdown("---")
                                st.markdown("**🇪🇸 Traducción al español:**")
                                st.write(datos_eslogans.get("traduccion"))
                            st.caption(f"⏱️ {datos_eslogans.get('tiempo_ms', 0)} ms")
                
                if "email" in resultado["contenido"]:
                    datos_email = resultado["contenido"]["email"].get(llm_nombre, {})
                    if datos_email.get("exito"):
                        st.markdown("#### 📧 Email Promocional")
                        with st.expander("Ver contenido", expanded=True):
                            st.markdown("**🌐 Original:**")
                            st.write(datos_email.get("respuesta", ""))
                            if datos_email.get("traduccion"):
                                st.markdown("---")
                                st.markdown("**🇪🇸 Traducción al español:**")
                                st.write(datos_email.get("traduccion"))
                            st.caption(f"⏱️ {datos_email.get('tiempo_ms', 0)} ms")
                
                st.markdown("---")
                
            else:
                st.markdown(f"""
                <div style="
                    background: #f0f0f0;
                    border-radius: 16px;
                    padding: 1rem;
                    text-align: center;
                    border: 1px solid #ddd;
                ">
                    <div style="font-size: 1.2rem; font-weight: 500; color: #888;">{llm_nombre}</div>
                    <div style="color: #c00; font-size: 0.8rem;">Error en generación</div>
                </div>
                """, unsafe_allow_html=True)


def mostrar_resultados_normales(resultado, llm_usado_texto):
    """Muestra los resultados en pestañas (modo normal)"""
    st.markdown(f"### Resultados generados por {llm_usado_texto}")
    
    tab1, tab2, tab3 = st.tabs(["📱 Redes Sociales", "📧 Email Promocional", "🎯 Eslogans"])
    
    with tab1:
        st.markdown("#### 📱 Post para Redes Sociales")
        if "post" in resultado["contenido"]:
            datos = resultado["contenido"]["post"]
            if datos.get("exito"):
                with st.expander("Ver contenido", expanded=True):
                    st.markdown("**🌐 Original:**")
                    st.write(datos.get("respuesta", ""))
                    if datos.get("traduccion"):
                        st.markdown("---")
                        st.markdown("**🇪🇸 Traducción al español:**")
                        st.write(datos.get("traduccion"))
                    st.caption(f"⏱️ {datos.get('tiempo_ms', 0)} ms")
            else:
                st.warning(f"⚠️ Error: {datos.get('error', 'Error desconocido')}")
        else:
            st.info("No hay datos de post disponibles")
    
    with tab2:
        st.markdown("#### 📧 Email Promocional")
        if "email" in resultado["contenido"]:
            datos = resultado["contenido"]["email"]
            if datos.get("exito"):
                with st.expander("Ver contenido", expanded=True):
                    st.markdown("**🌐 Original:**")
                    st.write(datos.get("respuesta", ""))
                    if datos.get("traduccion"):
                        st.markdown("---")
                        st.markdown("**🇪🇸 Traducción al español:**")
                        st.write(datos.get("traduccion"))
                    st.caption(f"⏱️ {datos.get('tiempo_ms', 0)} ms")
            else:
                st.warning(f"⚠️ Error: {datos.get('error', 'Error desconocido')}")
        else:
            st.info("No hay datos de email disponibles")
    
    with tab3:
        st.markdown("#### 🎯 Eslogans Publicitarios")
        if "slogan" in resultado["contenido"]:
            datos = resultado["contenido"]["slogan"]
            if datos.get("exito"):
                with st.expander("Ver contenido", expanded=True):
                    st.markdown("**🌐 Original:**")
                    st.write(datos.get("respuesta", ""))
                    if datos.get("traduccion"):
                        st.markdown("---")
                        st.markdown("**🇪🇸 Traducción al español:**")
                        st.write(datos.get("traduccion"))
                    st.caption(f"⏱️ {datos.get('tiempo_ms', 0)} ms")
            else:
                st.warning(f"⚠️ Error: {datos.get('error', 'Error desconocido')}")
        else:
            st.info("No hay datos de eslóganes disponibles")


# ==================== LÓGICA PRINCIPAL ====================
# MODIFICO SOLO LA LÓGICA DE LLAMADA - Ahora usa hilos con tu endpoint /generar
if generar:
    if not descripcion:
        st.error("❌ Por favor, describe tu producto para empezar")
    else:
        mercado_nombre_para_mostrar = mercado_seleccionado.replace("🇧🇷 ", "").replace("🇯🇵 ", "").replace("🇩🇪 ", "")
        
        with st.spinner(f"🚀 Generando contenido para {mercado_nombre_para_mostrar} con {llm_seleccionado}..."):
            try:
                tiempo_inicio_total = time.time()
                
                if llm == "todos":
                    # MODO COMPARACIÓN: Genero con los 3 LLMs EN PARALELO
                    resultado = generar_todos_los_llms_con_hilos(descripcion, mercado)
                else:
                    # MODO NORMAL: Genero los 3 tipos de contenido EN PARALELO
                    resultado = generar_contenido_con_hilos(descripcion, mercado, llm)
                
                tiempo_total = time.time() - tiempo_inicio_total
                
                # Verifico si hay al menos algún contenido generado
                tiene_contenido = False
                if llm == "todos":
                    for tipo in ["post", "email", "eslogans"]:
                        if resultado["contenido"].get(tipo):
                            # Verifico si algún LLM tuvo éxito
                            for llm_key in resultado["contenido"][tipo]:
                                if resultado["contenido"][tipo].get(llm_key, {}).get("exito"):
                                    tiene_contenido = True
                                    break
                else:
                    for tipo in ["post", "email", "slogan"]:
                        if resultado["contenido"].get(tipo, {}).get("exito"):
                            tiene_contenido = True
                            break
                
                if tiene_contenido:
                    st.success(f"✅ ¡Campaña generada exitosamente para {mercado_nombre_para_mostrar} en {tiempo_total:.1f} segundos!")
                    
                    if llm == "todos":
                        mostrar_comparacion(resultado, mercado_nombre_para_mostrar)
                    else:
                        mostrar_resultados_normales(resultado, llm_seleccionado)
                else:
                    st.error("❌ No se pudo generar ningún contenido. Verifica las API keys y que el backend esté funcionando.")
                    
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
    Potenciado por  Gemini |  Deepseek |  Mistral
</div>
''', unsafe_allow_html=True)
