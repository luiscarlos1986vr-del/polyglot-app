# -*- coding: utf-8 -*-
"""
estructura_servicios_poliglot.py - Capa de Servicios del Proyecto Polyglot

Este archivo es el "cerebro" del proyecto. Aquí conectamos con las tres inteligencias artificiales
(Deepseek, Mistral y Gemini), construimos los mensajes (prompts) que les enviamos,
y procesamos las respuestas para generar el contenido de marketing localizado.
"""

# ==================== IMPORTACIÓN DE LIBRERÍAS ====================
# Importamos las herramientas necesarias para que nuestro proyecto funcione
import os
import time
from dotenv import load_dotenv
from openai import OpenAI          # Usamos OpenAI para conectarnos a Deepseek
from mistralai.client import Mistral  # SDK oficial de Mistral
from google import genai            # SDK oficial de Google Gemini


# ==================== CONFIGURACIÓN INICIAL ====================
# Cargamos las variables del archivo .env donde guardamos nuestras claves secretas
load_dotenv()

# Leemos cada clave de API desde el archivo .env
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TIMEOUT = int(os.getenv("TIMEOUT", 30))  # Tiempo máximo de espera para que respondan las IAs

# Verificamos que todas las claves existan. Si falta alguna, mostramos un error.
if not all([DEEPSEEK_API_KEY, MISTRAL_API_KEY, GEMINI_API_KEY]):
    missing = []
    if not DEEPSEEK_API_KEY: missing.append("DEEPSEEK_API_KEY")
    if not MISTRAL_API_KEY: missing.append("MISTRAL_API_KEY")
    if not GEMINI_API_KEY: missing.append("GEMINI_API_KEY")
    raise ValueError(f"Faltan keys en .env: {', '.join(missing)}")

# Creamos los "clientes" que nos permiten hablar con cada IA
deepseek_client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com", timeout=TIMEOUT)
mistral_client = Mistral(api_key=MISTRAL_API_KEY, timeout_ms=TIMEOUT * 1000)
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

# Confirmamos que todo está listo para empezar a trabajar
print("✅ Todos los clientes inicializados correctamente")


# ==================== CONFIGURACIÓN DE IDIOMAS ====================
# Definimos los idiomas en que el usuario puede escribir la descripción del producto
IDIOMAS_ENTRADA = {
    "es": {"nombre": "Español", "codigo": "es", "instruccion": "La descripción del producto está en español"},
    "en": {"nombre": "Inglés", "codigo": "en", "instruccion": "The product description is in English"}
}


# ==================== CONFIGURACIÓN DE MERCADOS ====================
# Definimos los tres países donde vamos a vender: Japón, Alemania y Brasil
MERCADOS = {
    "japon": {
        "codigo_idioma": "ja",
        "nombre_pais": "Japón",
        "tono": "formal, respetuoso y con énfasis en la calidad y precisión",
        "referencias_culturales": "valoran la armonía, la cortesía y la estética minimalista",
        "saludo": "株式会社Global-Gadgetsをご覧いただきありがとうございます"
    },
    "alemania": {
        "codigo_idioma": "de",
        "nombre_pais": "Alemania",
        "tono": "directo, profesional y enfocado en datos técnicos y eficiencia",
        "referencias_culturales": "valoran la puntualidad, la precisión y la documentación clara",
        "saludo": "Sehr geehrte Kundin, sehr geehrter Kunde"
    },
    "brasil": {
        "codigo_idioma": "pt-BR",
        "nombre_pais": "Brasil",
        "tono": "cálido, enérgico y con entusiasmo, usando un lenguaje cercano",
        "referencias_culturales": "valoran la calidez humana, el carnaval y el fútbol",
        "saludo": "Olá! Bem-vindo à Global-Gadgets"
    }
}


# ==================== CONSTRUCCIÓN DE PROMPTS ====================
# Nuestro objetivo es construir mensajes claros que la IA pueda entender
# Cada función prepara una instrucción específica según el tipo de contenido que necesitamos

