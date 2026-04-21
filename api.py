# -*- coding: utf-8 -*-
"""
api.py - Endpoints para la Interfaz de Polyglot

Este archivo crea un servidor web (API) que actúa como el "mesero" de nuestro proyecto.
Recibe las peticiones que vienen desde la interfaz de usuario (Streamlit),
las procesa llamando a las funciones del archivo de servicios,
y devuelve los resultados en formato JSON para que la interfaz los muestre.
"""

# ==================== IMPORTACIÓN DE LIBRERÍAS ====================
# Importamos las herramientas necesarias para crear nuestro servidor web
from flask import Flask, request, jsonify  # Flask crea el servidor, request lee los datos que llegan, jsonify formatea las respuestas
from flask_cors import CORS  # CORS permite que la interfaz (que corre en otro puerto) pueda comunicarse con nuestra API
import traceback  # Nos ayuda a imprimir errores detallados cuando algo sale mal

# Importamos las funciones que creamos en el archivo de servicios (el cerebro del proyecto)
from estructura_servicios_poliglot_ import (
    generar_campana_completa,    # Nuestra función principal que genera TODO el contenido
    comparar_llms_para_contenido, # Función para comparar cómo responden las diferentes IAs
    MERCADOS                      # Diccionario con la configuración de Japón, Alemania y Brasil
)

# ==================== CONFIGURACIÓN DEL SERVIDOR ====================
# Creamos la aplicación Flask (nuestro servidor web)
app = Flask(__name__)

# Habilitamos CORS para que cualquier interfaz (local o en la nube) pueda conectarse
# Sin esto, la interfaz de Streamlit no podría llamar a nuestra API
CORS(app)

# Lista de IAs disponibles para validar lo que envía la interfaz
LLMS_DISPONIBLES = ["deepseek", "mistral", "gemini", "todos"]


# ==================== ENDPOINT 1: VERIFICAR SALUD DEL SERVIDOR ====================
@app.route('/health', methods=['GET'])
def health_check():
    """
    Este endpoint es como un "chequeo médico" de nuestro servidor.
    La interfaz lo llama para asegurarse de que el backend está funcionando
    antes de intentar generar contenido.
    Nuestro objetivo es devolver un mensaje simple confirmando que todo está bien.
    """
    return jsonify({
        "estado": "OK",
        "mensaje": "Polyglot API funcionando correctamente",
        "versiones": {
            "deepseek": "conectado",
            "mistral": "conectado",
            "gemini": "conectado"
        }
    })


# ==================== ENDPOINT 2: LISTAR MERCADOS DISPONIBLES ====================
@app.route('/mercados', methods=['GET'])
def obtener_mercados():
    """
    Este endpoint le dice a la interfaz qué países están disponibles
    (Japón, Alemania, Brasil). Nuestro objetivo es que la interfaz pueda
    crear un menú desplegable con las opciones correctas.
    """
    try:
        # Preparamos la información de cada mercado para enviarla a la interfaz
        detalles_mercados = {}
        for clave, config in MERCADOS.items():
            detalles_mercados[clave] = {
                "nombre_pais": config["nombre_pais"],
                "codigo_idioma": config["codigo_idioma"],
                "tono": config["tono"]  # Incluimos el tono para que la interfaz pueda mostrar sugerencias
            }
        
        return jsonify({
            "exito": True,
            "mercados": list(MERCADOS.keys()),
            "detalles": detalles_mercados
        })
    except Exception as e:
        # Si algo sale mal, devolvemos un error claro
        return jsonify({"exito": False, "error": str(e)}), 500


# ==================== ENDPOINT 3: LISTAR IAs DISPONIBLES ====================
@app.route('/llms', methods=['GET'])
def obtener_llms():
    """
    Este endpoint le dice a la interfaz qué modelos de IA están disponibles
    (Deepseek, Mistral, Gemini, o la opción "Todos" para comparar).
    Nuestro objetivo es que la interfaz pueda crear las opciones de selección.
    """
    return jsonify({
        "exito": True,
        "llms": ["deepseek", "mistral", "gemini", "todos"],
        "descripcion": {
            "deepseek": "Modelo chino, eficiente en costo",
            "mistral": "Modelo europeo, excelente para marketing",
            "gemini": "Modelo de Google, rápido y versátil",
            "todos": "Compara los 3 modelos simultáneamente"
        }
    })


