# -*- coding: utf-8 -*-
"""
estructura_servicios_poliglot
.py - Capa de Servicios del Proyecto Polyglot
Creado: 2026-04-08
@author: user1 (Arquitectura)

PROPÓSITO: Este archivo contiene toda la lógica de negocio del proyecto.
           Comunica la interfaz (frontend) con los modelos de IA (backend).
           
           PARA TU COMPAÑERO (INTERFAZ): 
           Solo necesita llamar a las funciones de este archivo,
           NO necesita entender cómo funcionan internamente.
"""

# ✅ Conservado - Importación de librerías base
import os
import time  # NUEVO: Para medir tiempos de respuesta
from dotenv import load_dotenv
from openai import OpenAI  # Deepseek
from mistralai.client import Mistral  # Mistral
from google import genai  # Gemini

# ==================== CONFIGURACIÓN INICIAL ====================
# ✅ Conservado - Cargar variables del archivo .env
load_dotenv()

# ✅ Conservado - Configuración de API keys
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TIMEOUT = int(os.getenv("TIMEOUT", 30))

# ✅ Conservado - Validación de keys
if not all([DEEPSEEK_API_KEY, MISTRAL_API_KEY, GEMINI_API_KEY]):
    missing = []
    if not DEEPSEEK_API_KEY: missing.append("DEEPSEEK_API_KEY")
    if not MISTRAL_API_KEY: missing.append("MISTRAL_API_KEY")
    if not GEMINI_API_KEY: missing.append("GEMINI_API_KEY")
    raise ValueError(f"Faltan keys en .env: {', '.join(missing)}")


# ✅ Conservado - Inicializar clientes

# Cliente Deepseek
deepseek_client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com",
    timeout=TIMEOUT
)

# Cliente Mistral
mistral_client = Mistral(
    api_key=MISTRAL_API_KEY,
    timeout_ms=TIMEOUT * 1000
)

# Cliente Gemini
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

# ✅ Conservado - Comprobación
print("✅ Todos los clientes inicializados correctamente")


# ==================== CONFIGURACIÓN DE MERCADOS ====================
# REQUISITO 3: Localización para Japón, Alemania y Brasil
# Diccionario con instrucciones culturales para cada mercado
MERCADOS = {
    "japon": {
        "codigo_idioma": "ja",  # Código ISO para japonés
        "nombre_pais": "Japón",
        "tono": "formal, respetuoso y con énfasis en la calidad y precisión",
        "referencias_culturales": "valoran la armonía, la cortesía y la estética minimalista",
        "saludo": "株式会社Global-Gadgetsをご覧いただきありがとうございます"  # "Gracias por visitar Global-Gadgets"
    },
    "alemania": {
        "codigo_idioma": "de",
        "nombre_pais": "Alemania",
        "tono": "directo, profesional y enfocado en datos técnicos y eficiencia",
        "referencias_culturales": "valoran la puntualidad, la precisión y la documentación clara",
        "saludo": "Sehr geehrte Kundin, sehr geehrter Kunde"  # "Estimado cliente"
    },
    "brasil": {
        "codigo_idioma": "pt-BR",
        "nombre_pais": "Brasil",
        "tono": "cálido, enérgico y con entusiasmo, usando un lenguaje cercano",
        "referencias_culturales": "valoran la calidez humana, el carnaval y el fútbol",
        "saludo": "Olá! Bem-vindo à Global-Gadgets"  # "¡Hola! Bienvenido a Global-Gadgets"
    }
}


# ==================== CONSTRUCCIÓN DE PROMPTS ====================
# Estas funciones construyen las instrucciones que se enviarán a los LLMs

