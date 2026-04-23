"""
interfaz_polyglot.py - Frontend con multi-hilos para generación paralela
Yo, Luis Carlos, he implementado esta versión para acelerar la generación de contenido
Mantiene EXACTAMENTE la misma interfaz visual, solo cambia el procesamiento interno
Ejecutar con: streamlit run interfaz_polyglot.py
"""

# ============================================================================
# IMPORTACIONES - Librerías que necesito para que todo funcione
# ============================================================================
import streamlit as st
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import time

# ============================================================================
# CONFIGURACIÓN DE LA PÁGINA - MANTIENE EL MISMO ESTILO
# ============================================================================
st.set_page_config(
    page_title="Polyglot - Marketing Multilingüe",
    page_icon="🌍",
    layout="wide"
)

# ============================================================================
# CONSTANTES GLOBALES - MISMO COLOR Y ESTILO QUE ANTES
# ============================================================================
API_URL = "http://localhost:5000"

PAISES = [
    {"codigo": "BR", "nombre": "Brasil", "bandera": "🇧🇷", "color": "#009c3b"},
    {"codigo": "JP", "nombre": "Japón", "bandera": "🇯🇵", "color": "#bc002d"},
    {"codigo": "DE", "nombre": "Alemania", "bandera": "🇩🇪", "color": "#000000"}
]

TIPOS_CONTENIDO = [
    {"id": "post", "nombre": "📱 Post Redes Sociales"},
    {"id": "email", "nombre": "📧 Email Promocional"},
    {"id": "slogan", "nombre": "💡 Eslogan"}
]

# ============================================================================
# FUNCIÓN PARA VERIFICAR QUE EL BACKEND ESTÉ CORRIENDO
# ============================================================================
def verificar_backend():
    """
    Yo, Luis Carlos, añadí esta función para verificar si el backend está vivo
    ANTES de intentar generar contenido. Así evito errores confusos.
    """
    try:
        # Intento conectar con el backend
        respuesta = requests.get(f"{API_URL}/", timeout=2)
        return True
    except requests.exceptions.ConnectionError:
        return False
    except:
        return False

# ============================================================================
# FUNCIÓN PRINCIPAL - Genera contenido en paralelo con manejo de errores
# ============================================================================
def generar_contenido_paralelo(prompt, paises_seleccionados, tipos_seleccionados):
    """
    Yo, Luis Carlos, he mejorado esta función para manejar errores correctamente.
    Ahora verifica el backend antes de empezar y captura TODOS los errores.
    """
    
    # PASO 1: Verificar que el backend esté corriendo
    if not verificar_backend():
        return {}, [{"error": "Backend no disponible. ¿Ejecutaste 'python api.py' en otra terminal?"}]
    
    # PASO 2: Preparar todas las tareas
    tareas = []
    for pais in paises_seleccionados:
        for tipo in tipos_seleccionados:
            tarea = {
                'pais': pais,
                'tipo': tipo,
                'prompt': prompt,
                'key': f"{pais['codigo']}_{tipo['id']}"
            }
            tareas.append(tarea)
    
    # PASO 3: Configurar barra de progreso
    barra_progreso = st.progress(0)
    texto_estado = st.empty()
    
    # PASO 4: Crear el pool de hilos
    with ThreadPoolExecutor(max_workers=9) as executor:
        
        futures = {}
        texto_estado.text("🚀 Lanzando todas las generaciones en paralelo...")
        
        # Envío cada tarea a un hilo
        for tarea in tareas:
            futuro = executor.submit(
                llamar_api_generar,
                tarea['pais']['codigo'],
                tarea['tipo']['id'],
                tarea['prompt']
            )
            futures[futuro] = tarea['key']
        
        # PASO 5: Recolectar resultados
        resultados = {}
        errores = []
        completados = 0
        total_tareas = len(tareas)
        
        # UNA SOLA VEZ - Muestro el spinner mientras proceso
        with st.spinner('Generando contenido en paralelo...'):
            for futuro in as_completed(futures):
                completados += 1
                porcentaje = completados / total_tareas
                barra_progreso.progress(porcentaje)
                
                clave = futures[futuro]
                
                try:
                    # Espero el resultado con timeout de 25 segundos
                    resultado = futuro.result(timeout=25)
                    
                    if resultado and 'contenido' in resultado:
                        resultados[clave] = resultado
                        texto_estado.text(f"✅ Completado: {clave} ({completados}/{total_tareas})")
                    else:
                        errores.append({'clave': clave, 'error': 'Respuesta vacía de la API'})
                        texto_estado.text(f"⚠️ {clave}: Respuesta vacía")
                        
                except requests.exceptions.ConnectionError:
                    errores.append({'clave': clave, 'error': 'No se pudo conectar al backend. ¿Está corriendo api.py?'})
                    texto_estado.text(f"❌ {clave}: Backend no disponible")
                except requests.exceptions.Timeout:
                    errores.append({'clave': clave, 'error': 'Timeout - La API tardó más de 25 segundos'})
                    texto_estado.text(f"⏰ {clave}: Timeout")
                except Exception as error:
                    errores.append({'clave': clave, 'error': str(error)[:100]})
                    texto_estado.text(f"❌ {clave}: Error")
        
        # Limpio la barra de progreso
        barra_progreso.empty()
        texto_estado.empty()
        
        return resultados, errores

