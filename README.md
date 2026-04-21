# 🌍 Polyglot - Asistente de Marketing Multilingüe con IA

**Polyglot** es una aplicación web que genera contenido de marketing localizado para tres mercados internacionales: **Brasil 🇧🇷, Japón 🇯🇵 y Alemania 🇩🇪**. Utiliza tres motores de IA (Deepseek, Mistral y Gemini) para crear posts para redes sociales, emails promocionales y eslóganes publicitarios, adaptando el tono y las referencias culturales a cada país.

## Requisitos Previos

Asegúrate de tener instalado en tu sistema: **Python 3.9 o superior** ([Descargar](https://www.python.org/downloads/)), **Git** ([Descargar](https://git-scm.com/)) y una cuenta de correo electrónico para crear las cuentas en los servicios de IA.

## Estructura del Proyecto

polyglot-app/
│
├── interfaz_polyglot.py # Interfaz de usuario (Streamlit)
├── api.py # Servidor backend (Flask)
├── estructura_servicios_poliglot_.py # Lógica de negocio y conexión con IAs
├── requirements.txt # Dependencias del proyecto
├── .env # Archivo con API Keys (NO se sube a GitHub)
└── .gitignore # Archivos ignorados por Git


## Configuración Inicial

**1. Clonar el repositorio:** Abre una terminal y ejecuta `git clone https://github.com/luiscarlos1986vr-del/polyglot-app.git` y luego `cd polyglot-app`.

**2. Crear y activar un entorno virtual:** En Windows ejecuta `python -m venv venv` y luego `venv\Scripts\activate`. En Mac/Linux ejecuta `python3 -m venv venv` y luego `source venv/bin/activate`.

**3. Instalar dependencias:** Ejecuta `pip install -r requirements.txt`.

**4. Configurar variables de entorno:** Crea un archivo llamado **`.env`** en la raíz del proyecto (junto a `api.py`) con el siguiente contenido:
```env
DEEPSEEK_API_KEY=tu_clave_de_deepseek
MISTRAL_API_KEY=tu_clave_de_mistral
GEMINI_API_KEY=tu_clave_de_gemini
TIMEOUT=30

⚠️ NUNCA subas el archivo .env a GitHub. Ya está incluido en .gitignore.

Obtención de API Keys
Todas las claves se obtienen de forma gratuita (con límites de uso mensuales).

🔑 Deepseek API Key: Regístrate en Deepseek Platform, verifica tu correo, inicia sesión, ve al Dashboard, selecciona "API Keys", haz clic en "Create API Key", asígnale un nombre (ej: "Polyglot") y copia la clave (comienza con sk-...). Guárdala en un lugar seguro.

🔑 Mistral API Key: Regístrate en Mistral AI Platform, verifica tu correo, activa el plan gratuito (Admin → Subscriptions → "Experiment for free", acepta términos y verifica tu número de teléfono), crea un Workspace, ve a "Workspace settings → API Keys", haz clic en "Create new key", asigna un nombre y copia la clave.

🔑 Gemini API Key: Accede a Google AI Studio, inicia sesión con tu cuenta de Google, acepta los términos, haz clic en "Create API Key", selecciona "Gemini API" y el proyecto (puedes crear uno nuevo) y copia la clave (comienza con AIza...).

Ejecución Local
Necesitas dos terminales abiertas porque el backend y el frontend corren por separado.

1. Iniciar el servidor backend (API): En la primera terminal, con el entorno virtual activado, ejecuta python api.py. Verás un mensaje indicando que el servidor está corriendo en http://localhost:5000. No cierres esta terminal.

2. Iniciar la interfaz de usuario (Frontend): En la segunda terminal, con el entorno virtual activado, ejecuta streamlit run interfaz_polyglot.py. Se abrirá automáticamente tu navegador en http://localhost:8501. ¡La aplicación está lista para usar!

Despliegue en la Nube
El proyecto está configurado para desplegarse en Render (backend) y Streamlit Cloud (frontend), ambos con planes gratuitos. Para desplegar: sube tu código a GitHub (sin el archivo .env), crea un Web Service en Render conectado a tu repositorio (Build Command: pip install -r requirements.txt, Start Command: python api.py, agrega las variables de entorno con tus API Keys), luego conecta Streamlit Cloud al mismo repositorio (Main file: interfaz_polyglot.py) y actualiza API_URL en el código con la URL de Render.

Tecnologías Utilizadas
Python 3.13 - Lenguaje base del proyecto

Streamlit - Interfaz de usuario interactiva

Flask - Servidor API para comunicación backend

Deepseek API - Motor de IA para generación de contenido

Mistral API - Motor de IA para generación de contenido

Gemini API - Motor de IA para generación de contenido y traducción

Render - Despliegue del backend en la nube

Streamlit Cloud - Despliegue del frontend en la nube

Autores
Luis Valencia - Arquitectura y desarrollo backend

Mauro Patiño - Interfaz de usuario y experiencia visual

Proyecto final del Diplomado Python - Universidad de los Hemisferios, Quito, Ecuador

Licencia
Este proyecto es de uso académico y educativo.
