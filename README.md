# 🌍 Polyglot - Asistente de Marketing Multilingüe con IA

**Polyglot** es una aplicación web que genera contenido de marketing localizado para Brasil 🇧🇷, Japón 🇯🇵 y Alemania 🇩🇪. Utiliza tres motores de IA (Deepseek, Mistral y Gemini) para crear posts para redes sociales, emails promocionales y eslóganes publicitarios, adaptando el tono y las referencias culturales a cada país.

---

## 📋 Requisitos Previos

- Python 3.13 o superior
- Cuentas en [Deepseek](https://platform.deepseek.com/), [Mistral AI](https://mistral.ai/) y [Google AI Studio](https://aistudio.google.com/) para obtener las API Keys.

---

## 🛠 Configuración del Proyecto

### 1. Clonar el repositorio

```bash
git clone https://github.com/luiscarlos1986vr-del/polyglot-app.git
cd polyglot-app
```

### 2. Crear y activar entorno virtual

- **Windows:**
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```
- **Mac/Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```ini
DEEPSEEK_API_KEY=tu_clave_de_deepseek
MISTRAL_API_KEY=tu_clave_de_mistral
GEMINI_API_KEY=tu_clave_de_gemini
TIMEOUT=30
```

> ⚠️ **Importante:** Nunca subas el archivo `.env` a GitHub. Ya está incluido en `.gitignore`.

---

## 🔑 Guía Detallada para Obtener las API Keys

### Deepseek API Key

1. **Registro:** Ve a [Deepseek Platform](https://platform.deepseek.com/) y regístrate con tu correo electrónico.
2. **Verificación:** Verifica tu correo electrónico a través del enlace que recibirás.
3. **Dashboard:** Inicia sesión y ve al Dashboard.
4. **Generar API Key:** Selecciona "API Keys" en el menú lateral, haz clic en "Create API Key", asígnale un nombre (ej: "Polyglot") y copia la clave generada (comienza con `sk-...`).
5. **Guardar:** Guarda esta clave en un lugar seguro y añádela al archivo `.env` como `DEEPSEEK_API_KEY`.

### Mistral API Key

1. **Registro:** Ve a [Mistral AI Platform](https://mistral.ai/) y regístrate.
2. **Verificación:** Verifica tu correo electrónico.
3. **Plan Gratuito:** Ve a Admin → Subscriptions, selecciona "Experiment for free", acepta los términos y verifica tu número de teléfono.
4. **Workspace:** Crea un Workspace.
5. **Generar API Key:** Ve a "Workspace settings" → "API Keys", haz clic en "Create new key", asígnale un nombre y copia la clave generada.
6. **Guardar:** Guarda esta clave en un lugar seguro y añádela al archivo `.env` como `MISTRAL_API_KEY`.

### Gemini API Key

1. **Registro:** Ve a [Google AI Studio](https://aistudio.google.com/) e inicia sesión con tu cuenta de Google.
2. **Términos:** Acepta los términos y condiciones.
3. **Generar API Key:** Haz clic en "Create API Key", selecciona "Gemini API" y el proyecto (puedes crear uno nuevo si es necesario).
4. **Guardar:** Copia la clave generada (comienza con `AIza...`) y guárdala en un lugar seguro. Añádela al archivo `.env` como `GEMINI_API_KEY`.

---

## 🚀 Ejecución Local

Necesitas **dos terminales** abiertas: una para el backend y otra para el frontend.

1. **Iniciar el servidor backend (API):**
  ```bash
   python api.py
  ```
   Verás un mensaje indicando que el servidor está corriendo en `http://localhost:5000`.
2. **Iniciar la interfaz de usuario (Frontend):**
  ```bash
   streamlit run interfaz_polyglot.py
  ```
   Se abrirá automáticamente tu navegador en `http://localhost:8501`.

---

## ☁️ Despliegue en la Nube

El proyecto está configurado para desplegarse en **Render** (backend) y **Streamlit Cloud** (frontend), ambos con planes gratuitos.

1. **Backend (Render):**
  - Sube tu código a GitHub (sin el archivo `.env`).
  - Crea un **Web Service** en Render conectado a tu repositorio.
  - Configura:
    - **Build Command:** `pip install -r requirements.txt`
    - **Start Command:** `python api.py`
    - Añade las variables de entorno con tus API Keys.
2. **Frontend (Streamlit Cloud):**
  - Conecta Streamlit Cloud al mismo repositorio.
  - Configura el archivo principal como `interfaz_polyglot.py`.
  - Actualiza la variable `API_URL` en el código con la URL de Render.

---

## 🛠 Tecnologías Utilizadas

- **Python 3.13** - Lenguaje base del proyecto
- **Streamlit** - Interfaz de usuario interactiva
- **Flask** - Servidor API para comunicación backend
- **Deepseek API, Mistral API, Gemini API** - Motores de IA para generación de contenido
- **Render y Streamlit Cloud** - Despliegue en la nube

---

## 📜 Licencia

Este proyecto es de uso académico y educativo.