def construir_prompt_post(descripcion_producto, mercado):
    """
    REQUISITO 2: Construye el prompt para generar un post de redes sociales (formato Twitter/X)
    
    Args:
        descripcion_producto (str): Descripción del producto en español/inglés
        mercado (str): Clave del mercado ('japon', 'alemania', 'brasil')
    
    Returns:
        str: Prompt completo para enviar al LLM
    """
    config = MERCADOS[mercado]
    
    # El prompt incluye instrucciones específicas de formato y cultura
    prompt = f"""
    Actúa como un experto en marketing localizado para {config['nombre_pais']}.
    
    TAREA: Crear un post para redes sociales (estilo Twitter/X) sobre el siguiente producto.
    IMPORTANTE: El contenido debe estar en IDIOMA {config['codigo_idioma']} ({config['nombre_pais']}).
    
    DESCRIPCIÓN DEL PRODUCTO:
    {descripcion_producto}
    
    REQUISITOS DEL POST:
    - Máximo 280 caracteres
    - Tono: {config['tono']}
    - Incluir 2-3 hashtags relevantes para {config['nombre_pais']}
    - Adaptación cultural: {config['referencias_culturales']}
    
    Responde ÚNICAMENTE con el texto del post, sin explicaciones adicionales.
    """
    return prompt


def construir_prompt_email(descripcion_producto, mercado):
    """
    REQUISITO 2: Construye el prompt para generar un email promocional
    
    Args:
        descripcion_producto (str): Descripción del producto
        mercado (str): Clave del mercado
    
    Returns:
        str: Prompt completo para el email
    """
    config = MERCADOS[mercado]
    
    prompt = f"""
    Actúa como un redactor de email marketing especializado en {config['nombre_pais']}.
    
    TAREA: Escribir un email promocional en IDIOMA {config['codigo_idioma']}.
    
    PRODUCTO:
    {descripcion_producto}
    
    ESTRUCTURA REQUERIDA:
    1. ASUNTO: Llamativo, máximo 60 caracteres
    2. CUERPO: Aproximadamente 150 palabras
       - Saludo apropiado para {config['nombre_pais']}
       - Beneficios del producto
       - Llamada a la acción (CTA)
       - Despedida cálida
    
    Tono: {config['tono']}
    Adaptación cultural: {config['referencias_culturales']}
    
    Responde ÚNICAMENTE en formato:
    ASUNTO: [texto del asunto]
    CUERPO: [texto del email]
    """
    return prompt


def construir_prompt_eslogans(descripcion_producto, mercado):
    """
    REQUISITO 2: Construye el prompt para generar 3 eslóganes publicitarios
    
    Args:
        descripcion_producto (str): Descripción del producto
        mercado (str): Clave del mercado
    
    Returns:
        str: Prompt completo para los eslóganes
    """
    config = MERCADOS[mercado]
    
    prompt = f"""
    Actúa como un creativo publicitario con experiencia en el mercado {config['nombre_pais']}.
    
    TAREA: Generar 3 eslóganes publicitarios en IDIOMA {config['codigo_idioma']}.
    
    PRODUCTO:
    {descripcion_producto}
    
    REQUISITOS:
    - Cada eslogan: máximo 8 palabras
    - Tono: {config['tono']}
    - Deben ser memorables y persuasivos
    - Adaptación cultural: {config['referencias_culturales']}
    
    Responde ÚNICAMENTE con los 3 eslóganes, uno por línea, sin numerar.
    """
    return prompt


# ==================== FUNCIONES DE CONSULTA A LLMs ====================
# REQUISITO 1: Conectividad Multi-LLM
# Cada función se comunica con un LLM específico

def consultar_deepseek(prompt, temperatura=0.7):
    """
    Envía un prompt a Deepseek y retorna la respuesta.
    
    Args:
        prompt (str): Instrucción para el modelo
        temperatura (float): Creatividad (0.0 = más preciso, 1.0 = más creativo)
    
    Returns:
        dict: {'exito': bool, 'respuesta': str, 'error': str (si existe), 'tiempo_ms': int}
    """
    inicio = time.time()
    try:
        respuesta = deepseek_client.chat.completions.create(
            model="deepseek-chat",  # Modelo gratuito/eficiente
            messages=[{"role": "user", "content": prompt}],
            temperature=temperatura,
            max_tokens=500  # Suficiente para posts/emails cortos
        )
        tiempo_ms = int((time.time() - inicio) * 1000)
        
        return {
            "exito": True,
            "respuesta": respuesta.choices[0].message.content,
            "error": None,
            "tiempo_ms": tiempo_ms,
            "modelo": "Deepseek"
        }
    except Exception as e:
        return {
            "exito": False,
            "respuesta": None,
            "error": str(e),
            "tiempo_ms": int((time.time() - inicio) * 1000),
            "modelo": "Deepseek"
        }

