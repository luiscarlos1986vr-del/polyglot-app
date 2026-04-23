"""
interfaz_polyglot.py - Frontend con multi-hilos para generación paralela
Yo, Luis Carlos, he implementado esta versión para acelerar la generación de contenido
Ejecutar con: streamlit run interfaz_polyglot.py
"""

# ============================================================================
# IMPORTACIONES - Librerías que necesito para que todo funcione
# ============================================================================
import streamlit as st  # Para crear la interfaz web
import requests  # Para comunicarme con mi backend API
from concurrent.futures import ThreadPoolExecutor, as_completed  # Para los hilos
from datetime import datetime  # Para mostrar fechas y tiempos
import time  # Para medir cuánto tarda la generación

# ============================================================================
# CONFIGURACIÓN DE LA PÁGINA - Estilo y título de la app web
# ============================================================================
st.set_page_config(
    page_title="Polyglot - Marketing Multilingüe",  # Título que aparece en la pestaña
    page_icon="🌍",  # Icono que aparece en la pestaña
    layout="wide"  # Layout ancho para aprovechar toda la pantalla
)

# ============================================================================
# CONSTANTES GLOBALES - Datos que no cambian durante la ejecución
# ============================================================================
# URL de mi backend Flask (cambiar si despliego en la nube)
API_URL = "http://localhost:5000"

# Lista de países que soporta mi app
# Cada país tiene: código (para APIs), nombre, bandera y color (para la UI)
PAISES = [
    {"codigo": "BR", "nombre": "Brasil", "bandera": "🇧🇷", "color": "#009c3b"},
    {"codigo": "JP", "nombre": "Japón", "bandera": "🇯🇵", "color": "#bc002d"},
    {"codigo": "DE", "nombre": "Alemania", "bandera": "🇩🇪", "color": "#000000"}
]

# Tipos de contenido que puedo generar
TIPOS_CONTENIDO = [
    {"id": "post", "nombre": "📱 Post Redes Sociales"},  # Para Instagram, Facebook, etc
    {"id": "email", "nombre": "📧 Email Promocional"},   # Para campañas de email
    {"id": "slogan", "nombre": "💡 Eslogan"}             # Frases cortas para branding
]

