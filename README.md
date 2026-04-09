# 🤖 Who is Who: Edición AI (Telegram Bot)
Un bot interactivo para Telegram que reinventa el clásico juego de adivinar personajes ("Quién es Quién") utilizando Machine Learning y Procesamiento de Lenguaje Natural (NLP). En lugar de reglas simples, este bot utiliza vectores matemáticos para procesar las descripciones de los usuarios y predecir en qué personaje están pensando.

---

## ✨ Características Principales
- **Motor de Inteligencia Artificial:** Utiliza TfidfVectorizer y Similitud del Coseno (vía Scikit-Learn) para calcular el nivel de coincidencia entre las pistas del usuario y el dataset de 24 personajes deportivos.
- **Flujo Conversacional Dinámico:** Implementa ConversationHandler para guiar al usuario paso a paso recopilando datos (género, pelo, deporte, ropa y accesorios).
- **El "Tíguere Check" (Manejo de Baja Confianza):** Si el usuario proporciona pistas contradictorias o inventadas (confianza < 15%), el algoritmo lo detecta, evita dar un falso positivo y le ofrece al usuario sus dos mejores suposiciones con un toque de humor.
- **Respuestas Visuales:** Carga y envía dinámicamente imágenes individuales de los personajes desde la carpeta local al acertar.
- **Seguridad Robusta:** Enmascaramiento de tokens en consola, Secret Token para Webhooks y filtrado de eventos permitidos.
- **Entornos Flexibles:** Soporta modo `Polling` para pruebas locales y `Webhook` para despliegue en la nube (Render).

---

## 🔛 Demostración en vivo
¡Pon a prueba el algoritmo! Puedes jugar con el bot en vivo aquí: 
👉 https://t.me/wsw2026bot

---

## 📦 Archivos del Proyecto
- `bot.py` – Aplicación principal del bot (Python asíncrono con la API de Telegram y Scikit-Learn con seguridad reforzada).
- `.env` – Variables de entorno para Tokens, API Keys y configuración de entorno (No subir a Git).
- `requirements.txt` – Dependencias del proyecto (Versiones estables, incluye soporte para webhooks y requests).
- `.gitignore` – Configuración para excluir archivos sensibles y basura.
- `README.md` – Guía de configuración y uso.

---

## 🧰 Requisitos
- **Python 3.11.x (Recomendado)**
- Windows, macOS, o Linux.
- Telegram Bot Token (Obtenido de @BotFather).
- Groq API Key (Obtenida de Groq Cloud).
- Cuenta en Render (Opcional, para alojamiento en la nube).

---

## ⚠️ Nota de Compatibilidad

Este proyecto ha sido testeado con **Python 3.11.9**.

- Se recomienda evitar Python 3.12+ en Windows para prevenir conflictos de dependencias con algunas librerías de red.

---

## ⚙️ Configuración (Ambiente Virtual)

- Se recomienda encarecidamente el uso de un entorno virtual para mantener las dependencias aisladas.

### 1. Clonar y preparar carpeta
- Crea tu carpeta de proyecto y coloca los archivos proporcionados.

### 2. Crear y activar ambiente virtual

**Windows (PowerShell):**
```powershell
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

**macOS / Linux (bash/zsh):**
```
python3.11 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```
### 3. Configurar variables de entorno
- Crea un archivo llamado `.env` en la raíz del proyecto con el siguinete formato:

```
TELEGRAM_TOKEN=tu_token_de_telegram_aqui
ENTORNO=local

# Las siguientes variables son exclusivas para producción (Render)
URL_RENDER= Escribe la URL completa que Render te asignó en el paso anterior (ej. https://who-is-who-bot.onrender.com). Asegúrate de no poner / al final.
WEBHOOK_SECRET=	Inventa una contraseña segura y sin espacios. Esto protege tu bot de peticiones falsas.
ENTORNO=	Escribe: produccion
PYTHON_VERSION=	Escribe: 3.11.9 (Esto obliga a Render a usar una versión compatible)
TELEGRAM_TOKEN= Pega aquí el token de tu bot que te dio @BotFather
```
Nota: Para ejecutar localmente en tu PC, asegúrate de que `ENTORNO=local` para activar el modo Polling.