def consultar_mistral(prompt, temperatura=0.7):
    """
    Envía un prompt a Mistral usando requests directos.
    Más confiable que el SDK.
    """
    import requests
    inicio = time.time()
    
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistral-large-latest",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperatura,
        "max_tokens": 500
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=TIMEOUT)
        tiempo_ms = int((time.time() - inicio) * 1000)
        
        if response.status_code == 200:
            resultado = response.json()
            contenido = resultado["choices"][0]["message"]["content"]
            return {
                "exito": True,
                "respuesta": contenido,
                "error": None,
                "tiempo_ms": tiempo_ms,
                "modelo": "Mistral"
            }
        else:
            return {
                "exito": False,
                "respuesta": None,
                "error": f"HTTP {response.status_code}: {response.text[:200]}",
                "tiempo_ms": tiempo_ms,
                "modelo": "Mistral"
            }
    except Exception as e:
        tiempo_ms = int((time.time() - inicio) * 1000)
        return {
            "exito": False,
            "respuesta": None,
            "error": str(e),
            "tiempo_ms": tiempo_ms,
            "modelo": "Mistral"
        }

def consultar_gemini(prompt, temperatura=0.7):
    """
    Envía un prompt a Gemini y retorna la respuesta.
    """
    inicio = time.time()
    try:
        respuesta = gemini_client.models.generate_content(
            model="gemini-2.5-flash-lite",  # Rápido y económico
            contents=prompt,
            config={
                "temperature": temperatura,
                "max_output_tokens": 500
            }
        )
        tiempo_ms = int((time.time() - inicio) * 1000)
        
        return {
            "exito": True,
            "respuesta": respuesta.text,
            "error": None,
            "tiempo_ms": tiempo_ms,
            "modelo": "Gemini"
        }
    except Exception as e:
        return {
            "exito": False,
            "respuesta": None,
            "error": str(e),
            "tiempo_ms": int((time.time() - inicio) * 1000),
            "modelo": "Gemini"
        }


# ==================== FUNCIÓN PRINCIPAL ====================
# REQUISITO 4: Permite seleccionar qué LLM usar o comparar todos