# ============================================================================
# FUNCIÓN PRINCIPAL - La que hace la magia de los hilos
# ============================================================================
def generar_contenido_paralelo(prompt, paises_seleccionados, tipos_seleccionados):
    """
    Yo, Luis Carlos, he creado esta función para generar contenido en PARALELO.
    
    QUÉ HACE: 
    - Toma el texto del producto y los países/tipos seleccionados
    - Crea un hilo por cada combinación (ej: Brasil-Post, Brasil-Email, etc)
    - Todos los hilos trabajan al mismo tiempo
    - Muestra progreso en tiempo real mientras generan
    
    PARÁMETROS:
    - prompt: El texto que describe el producto/servicio
    - paises_seleccionados: Lista de países que el usuario eligió
    - tipos_seleccionados: Lista de tipos de contenido que el usuario eligió
    
    RETORNA:
    - Diccionario con todos los resultados generados
    - Tiempo total que tardó todo el proceso
    """
    
    # PASO 1: Preparar todas las tareas que voy a lanzar
    # Cada tarea es una combinación de país + tipo de contenido
    tareas = []  # Lista vacía donde voy a guardar cada tarea
    
    # Recorro cada país seleccionado
    for pais in paises_seleccionados:
        # Recorro cada tipo de contenido seleccionado
        for tipo in tipos_seleccionados:
            # Creo una tarea: es un diccionario con los datos necesarios
            tarea = {
                'pais': pais,      # Guarda el país completo (con bandera, etc)
                'tipo': tipo,      # Guarda el tipo completo
                'prompt': prompt,   # Guarda el texto del producto
                'key': f"{pais['codigo']}_{tipo['id']}"  # Clave única: "BR_post"
            }
            tareas.append(tarea)  # Agrego esta tarea a mi lista
    
    # PASO 2: Configurar la barra de progreso para que el usuario vea qué pasa
    # Creo una barra que irá del 0% al 100%
    barra_progreso = st.progress(0)
    # Creo un espacio de texto para mostrar mensajes de estado
    texto_estado = st.empty()
    
    # PASO 3: Crear el "pool de hilos" - Grupo de trabajadores virtuales
    # max_workers=9 significa que puedo tener hasta 9 tareas a la vez
    # Uso 9 porque es 3 países × 3 tipos = 9 combinaciones máximas
    with ThreadPoolExecutor(max_workers=9) as executor:
        
        # PASO 4: Enviar todas las tareas a los hilos
        # futures es un diccionario que me permite rastrear cada tarea
        futures = {}  # Aquí voy a guardar cada tarea que envío
        
        texto_estado.text("🚀 Lanzando todas las generaciones en paralelo...")
        
        # Recorro cada tarea y la envío a un hilo libre
        for tarea in tareas:
            # submit() asigna la tarea a un hilo y me devuelve un "futuro"
            # El futuro es como un recibo que me permite saber cuándo termina
            futuro = executor.submit(
                llamar_api_generar,  # La función que quiero ejecutar
                tarea['pais']['codigo'],  # Primer parámetro de la función
                tarea['tipo']['id'],      # Segundo parámetro
                tarea['prompt']           # Tercer parámetro
            )
            # Guardo el futuro con su clave para identificarlo después
            futures[futuro] = tarea['key']
        
        # PASO 5: Recolectar los resultados a medida que terminan
        # as_completed() me va dando los futuros en el orden que terminan
        resultados = {}  # Diccionario donde guardo los resultados exitosos
        errores = []     # Lista donde guardo los que fallaron
        
        # Cuento cuántos han terminado para actualizar la barra
        completados = 0
        total_tareas = len(tareas)
        
        # Muestro un spinner de carga mientras espero
        with st.spinner('Generando contenido en paralelo...'):
            # Itero sobre cada futuro que se va completando
            for futuro in as_completed(futures):
                completados += 1  # Uno más terminado
                
                # Actualizo la barra de progreso (ej: 3 de 9 = 33%)
                porcentaje = completados / total_tareas
                barra_progreso.progress(porcentaje)
                
                # Obtengo la clave de esta tarea (ej: "BR_post")
                clave = futures[futuro]
                
                # Intento obtener el resultado de la tarea
                try:
                    # result() me da el valor que retornó la función
                    # timeout=15 significa: espero máximo 15 segundos por tarea
                    resultado = futuro.result(timeout=15)
                    
                    # Si llegué aquí, la tarea fue exitosa
                    resultados[clave] = resultado
                    texto_estado.text(f"✅ Completado: {clave} ({completados}/{total_tareas})")
                    
                except Exception as error:
                    # Si hubo error (timeout, API caída, etc)
                    errores.append({
                        'clave': clave,
                        'error': str(error)
                    })
                    texto_estado.text(f"❌ Error en {clave}: {str(error)[:50]}")
        
        # PASO 6: Mostrar resumen final
        if errores:
            st.warning(f"⚠️ {len(errores)} tareas fallaron de {total_tareas}")
        
        return resultados, errores

# ============================================================================
# FUNCIÓN AUXILIAR - La que realmente llama a mi API
# ============================================================================
def llamar_api_generar(codigo_pais, tipo_contenido, texto_prompt):
    """
    Yo, Luis Carlos, uso esta función para comunicarme con mi backend Flask.
    
    QUÉ HACE:
    - Toma los parámetros y los envía a mi API local
    - Espera la respuesta y la retorna
    - Si algo falla, lanza una excepción que capturará la función principal
    
    NOTA: Esta función se ejecuta DENTRO de un hilo separado
    """
    
    # Construyo el payload (los datos que envío a mi API)
    payload = {
        'pais': codigo_pais,        # Ej: "BR", "JP" o "DE"
        'tipo': tipo_contenido,      # Ej: "post", "email" o "slogan"
        'prompt': texto_prompt       # La descripción del producto
    }
    
    # Hago la llamada HTTP a mi backend
    # timeout=20: si tarda más de 20 segundos, cancelo
    respuesta = requests.post(
        f"{API_URL}/generate",  # URL del endpoint
        json=payload,            # Datos que envío
        timeout=20               # Tiempo máximo de espera
    )
    
    # Verifico si la respuesta fue exitosa
    if respuesta.status_code == 200:
        # Retorno el JSON que me envió mi backend
        return respuesta.json()
    else:
        # Si hubo error, lanzo una excepción
        raise Exception(f"Error HTTP {respuesta.status_code}: {respuesta.text}")

