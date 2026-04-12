# -*- coding: utf-8 -*-
"""
api.py - Endpoints para la Interfaz de Polyglot
Creado: 2026-04-08
@author: user1 (Arquitectura)

PROPÓSITO DE ESTE ARCHIVO:
    Este archivo crea un SERVIDOR WEB (API) que permite que la interfaz de usuario
    (hecha por tu compañero) se comunique con tu código de servicios.py.
    
    Es como un "mesero" que recibe pedidos de la interfaz y los lleva a los LLMs.
    
    PARA TU COMPAÑERO (INTERFAZ):
    - No necesita instalar nada especial (solo requests o fetch)
    - Solo necesita hacer peticiones HTTP a http://localhost:5000
    - Recibirá respuestas en formato JSON (fácil de mostrar en pantalla)
"""

# ==================== IMPORTACIONES ====================

from flask import Flask, request, jsonify
# Flask: Crea el servidor web
# request: Para leer lo que envía la interfaz
# jsonify: Para enviar respuestas en formato JSON

from flask_cors import CORS
# CORS: Permite que la interfaz (que corre en otro puerto) pueda comunicarse
# Sin esto, la interfaz web no podría llamar a tu API

import traceback
# traceback: Para imprimir errores detallados (útil para depuración)

# Importamos las funciones que ya creaste en servicios.py
from estructura_servicios_poliglot_ import (
    generar_campana_completa,    # Función principal que genera TODO
    comparar_llms_para_contenido, # Función para comparar LLMs
    MERCADOS                      # Diccionario con Japón, Alemania, Brasil
)

# ==================== CONFIGURACIÓN ====================

# Crear la aplicación Flask (el servidor web)
app = Flask(__name__)

# Habilitar CORS para que cualquier interfaz pueda conectarse
# Esto es necesario si la interfaz es una página web (HTML/JavaScript)
CORS(app)

# Lista de LLMs disponibles para validar lo que envía la interfaz
LLMS_DISPONIBLES = ["deepseek", "mistral", "gemini", "todos"]

# ==================== ENDPOINT 1: VERIFICAR SALUD ====================
# PROPÓSITO: Que la interfaz compruebe si el servidor está funcionando
# MÉTODO: GET (solo consulta, no envía datos)
# URL: http://localhost:5000/health