def generar_campana_completa(descripcion_producto, mercado, llm_seleccionado="todos"):
    """
    REQUISITOS 2 y 3: Genera TODO el contenido de marketing para un mercado específico.
    
    Args:
        descripcion_producto (str): Descripción del producto
        mercado (str): 'japon', 'alemania', o 'brasil'
        llm_seleccionado (str): 'deepseek', 'mistral', 'gemini', o 'todos'
    
    Returns:
        dict: Estructura completa con todo el contenido generado
    """
    
    # Validar que el mercado existe
    if mercado not in MERCADOS:
        return {
            "exito": False,
            "error": f"Mercado '{mercado}' no válido. Opciones: {list(MERCADOS.keys())}"
        }
    
    # Seleccionar las funciones de consulta según el LLM elegido
    consultas_disponibles = {
        "deepseek": consultar_deepseek,
        "mistral": consultar_mistral,
        "gemini": consultar_gemini
    }
    
    if llm_seleccionado == "todos":
        llms_a_usar = consultas_disponibles.values()
        modo = "comparativa"
    elif llm_seleccionado in consultas_disponibles:
        llms_a_usar = [consultas_disponibles[llm_seleccionado]]
        modo = "single"
    else:
        return {
            "exito": False,
            "error": f"LLM '{llm_seleccionado}' no válido. Opciones: 'deepseek', 'mistral', 'gemini', 'todos'"
        }
    
    # Construir los prompts para cada tipo de contenido
    prompts = {
        "post": construir_prompt_post(descripcion_producto, mercado),
        "email": construir_prompt_email(descripcion_producto, mercado),
        "eslogans": construir_prompt_eslogans(descripcion_producto, mercado)
    }
    
    # Diccionario para almacenar resultados
    resultados = {
        "exito": True,
        "mercado": mercado,
        "configuracion_mercado": MERCADOS[mercado],
        "modo": modo,
        "llm_utilizado": llm_seleccionado,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "contenido": {}
    }
    
    # Para cada tipo de contenido, consultar a cada LLM
    for tipo_contenido, prompt in prompts.items():
        resultados["contenido"][tipo_contenido] = {}
        
        for consulta_func in llms_a_usar:
            # Obtener nombre del modelo para usarlo como clave
            # Llamada de prueba para saber qué modelo es
            prueba = consulta_func("Di hola")
            nombre_modelo = prueba.get("modelo", "desconocido")
            
           # Consulta real
            respuesta = consulta_func(prompt)
            
            # Obtener el texto de la respuesta
            respuesta_texto = respuesta.get("respuesta")
            
            # Traducir al español si la respuesta es exitosa
            traduccion = None
            if respuesta.get("exito") and respuesta_texto:
                codigo_idioma = MERCADOS[mercado]["codigo_idioma"]
                traduccion = traducir_a_espanol(respuesta_texto, codigo_idioma)
            
            resultados["contenido"][tipo_contenido][nombre_modelo] = {
                "respuesta": respuesta_texto,
                "traduccion": traduccion,  # ← NUEVO: traducción al español
                "exito": respuesta.get("exito"),
                "error": respuesta.get("error"),
                "tiempo_ms": respuesta.get("tiempo_ms")
            }
    
    return resultados


# ==================== FUNCIÓN COMPARATIVA RÁPIDA ====================
# REQUISITO 4 (Avanzado): Compara LLMs para un tipo de contenido específico

def comparar_llms_para_contenido(descripcion_producto, mercado, tipo_contenido="post"):
    """
    REQUISITO 4: Envía el mismo prompt a TODOS los LLMs y permite comparar resultados.
    
    Args:
        descripcion_producto (str): Descripción del producto
        mercado (str): 'japon', 'alemania', 'brasil'
        tipo_contenido (str): 'post', 'email', o 'eslogans'
    
    Returns:
        dict: Respuestas de todos los LLMs para comparar lado a lado
    """
    
    # Seleccionar el constructor de prompt adecuado
    constructores = {
        "post": construir_prompt_post,
        "email": construir_prompt_email,
        "eslogans": construir_prompt_eslogans
    }
    
    if tipo_contenido not in constructores:
        return {
            "exito": False,
            "error": f"Tipo de contenido '{tipo_contenido}' no válido. Opciones: post, email, eslogans"
        }
    
    # Construir el prompt
    prompt = constructores[tipo_contenido](descripcion_producto, mercado)
    
    # Consultar a los 3 LLMs
    resultados = {
        "exito": True,
        "mercado": mercado,
        "tipo_contenido": tipo_contenido,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "respuestas": {}
    }
    
    # Lista de LLMs a consultar
    llms = [
        ("Deepseek", consultar_deepseek),
        ("Mistral", consultar_mistral),
        ("Gemini", consultar_gemini)
    ]
    
    for nombre, consulta_func in llms:
        respuesta = consulta_func(prompt)
        resultados["respuestas"][nombre] = {
            "respuesta": respuesta.get("respuesta"),
            "exito": respuesta.get("exito"),
            "error": respuesta.get("error"),
            "tiempo_ms": respuesta.get("tiempo_ms")
        }
    
    return resultados

# TRDUCCIÓN A ESP