# ==================== ENDPOINT 4: GENERAR CAMPAÑA COMPLETA (EL MÁS IMPORTANTE) ====================
@app.route('/generar', methods=['POST'])
def generar_campana():
    """
    Este es nuestro endpoint principal, el corazón de la aplicación.
    Nuestro objetivo es:
    1. Recibir la descripción del producto, el mercado, la IA a usar y el idioma
    2. Validar que todos los datos sean correctos
    3. Llamar a nuestra función principal del archivo de servicios
    4. Devolver el resultado a la interfaz para que lo muestre al usuario
    """
    try:
        # PASO 1: Leer los datos que envió la interfaz (vienen en formato JSON)
        datos = request.get_json()
        
        # PASO 2: Verificar que llegaron datos
        if not datos:
            return jsonify({
                "exito": False,
                "error": "No se recibieron datos. Asegúrate de enviar un JSON válido."
            }), 400
        
        # PASO 3: Extraer cada campo con valores por defecto por si no vienen
        descripcion = datos.get('descripcion_producto')
        mercado = datos.get('mercado')
        llm = datos.get('llm', 'todos')  # Si no especifica, usamos 'todos'
        idioma_entrada = datos.get('idioma_entrada', 'es')  # Si no especifica, usamos español
        
        # Mostramos en los logs qué idioma recibimos (útil para depuración)
        print(f"🔍 [API] Idioma recibido: {idioma_entrada}")
        
        # PASO 4: Validar que los campos obligatorios existen
        if not descripcion:
            return jsonify({
                "exito": False,
                "error": "Falta el campo 'descripcion_producto' en la petición."
            }), 400
        
        if not mercado:
            return jsonify({
                "exito": False,
                "error": "Falta el campo 'mercado' en la petición."
            }), 400
        
        # PASO 5: Validar que el mercado sea válido (Japón, Alemania o Brasil)
        if mercado not in MERCADOS:
            return jsonify({
                "exito": False,
                "error": f"Mercado '{mercado}' no válido. Opciones: {list(MERCADOS.keys())}"
            }), 400
        
        # PASO 6: Validar que la IA seleccionada sea válida
        if llm not in LLMS_DISPONIBLES:
            return jsonify({
                "exito": False,
                "error": f"LLM '{llm}' no válido. Opciones: {LLMS_DISPONIBLES}"
            }), 400
        
        # PASO 7: ¡LLAMAR A NUESTRA FUNCIÓN PRINCIPAL!
        # Aquí es donde ocurre la magia: nos conectamos a las IAs y generamos todo el contenido
        resultado = generar_campana_completa(
            descripcion_producto=descripcion,
            mercado=mercado,
            llm_seleccionado=llm,
            idioma_entrada=idioma_entrada
        )
        
        # PASO 8: Devolver el resultado a la interfaz en formato JSON
        return jsonify(resultado)
        
    except Exception as e:
        # Si algo sale mal, imprimimos el error en los logs y lo enviamos a la interfaz
        print(f"❌ Error en /generar: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            "exito": False,
            "error": f"Error interno del servidor: {str(e)}"
        }), 500


# ==================== ENDPOINT 5: COMPARAR IAs PARA UN TIPO DE CONTENIDO ====================
@app.route('/comparar', methods=['POST'])
def comparar():
    """
    Este endpoint permite comparar cómo responden las tres IAs
    para un tipo de contenido específico (solo post, solo email o solo eslóganes).
    Nuestro objetivo es ayudar al gerente de marketing a elegir qué IA hace mejor
    cada tipo de contenido.
    """
    try:
        datos = request.get_json()
        
        if not datos:
            return jsonify({
                "exito": False,
                "error": "No se recibieron datos."
            }), 400
        
        descripcion = datos.get('descripcion_producto')
        mercado = datos.get('mercado')
        tipo_contenido = datos.get('tipo_contenido', 'post')
        
        # Validamos que los datos sean correctos
        if not descripcion:
            return jsonify({
                "exito": False,
                "error": "Falta 'descripcion_producto'"
            }), 400
        
        if not mercado or mercado not in MERCADOS:
            return jsonify({
                "exito": False,
                "error": f"Mercado inválido. Opciones: {list(MERCADOS.keys())}"
            }), 400
        
        tipos_validos = ['post', 'email', 'eslogans']
        if tipo_contenido not in tipos_validos:
            return jsonify({
                "exito": False,
                "error": f"Tipo de contenido inválido. Opciones: {tipos_validos}"
            }), 400
        
        # Llamamos a la función comparativa
        resultado = comparar_llms_para_contenido(
            descripcion_producto=descripcion,
            mercado=mercado,
            tipo_contenido=tipo_contenido
        )
        
        return jsonify(resultado)
        
    except Exception as e:
        print(f"❌ Error en /comparar: {str(e)}")
        return jsonify({
            "exito": False,
            "error": str(e)
        }), 500