def construir_prompt_post(descripcion_producto, mercado, idioma_entrada="es"):
    """Preparamos el mensaje para que la IA genere un post para redes sociales"""
    config = MERCADOS[mercado]
    idioma_config = IDIOMAS_ENTRADA.get(idioma_entrada, IDIOMAS_ENTRADA["es"])
    return f"""
    Actúa como un experto en marketing localizado para {config['nombre_pais']}.
    
    IMPORTANTE: {idioma_config['instruccion']}.
    
    Nuestra tarea es crear un post para redes sociales (estilo Twitter/X) sobre el siguiente producto.
    El contenido debe estar en IDIOMA {config['codigo_idioma']} ({config['nombre_pais']}).
    
    DESCRIPCIÓN DEL PRODUCTO:
    {descripcion_producto}
    
    REQUISITOS DEL POST:
    - Máximo 280 caracteres
    - Tono: {config['tono']}
    - Incluir 2-3 hashtags relevantes para {config['nombre_pais']}
    - Adaptación cultural: {config['referencias_culturales']}
    
    Responde ÚNICAMENTE con el texto del post, sin explicaciones adicionales.
    """


def construir_prompt_email(descripcion_producto, mercado, idioma_entrada="es"):
    """Preparamos el mensaje para que la IA genere un email promocional"""
    config = MERCADOS[mercado]
    idioma_config = IDIOMAS_ENTRADA.get(idioma_entrada, IDIOMAS_ENTRADA["es"])
    return f"""
    Actúa como un redactor de email marketing especializado en {config['nombre_pais']}.
    
    IMPORTANTE: {idioma_config['instruccion']}.
    
    Nuestra tarea es escribir un email promocional en IDIOMA {config['codigo_idioma']}.
    
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


def construir_prompt_eslogans(descripcion_producto, mercado, idioma_entrada="es"):
    """Preparamos el mensaje para que la IA genere 3 eslóganes publicitarios cortos"""
    config = MERCADOS[mercado]
    idioma_config = IDIOMAS_ENTRADA.get(idioma_entrada, IDIOMAS_ENTRADA["es"])
    return f"""
Eres un experto creativo publicitario especializado en el mercado de {config['nombre_pais']}.

IMPORTANTE: {idioma_config['instruccion']}.

Nuestra tarea es generar EXACTAMENTE 3 eslóganes publicitarios para el siguiente producto:

PRODUCTO: "{descripcion_producto}"

REQUISITOS OBLIGATORIOS:
1. Los 3 eslóganes deben estar en IDIOMA {config['codigo_idioma']} ({config['nombre_pais']})
2. Cada eslogan debe tener MÁXIMO 8 palabras
3. Tono del eslogan: {config['tono']}
4. Debe incluir referencias culturales: {config['referencias_culturales']}
5. Los eslóganes deben ser creativos, memorables y persuasivos

FORMATO DE RESPUESTA (ESTRICTO):
Responde ÚNICAMENTE con los 3 eslóganes, UNO POR LÍNEA, comenzando cada línea con un guión.

Ejemplo de formato correcto:
- Silencio absoluto, batería infinita
- Escucha lo que importa
- Tecnología que te acompaña

