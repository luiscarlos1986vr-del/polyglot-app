# -*- coding: utf-8 -*-
"""
api.py - Endpoints para la Interfaz de Polyglot
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import traceback

from estructura_servicios_poliglot_ import (
    generar_campana_completa,
    comparar_llms_para_contenido,
    MERCADOS
)

app = Flask(__name__)
CORS(app)

LLMS_DISPONIBLES = ["deepseek", "mistral", "gemini", "todos"]


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "estado": "OK",
        "mensaje": "Polyglot API funcionando correctamente",
        "versiones": {
            "deepseek": "conectado",
            "mistral": "conectado",
            "gemini": "conectado"
        }
    })


@app.route('/mercados', methods=['GET'])
def obtener_mercados():
    try:
        detalles_mercados = {}
        for clave, config in MERCADOS.items():
            detalles_mercados[clave] = {
                "nombre_pais": config["nombre_pais"],
                "codigo_idioma": config["codigo_idioma"],
                "tono": config["tono"]
            }
        
        return jsonify({
            "exito": True,
            "mercados": list(MERCADOS.keys()),
            "detalles": detalles_mercados
        })
    except Exception as e:
        return jsonify({"exito": False, "error": str(e)}), 500


@app.route('/llms', methods=['GET'])
def obtener_llms():
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


@app.route('/generar', methods=['POST'])
def generar_campana():
    try:
        datos = request.get_json()
        
        if not datos:
            return jsonify({
                "exito": False,
                "error": "No se recibieron datos. Asegúrate de enviar un JSON válido."
            }), 400
        
        descripcion = datos.get('descripcion_producto')
        mercado = datos.get('mercado')
        llm = datos.get('llm', 'todos')
        idioma_entrada = datos.get('idioma_entrada', 'es')
        
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
        
        if mercado not in MERCADOS:
            return jsonify({
                "exito": False,
                "error": f"Mercado '{mercado}' no válido. Opciones: {list(MERCADOS.keys())}"
            }), 400
        
        if llm not in LLMS_DISPONIBLES:
            return jsonify({
                "exito": False,
                "error": f"LLM '{llm}' no válido. Opciones: {LLMS_DISPONIBLES}"
            }), 400
        
        resultado = generar_campana_completa(
            descripcion_producto=descripcion,
            mercado=mercado,
            llm_seleccionado=llm,
            idioma_entrada=idioma_entrada
        )
        
        return jsonify(resultado)
        
    except Exception as e:
        print(f"❌ Error en /generar: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            "exito": False,
            "error": f"Error interno del servidor: {str(e)}"
        }), 500


@app.route('/comparar', methods=['POST'])
def comparar():
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


@app.route('/', methods=['GET'])
def documentacion():
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
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
