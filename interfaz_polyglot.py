# interfaz_polyglot.py - TRABAJO DE TU COMPAÑERO
import streamlit as st
import requests

# Configuración de la API (tu servidor)
API_URL = "http://localhost:5000"

st.set_page_config(page_title="Polyglot", page_icon="🌍")
st.title("🌍 Polyglot - Marketing Multilingüe")
st.markdown("Genera contenido localizado para Japón, Alemania y Brasil")

# Entrada del producto
descripcion = st.text_area("📝 Describe tu producto:", height=150)

# Selección de mercado
mercado = st.selectbox("🎯 Mercado objetivo:", ["Brasil", "Japón", "Alemania"])
mercado_map = {"Brasil": "brasil", "Japón": "japon", "Alemania": "alemania"}

# Selección de LLM
llm = st.selectbox("🤖 Modelo de IA:", ["Todos", "Deepseek", "Mistral", "Gemini"])
llm_map = {"Todos": "todos", "Deepseek": "deepseek", "Mistral": "mistral", "Gemini": "gemini"}

if st.button("✨ Generar Campaña", type="primary"):
    if not descripcion:
        st.error("Por favor, describe tu producto")
    else:
        with st.spinner("Generando contenido... (puede tomar unos segundos)"):
            try:
                # Llamar a tu API Flask
                response = requests.post(
                    f"{API_URL}/generar",
                    json={
                        "descripcion_producto": descripcion,
                        "mercado": mercado_map[mercado],
                        "llm": llm_map[llm]
                    },
                    timeout=60
                )
                
                if response.status_code == 200:
                    resultado = response.json()
                    
                    if resultado.get("exito"):
                        st.success("✅ ¡Campaña generada exitosamente!")
                        
                        # Mostrar resultados en pestañas
                        tab1, tab2, tab3 = st.tabs(["📱 Redes Sociales", "📧 Email Promocional", "🎯 Eslogans"])
                        
                        with tab1:
                            if "post" in resultado["contenido"]:
                                for modelo, datos in resultado["contenido"]["post"].items():
                                    if datos.get("exito"):
                                        with st.expander(f"📝 {modelo}"):
                                            st.write(datos["respuesta"])
                                            st.caption(f"⏱️ {datos['tiempo_ms']} ms")
                                    else:
                                        st.error(f"{modelo}: {datos.get('error')}")
                        
                        with tab2:
                            if "email" in resultado["contenido"]:
                                for modelo, datos in resultado["contenido"]["email"].items():
                                    if datos.get("exito"):
                                        with st.expander(f"📧 {modelo}"):
                                            st.write(datos["respuesta"])
                                            st.caption(f"⏱️ {datos['tiempo_ms']} ms")
                        
                        with tab3:
                            if "eslogans" in resultado["contenido"]:
                                for modelo, datos in resultado["contenido"]["eslogans"].items():
                                    if datos.get("exito"):
                                        with st.expander(f"💡 {modelo}"):
                                            st.write(datos["respuesta"])
                            else:
                                st.info("Genera la campaña completa para ver los eslóganes")
                    else:
                        st.error(f"Error: {resultado.get('error')}")
                else:
                    st.error(f"Error de conexión: {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ No se pudo conectar al servidor. ¿Ejecutaste 'python api.py'?")
            except Exception as e:
                st.error(f"Error: {str(e)}")
