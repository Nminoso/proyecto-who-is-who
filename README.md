🤖 Who is Who: Edición AI (Telegram Bot)
Un bot interactivo para Telegram que reinventa el clásico juego de adivinar personajes ("Quién es Quién") utilizando Machine Learning y Procesamiento de Lenguaje Natural (NLP). En lugar de reglas simples, este bot utiliza vectores matemáticos para procesar las descripciones de los usuarios y predecir en qué personaje están pensando.

✨ Características Principales
Motor de Inteligencia Artificial: Utiliza TfidfVectorizer y Similitud del Coseno (vía Scikit-Learn) para calcular el nivel de coincidencia entre las pistas del usuario y el dataset de 24 personajes deportivos.

Flujo Conversacional Dinámico: Implementa ConversationHandler para guiar al usuario paso a paso recopilando datos (género, pelo, deporte, ropa y accesorios).

El "Tíguere Check" (Manejo de Baja Confianza): Si el usuario proporciona pistas contradictorias o inventadas (confianza < 15%), el algoritmo lo detecta, evita dar un falso positivo y le ofrece al usuario sus dos mejores suposiciones con un toque de humor.

Respuestas Visuales: Carga y envía dinámicamente imágenes individuales de los personajes desde la carpeta local al acertar.

Entornos Flexibles: Soporta modo Polling para pruebas locales y Webhook seguro para despliegue en la nube (ej. Render).

🔛 Demostración en vivo
¡Pon a prueba el algoritmo! Puedes jugar con el bot en vivo aquí:

👉 https://t.me/wsw2026bot

📦 Archivos del Proyecto
bot.py – Código principal de la aplicación (Python asíncrono con la API de Telegram y Scikit-Learn).

asset/ – Carpeta obligatoria que contiene la imagen general (imagen_personajes.jpg) y las 24 imágenes individuales de los personajes (ej. Toño.jpg, Beca.jpg).

.env – Variables de entorno para Tokens y configuración de entorno (No subir a Git).

requirements.txt – Dependencias del proyecto (pandas, scikit-learn, python-telegram-bot, etc.).

.gitignore – Configuración para excluir archivos sensibles y basura (caché, entornos virtuales).

README.md – Esta guía de configuración y uso.

🧰 Requisitos
Python 3.11.x (Recomendado)

Windows, macOS, o Linux.

Telegram Bot Token (Obtenido de @BotFather en Telegram).

Cuenta en Render (Opcional, para alojamiento en la nube mediante Webhooks).

⚠️ Nota de Compatibilidad
Este proyecto ha sido testeado con Python 3.11.9.

Se recomienda evitar Python 3.12+ en Windows para prevenir conflictos de dependencias con algunas librerías de Machine Learning y red.

⚙️ Configuración (Ambiente Virtual)
Se recomienda encarecidamente el uso de un entorno virtual para mantener las dependencias (como Pandas y Scikit-Learn) aisladas del sistema principal.

1. Clonar y preparar carpeta
Crea tu carpeta de proyecto, coloca los archivos proporcionados y asegúrate de incluir la carpeta asset/ con todas las imágenes.

2. Crear y activar ambiente virtual
Windows (PowerShell):

PowerShell
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
macOS / Linux (bash/zsh):

Bash
python3.11 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

3. Configurar variables de entorno
Crea un archivo llamado .env en la raíz del proyecto con el siguiente formato:

Fragmento de código
TELEGRAM_TOKEN=tu_telegram_bot_token_aqui
ENTORNO=local
# Variables para producción (Render)
URL_RENDER=https://tu-app.onrender.com
WEBHOOK_SECRET=tu_secreto_personalizado

4. Ejecución del Bot
Una vez configurado el .env y con el ambiente virtual activo, ejecuta:

Bash
python bot.py