@app.route('/health', methods=['GET'])
def health_check():
    """
    Endpoint de verificación de salud.
    
    ¿PARA QUÉ SIRVE?
    La interfaz puede llamar a este endpoint al iniciar para asegurarse
    de que tu servidor está corriendo antes de intentar generar contenido.
    
    ¿QUÉ DEVUELVE?
    Un JSON confirmando que todo está bien.
    
    EJEMPLO DE RESPUESTA:
    {
        "estado": "OK",
        "mensaje": "Polyglot API funcionando correctamente",
        "versiones": {
            "deepseek": "conectado",
            "mistral": "conectado", 
            "gemini": "conectado"
        }
    }
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


# ==================== ENDPOINT 2: LISTAR MERCADOS ====================
# PROPÓSITO: Decirle a la interfaz qué países están disponibles
# MÉTODO: GET
# URL: http://localhost:5000/mercados

@app.route('/mercados', methods=['GET'])
def obtener_mercados():
    """
    Endpoint para obtener la lista de mercados disponibles.
    
    ¿PARA QUÉ SIRVE?
    La interfaz puede usar esto para crear un menú desplegable
    con los países disponibles (Japón, Alemania, Brasil).
    
    ¿QUÉ DEVUELVE?
    La lista de mercados y detalles de cada uno.
    
    EJEMPLO DE RESPUESTA:
    {
        "exito": true,
        "mercados": ["japon", "alemania", "brasil"],
        "detalles": {
            "japon": {"nombre_pais": "Japón", "codigo_idioma": "ja", "tono": "formal..."},
            "alemania": {"nombre_pais": "Alemania", "codigo_idioma": "de", ...},
            "brasil": {"nombre_pais": "Brasil", "codigo_idioma": "pt-BR", ...}
        }
    }
    """
    try:
        # Extraer solo la información relevante para la interfaz
        detalles_mercados = {}
        for clave, config in MERCADOS.items():
            detalles_mercados[clave] = {
                "nombre_pais": config["nombre_pais"],
                "codigo_idioma": config["codigo_idioma"],
                "tono": config["tono"]  # Para que la interfaz pueda mostrar sugerencias
            }
        
        return jsonify({
            "exito": True,
            "mercados": list(MERCADOS.keys()),
            "detalles": detalles_mercados
        })
    except Exception as e:
        return jsonify({
            "exito": False,
            "error": str(e)
        }), 500


# ==================== ENDPOINT 3: LISTAR LLMs ====================
# PROPÓSITO: Decirle a la interfaz qué modelos de IA están disponibles
# MÉTODO: GET
# URL: http://localhost:5000/llms

@app.route('/llms', methods=['GET'])
def obtener_llms():
    """
    Endpoint para obtener la lista de LLMs disponibles.
    
    ¿PARA QUÉ SIRVE?
    La interfaz puede usar esto para crear opciones de selección
    (Deepseek, Mistral, Gemini, o comparar todos).
    
    EJEMPLO DE RESPUESTA:
    {
        "exito": true,
        "llms": ["deepseek", "mistral", "gemini", "todos"],
        "descripcion": {
            "deepseek": "Modelo chino, eficiente en costo",
            "mistral": "Modelo europeo, excelente para marketing",
            "gemini": "Modelo de Google, rápido y versátil",
            "todos": "Compara los 3 modelos simultáneamente"
        }
    }
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


# ==================== ENDPOINT 4: GENERAR CAMPAÑA COMPLETA ====================
# PROPÓSITO: ¡El más importante! Genera todo el contenido de marketing
# MÉTODO: POST (envía datos, recibe resultados)
# URL: http://localhost:5000/generar

@app.route('/generar', methods=['POST'])
def generar_campana():
    """
    Endpoint principal para generar contenido de marketing.
    
    REQUISITOS 2 y 3: Genera posts, emails y eslóganes localizados.
    
    ¿CÓMO LO USA LA INTERFAZ?
    1. La interfaz recoge lo que el usuario escribió
    2. Arma un JSON con los datos
    3. Lo envía a este endpoint
    4. Espera la respuesta con todo el contenido generado
    
    EJEMPLO DE LO QUE ENVÍA LA INTERFAZ (JSON):
    {
        "descripcion_producto": "Auriculares con cancelación de ruido...",
        "mercado": "brasil",
        "llm": "todos"
    }
    
    EJEMPLO DE LO QUE RECIBE LA INTERFAZ (JSON):
    {
        "exito": true,
        "mercado": "brasil",
        "contenido": {
            "post": {
                "Deepseek": "🎧 Foco total no seu som!...",
                "Mistral": "...",
                "Gemini": "..."
            },
            "email": {...},
            "eslogans": {...}
        }
    }
    """
    try:
        # PASO 1: Leer lo que envió la interfaz
        datos = request.get_json()
        
        # PASO 2: Validar que llegaron datos
        if not datos:
            return jsonify({
                "exito": False,
                "error": "No se recibieron datos. Asegúrate de enviar un JSON válido."
            }), 400
        
        # PASO 3: Extraer cada campo
        descripcion = datos.get('descripcion_producto')
        mercado = datos.get('mercado')
        llm = datos.get('llm', 'todos')  # Si no especifica, usa 'todos'
        
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
        
        # PASO 6: Validar que el LLM sea válido
        if llm not in LLMS_DISPONIBLES:
            return jsonify({
                "exito": False,
                "error": f"LLM '{llm}' no válido. Opciones: {LLMS_DISPONIBLES}"
            }), 400
        
        # PASO 7: ¡LLAMAR A TU FUNCIÓN! (la que ya probaste que funciona)
        # Aquí es donde ocurre la magia: se conecta a las APIs y genera contenido
        resultado = generar_campana_completa(
            descripcion_producto=descripcion,
            mercado=mercado,
            llm_seleccionado=llm
        )
        
        # PASO 8: Devolver el resultado a la interfaz
        return jsonify(resultado)
        
    except Exception as e:
        # Si algo sale mal, imprimimos el error y lo enviamos a la interfaz
        print(f"❌ Error en /generar: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            "exito": False,
            "error": f"Error interno del servidor: {str(e)}"
        }), 500