# ============================================================================
# FUNCIÓN QUE LLAMA A LA API - Con manejo de errores mejorado
# ============================================================================
def llamar_api_generar(codigo_pais, tipo_contenido, texto_prompt):
    """
    Yo, Luis Carlos, uso esta función para comunicarme con mi backend Flask.
    Ahora con mejores mensajes de error y timeout adecuado.
    """
    
    # Construyo el payload
    payload = {
        'pais': codigo_pais,
        'tipo': tipo_contenido,
        'prompt': texto_prompt
    }
    
    # Hago la llamada con timeout de 20 segundos
    respuesta = requests.post(
        f"{API_URL}/generate",
        json=payload,
        timeout=20
    )
    
    # Verifico respuesta
    if respuesta.status_code == 200:
        return respuesta.json()
    else:
        raise Exception(f"Error HTTP {respuesta.status_code}")

# ============================================================================
# INTERFAZ DE USUARIO - EXACTAMENTE IGUAL QUE ANTES
# ============================================================================

# Título principal
st.title("🌍 Polyglot - Asistente de Marketing Multilingüe con IA")
st.markdown("---")

# ============================================================================
# BARRA LATERAL - MISMA QUE SIEMPRE
# ============================================================================
with st.sidebar:
    st.header("⚙️ Configuración")
    
    st.subheader("🌎 Países")
    paises_seleccionados = []
    for pais in PAISES:
        if st.checkbox(f"{pais['bandera']} {pais['nombre']}", value=True, key=f"pais_{pais['codigo']}"):
            paises_seleccionados.append(pais)
    
    st.markdown("---")
    
    st.subheader("📝 Tipos de contenido")
    tipos_seleccionados = []
    for tipo in TIPOS_CONTENIDO:
        if st.checkbox(tipo['nombre'], value=True, key=f"tipo_{tipo['id']}"):
            tipos_seleccionados.append(tipo)
    
    st.markdown("---")
    
    total_a_generar = len(paises_seleccionados) * len(tipos_seleccionados)
    st.info(f"📊 **{total_a_generar}** contenidos a generar")
    
    # Verificación del backend en el sidebar
    if not verificar_backend():
        st.error("❌ **Backend no conectado**\n\nEjecuta en otra terminal:\n```bash\npython api.py\n```")
    else:
        st.success("✅ Backend conectado")

# ============================================================================
# ÁREA PRINCIPAL - EXACTAMENTE IGUAL
# ============================================================================
st.subheader("✏️ Describe tu producto o servicio")

texto_producto = st.text_area(
    label="Descripción del producto",
    placeholder="Ejemplo: Auriculares con cancelación de ruido y 40 horas de batería...",
    height=120
)

col_boton1, col_boton2, col_boton3 = st.columns([2, 1, 1])

with col_boton2:
    boton_generar = st.button("🚀 GENERAR CONTENIDO", type="primary", use_container_width=True)

with col_boton3:
    boton_limpiar = st.button("🗑️ LIMPIAR", use_container_width=True)

if boton_limpiar:
    st.rerun()