# ==================== FUNCIÓN DE TRADUCCIÓN ====================
def traducir_a_espanol(texto, idioma_origen):
    """
    Traduce un texto del idioma origen al español.
    Usa Gemini como primera opción, con respaldo en Deepseek si falla.
    
    Args:
        texto (str): Texto a traducir
        idioma_origen (str): 'ja', 'de', 'pt-BR'
    
    Returns:
        str: Texto traducido al español
    """
    if not texto:
        return "⚠️ No hay texto para traducir"
    
    # Mapeo de idiomas para el prompt
    idiomas = {
        "ja": "japonés",
        "de": "alemán",
        "pt-BR": "portugués de Brasil"
    }
    
    nombre_idioma = idiomas.get(idioma_origen, "el idioma original")
    
    prompt_traduccion = f"""
    Traduce el siguiente texto del {nombre_idioma} al español.
    Mantén el tono y estilo original.
    Responde SOLO con la traducción, sin explicaciones.
    
    TEXTO ORIGINAL:
    {texto}
    
    TRADUCCIÓN AL ESPAÑOL:
    """
    
    # Intento 1: Gemini
    try:
        respuesta = gemini_client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt_traduccion,
            config={"temperature": 0.3, "max_output_tokens": 800}
        )
        return respuesta.text.strip()
    except Exception as e:
        error_msg = str(e)
        if "503" in error_msg or "UNAVAILABLE" in error_msg:
            print("⚠️ Gemini saturado, usando Deepseek como respaldo...")
        else:
            print(f"⚠️ Error en Gemini: {error_msg}")
    
    # Intento 2: Deepseek (respaldo)
    try:
        respuesta = deepseek_client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt_traduccion}],
            temperature=0.3,
            max_tokens=800
        )
        return respuesta.choices[0].message.content.strip()
    except Exception as e:
        print(f"⚠️ Error en Deepseek: {str(e)}")
    
    # Intento 3: Mistral (último respaldo)
    try:
        respuesta = mistral_client.chat.complete(
            model="mistral-large-latest",
            messages=[{"role": "user", "content": prompt_traduccion}],
            temperature=0.3,
            max_tokens=800
        )
        return respuesta.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ Error en todos los motores de traducción: {str(e)}")
        return f"❌ Error en traducción: {error_msg}"

# ==================== EJEMPLO DE USO (PARA PRUEBAS) ====================
# Este bloque solo se ejecuta si corres este archivo directamente
# NO se ejecuta cuando otro archivo lo importa

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🧪 POLYGLOT - PRUEBA DE SERVICIOS")
    print("="*60)
    
    # Producto de ejemplo para pruebas
    producto_ejemplo = """
    Auriculares inalámbricos con cancelación de ruido activa, 
    40 horas de batería y carga rápida (10 minutos = 4 horas de uso).
    Incluye estuche de carga y 3 tamaños de almohadillas.
    """
    
    print("\n📝 PRODUCTO DE PRUEBA:")
    print(producto_ejemplo)
    
    # Probar generación para Brasil con todos los LLMs
    print("\n🚀 Generando campaña para BRASIL con TODOS los LLMs...")
    resultado = generar_campana_completa(producto_ejemplo, "brasil", "todos")
    
    if resultado["exito"]:
        print("\n✅ CONTENIDO GENERADO EXITOSAMENTE")
        print(f"Mercado: {resultado['configuracion_mercado']['nombre_pais']}")
        print(f"Modo: {resultado['modo']}")
        
        # Mostrar un ejemplo del post generado por Deepseek
        if "post" in resultado["contenido"] and "Deepseek" in resultado["contenido"]["post"]:
            print("\n📱 EJEMPLO - POST (Deepseek):")
            print(resultado["contenido"]["post"]["Deepseek"]["respuesta"][:200] + "...")
    else:
        print(f"\n❌ Error: {resultado.get('error')}")
    
    print("\n" + "="*60)
    print("✅ Prueba completada. Revisa los resultados.")
    print("="*60)