# ============================================================================
# INTERFAZ DE USUARIO - Todo lo que el usuario ve y toca
# ============================================================================

# Título principal de la app
st.title("🌍 Polyglot - Asistente de Marketing Multilingüe con IA")
st.markdown("---")  # Línea separadora

# ============================================================================
# BARRA LATERAL (SIDEBAR) - Configuración que el usuario puede ajustar
# ============================================================================
with st.sidebar:
    st.header("⚙️ Configuración de Generación")
    
    # Sección para seleccionar países
    st.subheader("🌎 Selecciona los países")
    paises_seleccionados = []  # Lista vacía para guardar lo que elija el usuario
    
    # Muestro un checkbox por cada país
    for pais in PAISES:
        # checkbox: True si está marcado, False si no
        # value=True significa que viene marcado por defecto
        if st.checkbox(f"{pais['bandera']} {pais['nombre']}", value=True, key=f"pais_{pais['codigo']}"):
            paises_seleccionados.append(pais)
    
    st.markdown("---")  # Separador
    
    # Sección para seleccionar tipos de contenido
    st.subheader("📝 Selecciona los tipos de contenido")
    tipos_seleccionados = []  # Lista vacía para guardar lo que elija el usuario
    
    # Muestro un checkbox por cada tipo de contenido
    for tipo in TIPOS_CONTENIDO:
        if st.checkbox(tipo['nombre'], value=True, key=f"tipo_{tipo['id']}"):
            tipos_seleccionados.append(tipo)
    
    st.markdown("---")
    
    # Muestro cuántos contenidos se van a generar
    total_a_generar = len(paises_seleccionados) * len(tipos_seleccionados)
    st.info(f"📊 **{total_a_generar}** contenidos se generarán en paralelo")
    
    # Explicación simple de qué son los hilos
    with st.expander("ℹ️ ¿Cómo funciona la generación rápida?"):
        st.markdown("""
        **Sin hilos (antes):** Generaba 1 contenido, esperaba, generaba otro...  
        ⏱️ 9 contenidos = ~22 segundos
        
        **Con hilos (ahora):** Genera TODOS al mismo tiempo  
        ⚡ 9 contenidos = ~3 segundos
        
        🚀 **Hasta 7 veces más rápido**
        """)

# ============================================================================
# ÁREA PRINCIPAL - Donde el usuario escribe el producto
# ============================================================================

# Texto de ayuda para el usuario
st.subheader("✏️ Describe tu producto o servicio")

# Área de texto grande para que el usuario describa su producto
texto_producto = st.text_area(
    label="Descripción del producto",
    placeholder="Ejemplo: Un servicio de suscripción mensual de café orgánico de especialidad, con granos provenientes de agricultura sostenible...",
    height=120,
    help="Escribe una descripción detallada. Cuanto más específico, mejor será el contenido generado."
)

# Botones de acción en columnas para mejor organización
col_boton1, col_boton2, col_boton3 = st.columns([2, 1, 1])

with col_boton2:
    # Botón principal para generar contenido
    boton_generar = st.button(
        "🚀 GENERAR CONTENIDO", 
        type="primary",  # Botón de color primario (azul)
        use_container_width=True  # Ocupa todo el ancho de la columna
    )

with col_boton3:
    # Botón para limpiar todo
    boton_limpiar = st.button(
        "🗑️ LIMPIAR", 
        use_container_width=True
    )

# Si el usuario hace click en limpiar, recargo la página
if boton_limpiar:
    st.rerun()

