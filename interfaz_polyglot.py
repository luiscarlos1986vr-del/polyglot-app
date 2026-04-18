# interfaz_polyglot.py - VERSIÓN DEFINITIVA CON TRADUCCIÓN
# Requisito 4: Comparación y selección entre LLMs
import streamlit as st
import requests

# ==================== CONFIGURACIÓN ====================
API_URL = "https://polyglot-app-5crh.onrender.com" # URL de tu API en producción

st.set_page_config(
    page_title="Global-Gadgets | Polyglot",
    page_icon="🌍",
    layout="wide"
)

# ==================== ESTILOS CSS PERSONALIZADOS ====================
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
        background: linear-gradient(135deg, #1e1e2e 0%, #2a2a3e 100%);
        border-radius: 16px;
        padding: 1.2rem;
        border: 1px solid #333;
        transition: transform 0.2s, box-shadow 0.2s;
        height: 100%;
    }
    .llm-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        border-color: #00C9FF;
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
        font-size: 2.5rem;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .llm-name {
        text-align: center;
        font-size: 1.3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .llm-time {
        text-align: center;
        font-size: 0.8rem;
        color: #888;
        margin-bottom: 1rem;
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
    
       /* Ajuste para los radio buttons */
    div[role="radiogroup"] label {
        margin: 5px 0;
        padding: 8px 12px;
        border-radius: 10px;
        transition: all 0.2s ease;
        cursor: pointer;
    }
    
    /* Efecto al pasar el mouse - COLOR MÁS SUAVE */
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
st.markdown('<p class="subtitle">Convierte tu producto en ventas globales 🏆<br>Campaña de Marketing para Japón | Alemania | Brasil</p>', unsafe_allow_html=True)

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
    
    # Opciones de mercado con banderas (emojis)
    mercado_opciones = {
        "🇧🇷 Brasil": "brasil",
        "🇯🇵 Japón": "japon",
        "🇩🇪 Alemania": "alemania"
    }
    
    mercado_seleccionado = st.radio(
        "Mercado",
        options=list(mercado_opciones.keys()),
        index=0,  # Brasil seleccionado por defecto
        label_visibility="collapsed"
    )
    mercado = mercado_opciones[mercado_seleccionado]

with col2:
    st.markdown("### 🤖 Motor de generación")
    st.markdown("Selecciona qué IA generará tu contenido")
    
    # Opciones de LLM con nombres claros
    llm_opciones = {
        "Gemini (Google)": "gemini",
        "Deepseek (DeepSeek)": "deepseek",
        "Mistral (Mistral AI)": "mistral",
        "Todos (Comparar)": "todos"
    }
    
    llm_seleccionado = st.radio(
        "LLM",
        options=list(llm_opciones.keys()),
        index=0,  # Gemini seleccionado por defecto
        label_visibility="collapsed"
    )
    llm = llm_opciones[llm_seleccionado]

# ==================== BOTÓN DE GENERACIÓN ====================
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    generar = st.button("✨ Generar campaña internacional ✨", type="primary", use_container_width=True)


# ==================== FUNCIONES DE VISUALIZACIÓN ====================


def mostrar_comparacion(resultado, mercado_seleccionado_nombre):
    """Muestra los resultados de los 3 LLMs lado a lado para comparar"""
    
    st.markdown("---")
    st.markdown("## 🏆 Comparación de Motores de IA")
    st.markdown("Selecciona la mejor opción para tu campaña")
    
    # Verificar que hay datos de post
    if "post" not in resultado["contenido"]:
        st.warning("No hay datos de post para comparar")
        return
    
    posts = resultado["contenido"]["post"]
    
    # Íconos y colores
    llm_iconos = {
        "Deepseek": "🔍",
        "Mistral": "🌊",
        "Gemini": "🤖"
    }
    
    colores = {
        "Deepseek": "#00C9FF",
        "Mistral": "#FF6B6B",
        "Gemini": "#92FE9D"
    }
    
    col1, col2, col3 = st.columns(3)
    columnas = [col1, col2, col3]
    llms_orden = ["Deepseek", "Mistral", "Gemini"]
    
    if 'seleccionado' not in st.session_state:
        st.session_state.seleccionado = None
    
    for idx, llm_nombre in enumerate(llms_orden):
        with columnas[idx]:
            datos_post = posts.get(llm_nombre, {})
            icono = llm_iconos.get(llm_nombre, "🤖")
            color = colores.get(llm_nombre, "#00C9FF")
            
            # Mostrar datos del POST
            if datos_post.get("exito"):
                if st.session_state.seleccionado == llm_nombre:
                    st.markdown(f'<div class="winner-badge" style="background: linear-gradient(135deg, #FFD700, #FFA500);">⭐ SELECCIONADO PARA LA CAMPAÑA ⭐</div>', unsafe_allow_html=True)
                
                st.markdown(f'''
                <div class="llm-card" style="border-top: 3px solid {color};">
                    <div class="llm-icon">{icono}</div>
                    <div class="llm-name">{llm_nombre}</div>
                    <div class="llm-time">⏱️ {datos_post.get("tiempo_ms", 0)} ms</div>
                ''', unsafe_allow_html=True)
                
                respuesta_post = datos_post.get("respuesta", "")
                traduccion_post = datos_post.get("traduccion", "")
                
                with st.expander("📱 Ver post generado", expanded=True):
                    st.markdown("**🌐 Original (Post):**")
                    st.write(respuesta_post)
                    if traduccion_post:
                        st.markdown("---")
                        st.markdown("**🇪🇸 Traducción al español (Post):**")
                        st.write(traduccion_post)
                
                # ✅ NUEVO: Mostrar ESLÓGANES del mismo LLM
                if "eslogans" in resultado["contenido"]:
                    datos_eslogans = resultado["contenido"]["eslogans"].get(llm_nombre, {})
                    if datos_eslogans.get("exito"):
                        with st.expander("💡 Ver eslóganes generados", expanded=False):
                            st.markdown("**🌐 Original (Eslóganes):**")
                            st.write(datos_eslogans.get("respuesta", ""))
                            if datos_eslogans.get("traduccion"):
                                st.markdown("---")
                                st.markdown("**🇪🇸 Traducción al español (Eslóganes):**")
                                st.write(datos_eslogans.get("traduccion"))
                    else:
                        st.caption("⚠️ No se generaron eslóganes")
                
                # Botón de selección
                if st.button(f"✨ Elegir {llm_nombre}", key=f"select_{llm_nombre}", use_container_width=True):
                    st.session_state.seleccionado = llm_nombre
                    st.success(f"🎉 ¡Has seleccionado **{llm_nombre}** para la campaña de {mercado_seleccionado_nombre}!")
                    st.balloons()
                    st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="llm-card">
                    <div class="llm-icon">{icono}</div>
                    <div class="llm-name">{llm_nombre}</div>
                ''', unsafe_allow_html=True)
                st.error(f"❌ Error en post: {datos_post.get('error', 'Desconocido')}")
                st.markdown('</div>', unsafe_allow_html=True)
    
    if st.session_state.seleccionado:
        st.success(f"📌 **Campaña confirmada con {st.session_state.seleccionado} para {mercado_seleccionado_nombre}**")


def mostrar_resultados_normales(resultado, llm_usado_texto):
    """Muestra los resultados en pestañas (modo normal)"""
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
                    with st.expander(f"📧 {modelo}"):
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
                    with st.expander(f"💡 {modelo}"):
                        st.markdown("**🌐 Original:**")
                        st.write(datos["respuesta"])
                        
                        if datos.get("traduccion"):
                            st.markdown("---")
                            st.markdown("**🇪🇸 Traducción al español:**")
                            st.write(datos["traduccion"])

# ==================== LÓGICA PRINCIPAL ====================
if generar:
    if not descripcion:
        st.error("❌ Por favor, describe tu producto para empezar")
    else:
        # Obtenemos el texto limpio del mercado para mostrarlo
        mercado_nombre_para_mostrar = mercado_seleccionado.replace("🇧🇷 ", "").replace("🇯🇵 ", "").replace("🇩🇪 ", "")
        
        with st.spinner(f"🚀 Generando contenido para {mercado_nombre_para_mostrar} con {llm_seleccionado}..."):
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
                        st.success(f"✅ ¡Campaña generada exitosamente para {mercado_nombre_para_mostrar}!")
                        
                        if llm == "todos":
                            mostrar_comparacion(resultado, mercado_nombre_para_mostrar)
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
    Potenciado por  Gemini |  Deepseek |  Mistral
</div>
''', unsafe_allow_html=True)