# ==================== ENDPOINT 6: DOCUMENTACIÓN (PÁGINA PRINCIPAL) ====================
@app.route('/', methods=['GET'])
def documentacion():
    """
    Este endpoint muestra una página web bonita con la documentación de nuestra API.
    Cuando alguien abre la URL base de nuestra API en el navegador,
    ve una explicación clara de cómo usarla.
    Nuestro objetivo es que cualquier desarrollador pueda entender rápidamente
    cómo conectarse a nuestro servicio.
    """
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Polyglot API - Documentación</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
            h1 { color: #2c3e50; }
            h2 { color: #34495e; margin-top: 30px; }
            code { background: #f4f4f4; padding: 2px 6px; border-radius: 4px; }
            pre { background: #f4f4f4; padding: 15px; border-radius: 8px; overflow-x: auto; }
            .endpoint { background: #e8f4f8; padding: 15px; border-radius: 8px; margin: 15px 0; }
            .method { font-weight: bold; color: #2980b9; }
            .url { font-family: monospace; font-size: 1.1em; }
        </style>
    </head>
    <body>
        <h1>🌍 Polyglot API - Marketing Multilingüe</h1>
        <p>Servidor para generar contenido de marketing localizado usando IA.</p>
        
        <h2>📡 Endpoints Disponibles</h2>
        
        <div class="endpoint">
            <p><span class="method">GET</span> <span class="url">/health</span></p>
            <p>Verificar que el servidor está funcionando.</p>
        </div>
        
        <div class="endpoint">
            <p><span class="method">GET</span> <span class="url">/mercados</span></p>
            <p>Obtener lista de mercados disponibles (Japón, Alemania, Brasil).</p>
        </div>
        
        <div class="endpoint">
            <p><span class="method">GET</span> <span class="url">/llms</span></p>
            <p>Obtener lista de LLMs disponibles (Deepseek, Mistral, Gemini).</p>
        </div>
        
        <div class="endpoint">
            <p><span class="method">POST</span> <span class="url">/generar</span></p>
            <p>Generar campaña completa (post, email, eslóganes).</p>
            <pre>{
    "descripcion_producto": "texto del producto",
    "mercado": "brasil",
    "llm": "todos",
    "idioma_entrada": "es"
}</pre>
        </div>
        
        <div class="endpoint">
            <p><span class="method">POST</span> <span class="url">/comparar</span></p>
            <p>Comparar LLMs para un tipo de contenido específico.</p>
            <pre>{
    "descripcion_producto": "texto del producto",
    "mercado": "brasil",
    "tipo_contenido": "post"
}</pre>
        </div>
        
        <h2>🔧 Instalación</h2>
        <pre>pip install flask flask-cors</pre>
        
        <h2>🚀 Ejecución</h2>
        <pre>python api.py</pre>
        
        <hr>
        <p>✨ Polyglot - Marketing Multilingüe con IA ✨</p>
    </body>
    </html>
    """


# ==================== EJECUCIÓN DEL SERVIDOR ====================
# Este bloque se ejecuta SOLO cuando corremos "python api.py"
# No se ejecuta si otro archivo importa este módulo
if __name__ == '__main__':
    # Mostramos un mensaje bonito en la consola con todos los endpoints disponibles
    print("\n" + "="*60)
    print("🌍 POLYGLOT API - SERVIDOR DE MARKETING MULTILINGÜE")
    print("="*60)
    print("\n📡 Endpoints disponibles:")
    print("   GET  /          - Esta documentación (abre en navegador)")
    print("   GET  /health    - Verificar estado del servidor")
    print("   GET  /mercados  - Listar mercados disponibles")
    print("   GET  /llms      - Listar LLMs disponibles")
    print("   POST /generar   - Generar campaña completa")
    print("   POST /comparar  - Comparar LLMs para un contenido")
    print("\n🚀 Servidor iniciando en http://localhost:5000")
    print("="*60 + "\n")
    
    # Iniciamos el servidor Flask
    # host='0.0.0.0' permite que otros dispositivos en la red se conecten
    # port=5000 es el puerto donde escucha nuestro servidor
    # debug=True hace que el servidor se reinicie automáticamente cuando guardamos cambios
    app.run(host='0.0.0.0', port=5000, debug=True)