# ============================================================================
# PROCESAMIENTO - Cuando el usuario hace click en "Generar"
# ============================================================================
if boton_generar:
    
    # VALIDACIÓN 1: ¿El usuario escribió algo?
    if not texto_producto:
        st.error("❌ Por favor, escribe una descripción de tu producto/servicio")
    
    # VALIDACIÓN 2: ¿Seleccionó al menos un país?
    elif not paises_seleccionados:
        st.error("❌ Por favor, selecciona al menos un país")
    
    # VALIDACIÓN 3: ¿Seleccionó al menos un tipo de contenido?
    elif not tipos_seleccionados:
        st.error("❌ Por favor, selecciona al menos un tipo de contenido")
    
    # TODO está correcto, procedo a generar
    else:
        
        # Muestro métricas en tiempo real en 3 columnas
        col_metrica1, col_metrica2, col_metrica3 = st.columns(3)
        
        with col_metrica1:
            st.metric("📦 Total a generar", total_a_generar)
        
        # Marco el tiempo de inicio para medir rendimiento
        tiempo_inicio = time.time()
        
        # ================================================================
        # AQUÍ OCURRE LA MAGIA - Llamo a mi función con hilos
        # ================================================================
        resultados, errores = generar_contenido_paralelo(
            texto_producto, 
            paises_seleccionados, 
            tipos_seleccionados
        )
        # ================================================================
        
        # Calculo cuánto tiempo tardó
        tiempo_total = time.time() - tiempo_inicio
        
        with col_metrica2:
            st.metric("⏱️ Tiempo total", f"{tiempo_total:.2f} seg")
        
        with col_metrica3:
            # Calculo velocidad: contenidos por segundo
            velocidad = total_a_generar / tiempo_total if tiempo_total > 0 else 0
            st.metric("⚡ Velocidad", f"{velocidad:.1f} cont/seg")
        
        # ============================================================================
        # MOSTRAR RESULTADOS - Organizo por país en pestañas
        # ============================================================================
        
        st.markdown("---")
        st.subheader("📄 Contenido Generado")
        
        # Creo una pestaña por cada país seleccionado
        # tabs es una lista de objetos de pestaña
        pestañas = st.tabs([f"{pais['bandera']} {pais['nombre']}" for pais in paises_seleccionados])
        
        # Recorro cada pestaña con su país correspondiente
        for pestaña, pais in zip(pestañas, paises_seleccionados):
            with pestaña:
                # Dentro de cada país, muestro cada tipo de contenido
                for tipo in tipos_seleccionados:
                    clave = f"{pais['codigo']}_{tipo['id']}"  # Ej: "BR_post"
                    
                    if clave in resultados:
                        # Si el resultado existe, lo muestro en un expander
                        with st.expander(f"{tipo['nombre']}", expanded=True):
                            # Extraigo el contenido de la respuesta
                            contenido = resultados[clave].get('contenido', 'Sin contenido')
                            st.markdown(contenido)
                    else:
                        # Si no existe, muestro error
                        st.error(f"❌ No se pudo generar {tipo['nombre']}")
        
        # Muestro errores si los hubo
        if errores:
            with st.expander(f"⚠️ {len(errores)} errores ocurrieron", expanded=False):
                for error in errores:
                    st.code(f"{error['clave']}: {error['error']}")
        
        # ============================================================================
        # SECCIÓN DE DESCARGA - Opción para exportar resultados
        # ============================================================================
        
        # Creo un texto con todos los resultados para copiar/descargar
        if resultados:
            texto_exportacion = f"# RESULTADOS POLYGLOT\n"
            texto_exportacion += f"# Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            texto_exportacion += f"# Producto: {texto_producto}\n"
            texto_exportacion += f"# Tiempo: {tiempo_total:.2f} segundos\n\n"
            
            for clave, resultado in resultados.items():
                texto_exportacion += f"## {clave}\n"
                texto_exportacion += f"{resultado.get('contenido', 'Sin contenido')}\n"
                texto_exportacion += "---\n\n"
            
            # Botón para descargar los resultados como archivo de texto
            st.download_button(
                label="📥 Descargar todos los resultados (TXT)",
                data=texto_exportacion,
                file_name=f"polyglot_resultados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )

# ============================================================================
# PIE DE PÁGINA - Información adicional
# ============================================================================
st.markdown("---")
st.caption(f"🚀 Polyglot v2.0 - Generación multi-hilo | {datetime.now().year} | Hecho con ❤️ para el Diplomado Python")

# ============================================================================
# NOTA SOBRE EL BACKEND - Recordatorio importante
# ============================================================================
st.sidebar.markdown("---")
st.sidebar.warning(
    "⚠️ **Recuerda tener el backend corriendo**\n\n"
    "En otra terminal ejecuta:\n"
    "```bash\npython api.py\n```\n"
    "El backend debe estar en http://localhost:5000"
)
