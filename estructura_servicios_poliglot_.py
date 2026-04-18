# -*- coding: utf-8 -*-
"""
estructura_servicios_poliglot.py - Capa de Servicios del Proyecto Polyglot
"""

import os
import time
from dotenv import load_dotenv
from openai import OpenAI
from mistralai.client import Mistral
from google import genai

# ==================== CONFIGURACIÓN INICIAL ====================
# Cargar variables del archivo .env
load_dotenv()

# Configuración de API keys
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TIMEOUT = int(os.getenv("TIMEOUT", 30))

# Validación de keys
if not all([DEEPSEEK_API_KEY, MISTRAL_API_KEY, GEMINI_API_KEY]):
    missing = []
    if not DEEPSEEK_API_KEY: missing.append("DEEPSEEK_API_KEY")
    if not MISTRAL_API_KEY: missing.append("MISTRAL_API_KEY")
    if not GEMINI_API_KEY: missing.append("GEMINI_API_KEY")
    raise ValueError(f"Faltan keys en .env: {', '.join(missing)}")

# Inicializar clientes
deepseek_client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com",
    timeout=TIMEOUT
)

mistral_client = Mistral(
    api_key=MISTRAL_API_KEY,
    timeout_ms=TIMEOUT * 1000
)

gemini_client = genai.Client(api_key=GEMINI_API_KEY)

print("✅ Todos los clientes inicializados correctamente")


# ==================== CONFIGURACIÓN DE MERCADOS ====================
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
def construir_prompt_post(descripcion_producto, mercado):
    config = MERCADOS[mercado]
    return f"""
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


def construir_prompt_email(descripcion_producto, mercado):
    config = MERCADOS[mercado]
    return f"""
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


def construir_prompt_eslogans(descripcion_producto, mercado):
    config = MERCADOS[mercado]
    return f"""
Eres un experto creativo publicitario especializado en el mercado de {config['nombre_pais']}.

Tu tarea es generar EXACTAMENTE 3 eslóganes publicitarios para el siguiente producto:

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


# ==================== FUNCIONES DE CONSULTA ====================
def consultar_deepseek(prompt, temperatura=0.7):
    inicio = time.time()
    try:
        respuesta = deepseek_client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=temperatura,
            max_tokens=500
        )
        return {
            "exito": True,
            "respuesta": respuesta.choices[0].message.content,
            "error": None,
            "tiempo_ms": int((time.time() - inicio) * 1000),
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
    import requests
    inicio = time.time()
    
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistral-small-latest",  # Usar modelo más económico
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
        "max_tokens": 300
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
    inicio = time.time()
    try:
        respuesta = gemini_client.models.generate_content(
            model="gemini-2.5-flash-lite",
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


# ==================== FUNCIÓN PRINCIPAL ====================
def generar_campana_completa(descripcion_producto, mercado, llm_seleccionado="todos"):
    if mercado not in MERCADOS:
        return {"exito": False, "error": f"Mercado '{mercado}' no válido"}
    
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
        return {"exito": False, "error": f"LLM '{llm_seleccionado}' no válido"}
    
    prompts = {
        "post": construir_prompt_post(descripcion_producto, mercado),
        "email": construir_prompt_email(descripcion_producto, mercado),
        "eslogans": construir_prompt_eslogans(descripcion_producto, mercado)
    }
    
    resultados = {
        "exito": True,
        "mercado": mercado,
        "configuracion_mercado": MERCADOS[mercado],
        "modo": modo,
        "llm_utilizado": llm_seleccionado,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "contenido": {}
    }
    
    for tipo_contenido, prompt in prompts.items():
        resultados["contenido"][tipo_contenido] = {}
        for consulta_func in llms_a_usar:
            prueba = consulta_func("Di hola")
            nombre_modelo = prueba.get("modelo", "desconocido")
            
            if tipo_contenido == "eslogans" and nombre_modelo == "Mistral":
                respuesta = consultar_mistral_eslogans(prompt)
            else:
                respuesta = consulta_func(prompt)
            
            respuesta_texto = respuesta.get("respuesta")
            traduccion = None
            if respuesta.get("exito") and respuesta_texto:
                codigo_idioma = MERCADOS[mercado]["codigo_idioma"]
                traduccion = traducir_a_espanol(respuesta_texto, codigo_idioma)
            
            resultados["contenido"][tipo_contenido][nombre_modelo] = {
                "respuesta": respuesta_texto,
                "traduccion": traduccion,
                "exito": respuesta.get("exito"),
                "error": respuesta.get("error"),
                "tiempo_ms": respuesta.get("tiempo_ms")
            }
    
    return resultados


# ==================== TRADUCCIÓN ====================
def traducir_a_espanol(texto, idioma_origen):
    if not texto:
        return "⚠️ No hay texto para traducir"
    
    idiomas = {"ja": "japonés", "de": "alemán", "pt-BR": "portugués de Brasil"}
    nombre_idioma = idiomas.get(idioma_origen, "el idioma original")
    
    prompt_traduccion = f"Traduce el siguiente texto del {nombre_idioma} al español. Mantén el tono original. Responde SOLO con la traducción:\n\n{texto}"
    
    try:
        respuesta = gemini_client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt_traduccion,
            config={"temperature": 0.3, "max_output_tokens": 800}
        )
        return respuesta.text.strip()
    except:
        try:
            respuesta = deepseek_client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": prompt_traduccion}],
                temperature=0.3,
                max_tokens=800
            )
            return respuesta.choices[0].message.content.strip()
        except:
            return f"❌ Error en traducción"


def comparar_llms_para_contenido(descripcion_producto, mercado, tipo_contenido="post"):
    constructores = {
        "post": construir_prompt_post,
        "email": construir_prompt_email,
        "eslogans": construir_prompt_eslogans
    }
    
    if tipo_contenido not in constructores:
        return {"exito": False, "error": f"Tipo '{tipo_contenido}' no válido"}
    
    prompt = constructores[tipo_contenido](descripcion_producto, mercado)
    
    resultados = {
        "exito": True,
        "mercado": mercado,
        "tipo_contenido": tipo_contenido,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "respuestas": {}
    }
    
    for nombre, func in [("Deepseek", consultar_deepseek), ("Mistral", consultar_mistral), ("Gemini", consultar_gemini)]:
        respuesta = func(prompt)
        resultados["respuestas"][nombre] = {
            "respuesta": respuesta.get("respuesta"),
            "exito": respuesta.get("exito"),
            "error": respuesta.get("error"),
            "tiempo_ms": respuesta.get("tiempo_ms")
        }
    
    return resultados


if __name__ == "__main__":
    print("🧪 Prueba de servicios...")
    producto = "Auriculares con cancelación de ruido, 40h de batería"
    resultado = generar_campana_completa(producto, "brasil", "todos")
    if resultado["exito"]:
        print("✅ Prueba exitosa")
    else:
        print(f"❌ Error: {resultado.get('error')}")