Ahora genera los 3 eslóganes para el producto indicado, siguiendo EXACTAMENTE el formato del ejemplo.
"""


# ==================== FUNCIONES DE CONSULTA A CADA IA ====================
# Cada función se encarga de comunicarse con una IA específica.
# Medimos el tiempo que tarda cada una y manejamos los errores para que nuestra aplicación sea robusta.

def consultar_deepseek(prompt, temperatura=0.7):
    """
    Nos conectamos a Deepseek para que procese nuestro mensaje.
    Medimos el tiempo de respuesta y devolvemos el resultado en un formato uniforme.
    """
    inicio = time.time()  # Empezamos a contar el tiempo
    try:
        # Enviamos el mensaje a Deepseek
        respuesta = deepseek_client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=temperatura,  # Controlamos la creatividad de la IA
            max_tokens=500
        )
        # Calculamos cuánto tardó en responder
        return {
            "exito": True,
            "respuesta": respuesta.choices[0].message.content,
            "error": None,
            "tiempo_ms": int((time.time() - inicio) * 1000),
            "modelo": "Deepseek"
        }
    except Exception as e:
        # Si algo sale mal, registramos el error y continuamos
        return {
            "exito": False,
            "respuesta": None,
            "error": str(e),
            "tiempo_ms": int((time.time() - inicio) * 1000),
            "modelo": "Deepseek"
        }


def consultar_mistral(prompt, temperatura=0.7):
    """
    Nos conectamos a Mistral usando peticiones HTTP directas.
    Elegimos este método porque es más confiable que el SDK oficial.
    """
    import requests
    inicio = time.time()
    
    # Configuramos la petición a la API de Mistral
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistral-small-latest",  # Usamos el modelo pequeño porque es más económico
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperatura,
        "max_tokens": 500
    }
    
    try:
        # Enviamos la petición y esperamos la respuesta
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
            # Si la respuesta no es exitosa, guardamos el código de error
            return {
                "exito": False,
                "respuesta": None,
                "error": f"HTTP {response.status_code}",
                "tiempo_ms": tiempo_ms,
                "modelo": "Mistral"
            }
    except Exception as e:
        return {
            "exito": False,
            "respuesta": None,
            "error": str(e),
            "tiempo_ms": int((time.time() - inicio) * 1000),
            "modelo": "Mistral"
        }


def consultar_mistral_eslogans(prompt, temperatura=0.8):
    """
    Versión especial de Mistral para generar eslóganes.
    Usamos una temperatura más alta para que sea más creativo y menos tokens porque los eslóganes son cortos.
    """
    import requests
    inicio = time.time()
    
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistral-small-latest",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperatura,
        "max_tokens": 300  # Los eslóganes son cortos, no necesitamos muchos tokens
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
                "error": f"HTTP {response.status_code}",
                "tiempo_ms": tiempo_ms,
                "modelo": "Mistral"
            }
    except Exception as e:
        return {
            "exito": False,
            "respuesta": None,
            "error": str(e),
            "tiempo_ms": int((time.time() - inicio) * 1000),
            "modelo": "Mistral"
        }


def consultar_gemini(prompt, temperatura=0.7):
    """
    Nos conectamos a Gemini usando su SDK oficial.
    Usamos el modelo Flash Lite porque es rápido y económico.
    """
    inicio = time.time()
    try:
        # Enviamos el mensaje a Gemini
        respuesta = gemini_client.models.generate_content(
            model="gemini-3.1-flash-lite-preview",  # Modelo rápido y económico
            contents=prompt,
            config={"temperature": temperatura, "max_output_tokens": 500}
        )
        return {
            "exito": True,
            "respuesta": respuesta.text,
            "error": None,
            "tiempo_ms": int((time.time() - inicio) * 1000),
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


# ==================== TRADUCCIÓN ====================
def traducir_texto(texto, idioma_origen, idioma_destino="es"):
    """
    Traducimos el contenido generado al idioma que eligió el usuario.
    Primero intentamos con Gemini, si falla usamos Deepseek como respaldo.
    Así aseguramos que siempre tengamos una traducción disponible.
    """
    if not texto:
        return "⚠️ No hay texto para traducir"
    
    # Convertimos códigos de idioma a nombres legibles para el prompt
    idiomas_origen = {"ja": "japonés", "de": "alemán", "pt-BR": "portugués de Brasil"}
    nombre_origen = idiomas_origen.get(idioma_origen, "el idioma original")
    
    idiomas_destino = {"es": "español", "en": "inglés"}
    nombre_destino = idiomas_destino.get(idioma_destino, "español")
    
    # Construimos el mensaje de traducción
    prompt_traduccion = f"Traduce el siguiente texto del {nombre_origen} al {nombre_destino}. Mantén el tono original. Responde SOLO con la traducción:\n\n{texto}"
    
    print(f"🔍 [TRADUCCIÓN] Traduciendo de {nombre_origen} a {nombre_destino}")
    
    # Intento 1: Gemini (nuestra opción principal)
    try:
        respuesta = gemini_client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt_traduccion,
            config={"temperature": 0.3, "max_output_tokens": 800}
        )
        return respuesta.text.strip()
    except:
        # Intento 2: Deepseek (plan de respaldo si Gemini está saturado)
        try:
            respuesta = deepseek_client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": prompt_traduccion}],
                temperature=0.3,
                max_tokens=800
            )
            return respuesta.choices[0].message.content.strip()
        except:
            return f"❌ Error en traducción a {nombre_destino}"


# ==================== FUNCIÓN PRINCIPAL ====================
def generar_campana_completa(descripcion_producto, mercado, llm_seleccionado="todos", idioma_entrada="es"):
    """
    Esta es nuestra función más importante.
    Recibe la descripción del producto, el mercado objetivo, qué IA usar y el idioma.
    Genera TODO el contenido: post, email y eslóganes.
    Nuestro objetivo es devolver un diccionario organizado con todos los resultados.
    """
    # Verificamos que el mercado exista en nuestra configuración
    if mercado not in MERCADOS:
        return {"exito": False, "error": f"Mercado '{mercado}' no válido"}
    
    # Seleccionamos qué IA(s) vamos a usar según lo que eligió el usuario
    consultas_disponibles = {
        "deepseek": consultar_deepseek,
        "mistral": consultar_mistral,
        "gemini": consultar_gemini
    }
    
    if llm_seleccionado == "todos":
        llms_a_usar = consultas_disponibles.values()
        modo = "comparativa"  # Modo comparación: usamos las tres IAs
    elif llm_seleccionado in consultas_disponibles:
        llms_a_usar = [consultas_disponibles[llm_seleccionado]]
        modo = "single"  # Modo individual: usamos solo una IA
    else:
        return {"exito": False, "error": f"LLM '{llm_seleccionado}' no válido"}
    
    # Construimos los tres tipos de mensajes (post, email, eslóganes)
    prompts = {
        "post": construir_prompt_post(descripcion_producto, mercado, idioma_entrada),
        "email": construir_prompt_email(descripcion_producto, mercado, idioma_entrada),
        "eslogans": construir_prompt_eslogans(descripcion_producto, mercado, idioma_entrada)
    }
    
    # Preparamos el contenedor donde guardaremos todos los resultados
    resultados = {
        "exito": True,
        "mercado": mercado,
        "configuracion_mercado": MERCADOS[mercado],
        "modo": modo,
        "llm_utilizado": llm_seleccionado,
        "idioma_entrada": idioma_entrada,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "contenido": {}
    }
    
    # Para cada tipo de contenido (post, email, eslogans)...
    for tipo_contenido, prompt in prompts.items():
        resultados["contenido"][tipo_contenido] = {}
        for consulta_func in llms_a_usar:
            # Primero identificamos qué IA estamos usando
            prueba = consulta_func("Di hola")
            nombre_modelo = prueba.get("modelo", "desconocido")
            
            # Los eslóganes de Mistral requieren una función especial (más creativa)
            if tipo_contenido == "eslogans" and nombre_modelo == "Mistral":
                respuesta = consultar_mistral_eslogans(prompt)
            else:
                respuesta = consulta_func(prompt)
            
            respuesta_texto = respuesta.get("respuesta")
            traduccion = None
            
            # Si la respuesta fue exitosa, la traducimos al idioma que eligió el usuario
            if respuesta.get("exito") and respuesta_texto:
                codigo_idioma = MERCADOS[mercado]["codigo_idioma"]
                traduccion = traducir_texto(respuesta_texto, codigo_idioma, idioma_entrada)
                print(f"🔍 [DEBUG] Traducción solicitada a: {idioma_entrada}")
            
            # Guardamos toda la información en nuestro contenedor de resultados
            resultados["contenido"][tipo_contenido][nombre_modelo] = {
                "respuesta": respuesta_texto,
                "traduccion": traduccion,
                "exito": respuesta.get("exito"),
                "error": respuesta.get("error"),
                "tiempo_ms": respuesta.get("tiempo_ms")
            }
    
    return resultados


def comparar_llms_para_contenido(descripcion_producto, mercado, tipo_contenido="post"):
    """
    Esta función nos permite comparar cómo responden las tres IAs
    para un tipo de contenido específico (solo post, solo email o solo eslóganes).
    Nuestro objetivo es ayudar al usuario a elegir qué IA genera mejor contenido.
    """
    constructores = {
        "post": construir_prompt_post,
        "email": construir_prompt_email,
        "eslogans": construir_prompt_eslogans
    }
    
    if tipo_contenido not in constructores:
        return {"exito": False, "error": f"Tipo '{tipo_contenido}' no válido"}
    
    # Construimos el mensaje para el tipo de contenido solicitado
    prompt = constructores[tipo_contenido](descripcion_producto, mercado)
    
    # Preparamos el contenedor de resultados
    resultados = {
        "exito": True,
        "mercado": mercado,
        "tipo_contenido": tipo_contenido,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "respuestas": {}
    }
    
    # Consultamos a cada IA y guardamos sus respuestas
    for nombre, func in [("Deepseek", consultar_deepseek), ("Mistral", consultar_mistral), ("Gemini", consultar_gemini)]:
        respuesta = func(prompt)
        resultados["respuestas"][nombre] = {
            "respuesta": respuesta.get("respuesta"),
            "exito": respuesta.get("exito"),
            "error": respuesta.get("error"),
            "tiempo_ms": respuesta.get("tiempo_ms")
        }
    
    return resultados


# ==================== PRUEBA LOCAL ====================
# Este bloque solo se ejecuta cuando corremos este archivo directamente
# (no cuando es importado desde api.py)
if __name__ == "__main__":
    print("🧪 Prueba de servicios...")
    producto = "Auriculares con cancelación de ruido, 40h de batería"
    resultado = generar_campana_completa(producto, "brasil", "todos")
    if resultado["exito"]:
        print("✅ Prueba exitosa")
    else:
        print(f"❌ Error: {resultado.get('error')}")