# ============================================================================
# PROCESAMIENTO - MISMA LÓGICA DE VALIDACIÓN
# ============================================================================
if boton_generar:
    
    if not texto_producto:
        st.error("❌ Por favor, escribe una descripción de tu producto/servicio")
    
    elif not paises_seleccionados:
        st.error("❌ Por favor, selecciona al menos un país")
    
    elif not tipos_seleccionados:
        st.error("❌ Por favor, selecciona al menos un tipo de contenido")
    
    else:
        # Verifico el backend antes de empezar
        if not verificar_backend():
            st.error("""
            ❌ **No se puede conectar al backend**
            
            **Solución:**
            1. Abre una NUEVA terminal
            2. Ejecuta: `python api.py`
            3. Espera que diga "Running on http://localhost:5000"
            4. Vuelve a hacer click en GENERAR
            """)
        else:
            # Métricas en 3 columnas
            col_metrica1, col_metrica2, col_metrica3 = st.columns(3)
            
            with col_metrica1:
                st.metric("📦 Total a generar", total_a_generar)
            
            tiempo_inicio = time.time()
            
            # LLAMO A LA FUNCIÓN CON HILOS
            resultados, errores = generar_contenido_paralelo(
                texto_producto, 
                paises_seleccionados, 
                tipos_seleccionados
            )
            
            tiempo_total = time.time() - tiempo_inicio
            
            with col_metrica2:
                st.metric("⏱️ Tiempo total", f"{tiempo_total:.2f} seg")
            
            with col_metrica3:
                velocidad = total_a_generar / tiempo_total if tiempo_total > 0 else 0
                st.metric("⚡ Velocidad", f"{velocidad:.1f} cont/seg")
            
            # ================================================================
            # MUESTRO RESULTADOS - EXACTAMENTE IGUAL QUE ANTES
            # ================================================================
            st.markdown("---")
            st.subheader("📄 Contenido Generado")
            
            # Si hay errores de conexión, muestro mensaje claro
            if errores and not resultados:
                st.error("""
                ❌ **No se pudo generar ningún contenido**
                
                **Posibles causas:**
                1. El backend no está corriendo → Ejecuta `python api.py`
                2. Las API keys no son válidas → Revisa tu archivo `.env`
                3. Puerto 5000 está ocupado → Cambia el puerto en api.py
                """)
                
                with st.expander("Ver detalles de errores"):
                    for error in errores:
                        st.code(f"{error.get('clave', 'General')}: {error.get('error', 'Error desconocido')}")
            
            # Si tengo resultados, los muestro
            elif resultados:
                # Creo pestañas por país
                pestañas = st.tabs([f"{pais['bandera']} {pais['nombre']}" for pais in paises_seleccionados])
                
                for pestaña, pais in zip(pestañas, paises_seleccionados):
                    with pestaña:
                        for tipo in tipos_seleccionados:
                            clave = f"{pais['codigo']}_{tipo['id']}"
                            
                            if clave in resultados:
                                with st.expander(f"{tipo['nombre']}", expanded=True):
                                    contenido = resultados[clave].get('contenido', 'Sin contenido')
                                    st.markdown(contenido)
                            else:
                                st.error(f"❌ No se pudo generar {tipo['nombre']}")
                
                # Muestro errores parciales si los hay
                if errores:
                    with st.expander(f"⚠️ {len(errores)} errores en algunas tareas"):
                        for error in errores:
                            st.code(f"{error['clave']}: {error['error']}")
            
            # Opción de descarga si hay resultados
            if resultados:
                texto_exportacion = f"# RESULTADOS POLYGLOT\n"
                texto_exportacion += f"# Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                texto_exportacion += f"# Producto: {texto_producto}\n"
                texto_exportacion += f"# Tiempo: {tiempo_total:.2f} segundos\n\n"
                
                for clave, resultado in resultados.items():
                    texto_exportacion += f"## {clave}\n"
                    texto_exportacion += f"{resultado.get('contenido', 'Sin contenido')}\n"
                    texto_exportacion += "---\n\n"
                
                st.download_button(
                    label="📥 Descargar todos los resultados (TXT)",
                    data=texto_exportacion,
                    file_name=f"polyglot_resultados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )

# ============================================================================
# PIE DE PÁGINA - IGUAL
# ============================================================================
st.markdown("---")
st.caption(f"🚀 Polyglot v2.0 - Generación multi-hilo | {datetime.now().year}")