# ==================== ENDPOINT 5: COMPARAR LLMs ====================
# PROPÓSITO: Comparar respuestas de diferentes LLMs para un tipo de contenido
# MÉTODO: POST
# URL: http://localhost:5000/comparar

@app.route('/comparar', methods=['POST'])
def comparar():
    """
    Endpoint para comparar respuestas entre LLMs.
    
    REQUISITO 4: Permite ver lado a lado qué LLM generó mejor contenido.
    
    ¿PARA QUÉ SIRVE?
    Si el gerente de marketing quiere ver qué IA hace mejores posts,
    puede usar este endpoint para comparar resultados.
    
    EJEMPLO DE PETICIÓN (JSON):
    {
        "descripcion_producto": "Auriculares con cancelación de ruido...",
        "mercado": "brasil",
        "tipo_contenido": "post"
    }
    
    EJEMPLO DE RESPUESTA:
    {
        "exito": true,
        "mercado": "brasil",
        "tipo_contenido": "post",
        "respuestas": {
            "Deepseek": {"respuesta": "🎧 Foco total...", "tiempo_ms": 1200},
            "Mistral": {"respuesta": "...", "tiempo_ms": 950},
            "Gemini": {"respuesta": "...", "tiempo_ms": 800}
        }
    }
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
        
        # Validaciones
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
        
        # Llamar a la función comparativa
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


# ==================== ENDPOINT 6: DOCUMENTACIÓN ====================
# PROPÓSITO: Mostrar una página web con la documentación de la API
# MÉTODO: GET
# URL: http://localhost:5000/

@app.route('/', methods=['GET'])
def documentacion():
    """
    Endpoint raíz que muestra documentación HTML.
    
    ¿PARA QUÉ SIRVE?
    Cuando alguien abra http://localhost:5000 en su navegador,
    verá una página bonita explicando cómo usar la API.
    
    ¡Útil para tu compañero si olvida cómo funciona!
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
    "llm": "todos"
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
        
        <h2>📝 Ejemplo de uso desde Python</h2>
        <pre>
import requests

respuesta = requests.post(
    "http://localhost:5000/generar",
    json={
        "descripcion_producto": "Auriculares con cancelación de ruido",
        "mercado": "brasil",
        "llm": "todos"
    }
)
print(respuesta.json())
        </pre>
        
        <hr>
        <p>✨ Polyglot - Marketing Multilingüe con IA ✨</p>
    </body>
    </html>
    """


# ==================== EJECUCIÓN DEL SERVIDOR ====================
# Este bloque se ejecuta SOLO cuando corres "python api.py"
# No se ejecuta si otro archivo importa este módulo

if __name__ == '__main__':
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
    print("   Abre esta URL en tu navegador para ver la documentación")
    print("   Presiona CTRL+C para detener el servidor")
    print("="*60 + "\n")
    
    # Ejecutar el servidor Flask
    # debug=True: Recarga automáticamente cuando guardas cambios
    # host='0.0.0.0': Permite conexiones desde otros dispositivos en la red
    # port=5000: Puerto donde escucha el servidor
    app.run(host='0.0.0.0', port=5000, debug=True)
