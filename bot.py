import os
import logging
import pandas as pd
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# --- 1. CONFIGURACIÓN DE VARIABLES Y SEGURIDAD DE LOGS ---
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
RENDER_URL = os.getenv("URL_RENDER", "https://tu-app.onrender.com")
ENTORNO = os.getenv("ENTORNO", "produccion") 
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "secreto_super_seguro") 

if not TOKEN:
    print("❌ ERROR: Falta el TELEGRAM_TOKEN en el entorno. Apagando...")
    exit(1)

# Configuración base de logs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# 🛡️ ESCUDO 1: Silenciar las peticiones HTTP de la librería 'httpx'
logging.getLogger("httpx").setLevel(logging.WARNING)

# 🛡️ ESCUDO 2: Filtro global para ocultar el token si alguna otra librería intenta imprimirlo
class TokenRedactorFilter(logging.Filter):
    def filter(self, record):
        msg = record.getMessage()
        if TOKEN in msg:
            record.msg = msg.replace(TOKEN, "***TOKEN_TELEGRAM_OCULTO***")
            record.args = () 
        return True

# Aplicar el filtro a todos los logs
logger = logging.getLogger()
for handler in logger.handlers:
    handler.addFilter(TokenRedactorFilter())


# --- 2. CONFIGURACIÓN DEL MODELO DE MACHINE LEARNING (TF-IDF) ---
datos = {
    "Personaje": ["Toño", "Zac", "Pablo", "Gil", "Beca", "Pau", "Anisha", "Gary", "Rogelio", "Roy", "Lisa", "Alonso", "Oscar", "Erica", "Loren", "Gina", "Olga", "Paco", "Laura", "Julio", "Rich", "Kati", "Fer", "Cori"],
    "Descripcion": [
        "Chico rubio juega baloncesto ropa verde tiene balon",
        "Chico juega hockey usa casco azul ropa azul tiene stick",
        "Chico cabello castaño juega esqui ropa amarilla gorro",
        "Chica cabello castaño juega futbol ropa azul",
        "Chica rubio juega baloncesto ropa verde tiene balon",
        "Chica cabello negro natacion traje azul gafas de buceo",
        "Chica pelo azul juega golf ropa blanca lleva palos",
        "Chico cabello castaño juega tenis ropa blanca raqueta",
        "Chico juega baloncesto ropa amarilla usa cintillo",
        "Chico pelirrojo juega futbol ropa roja tiene balon",
        "Chica pelo azul juega futbol ropa amarilla usa cintillo",
        "Chico cabello negro juega golf ropa azul usa visera palos",
        "Chico cabello negro juega hockey ropa roja tiene stick",
        "Chica cabello castaño juega tenis ropa blanca usa visera raqueta",
        "Chica rubio juega golf ropa verde usa visera palos",
        "Chica cabello castaño juega voleibol ropa amarilla usa cintillo balon",
        "Chica pelirrojo juega esqui ropa azul usa gorro",
        "Chico rubio juega tenis ropa roja tiene raqueta",
        "Chica cabello negro juega futbol ropa roja tiene balon",
        "Chico pelo azul juega futbol ropa blanca tiene balon",
        "Chico pelirrojo juega baloncesto ropa roja tiene balon",
        "Chica cabello negro juega esqui ropa amarilla usa gorro",
        "Chica pelirrojo juega voleibol ropa blanca usa cintillo balon",
        "Chica cabello negro juega golf ropa roja usa gorra y usa visera palos"
    ]
}

df = pd.DataFrame(datos)
vectorizador = TfidfVectorizer()
matriz_tfidf = vectorizador.fit_transform(df['Descripcion'])

def predecir_personaje_avanzado(descripcion_usuario):
    vector_usuario = vectorizador.transform([descripcion_usuario])
    similitudes = cosine_similarity(vector_usuario, matriz_tfidf)[0] 
    
    indices_ordenados = similitudes.argsort()[::-1]
    
    top_1_idx = indices_ordenados[0]
    top_1_score = similitudes[top_1_idx]
    top_1_name = df.iloc[top_1_idx]['Personaje']
    
    if top_1_score >= 0.15:
        return True, top_1_name, top_1_score
    else:
        top_2_idx = indices_ordenados[1]
        top_2_name = df.iloc[top_2_idx]['Personaje']
        return False, [top_1_name, top_2_name], top_1_score

# --- 3. ESTADOS DE LA CONVERSACIÓN ---
PREGUNTA_JUGAR, GENERO, PELO, DEPORTE, ROPA, ACCESORIO, CONFIRMAR_GANADOR, ELEGIR_SUPOSICION = range(8)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    teclado = [['Sí, quiero jugar 🎮', 'No, en otro momento ❌']]
    markup = ReplyKeyboardMarkup(teclado, resize_keyboard=True, one_time_keyboard=True)
    
    await update.message.reply_text(
        "🤖 ¡Hola! Soy tu asistente de Machine Learning.\n\n"
        "¿Quieres jugar el juego de *Who is Who* (Quién es Quién)?",
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN
    )
    return PREGUNTA_JUGAR

async def inicio_juego(update: Update, context: ContextTypes.DEFAULT_TYPE):
    respuesta = update.message.text
    
    if 'No' in respuesta:
        await update.message.reply_text("¡Entendido! Avísame con /start cuando quieras jugar.", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
        
    try:
        with open('asset/imagen_personajes.jpg', 'rb') as foto:
            await update.message.reply_photo(
                photo=foto, 
                caption="Selecciona en tu mente un personaje de la imagen. ¡No me digas su nombre!\n\nTe haré unas preguntas para adivinarlo."
            )
    except FileNotFoundError:
        await update.message.reply_text("[Nota: La imagen general no se encontró en asset/imagen_personajes.jpg, pero sigamos]")

    teclado = [['Chico', 'Chica']]
    markup = ReplyKeyboardMarkup(teclado, resize_keyboard=True, one_time_keyboard=True)
    
    await update.message.reply_text("1️⃣ Primero, ¿cuál es su **género**?", reply_markup=markup, parse_mode=ParseMode.MARKDOWN)
    return GENERO

async def preguntar_pelo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['genero'] = update.message.text
    teclado = [['Rubio', 'Castaño', 'Negro'], ['Pelirrojo', 'Azul', 'Cubierto/No se ve']]
    markup = ReplyKeyboardMarkup(teclado, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text("2️⃣ ¿Qué color de **pelo** tiene?", reply_markup=markup, parse_mode=ParseMode.MARKDOWN)
    return PELO

async def preguntar_deporte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['pelo'] = update.message.text
    teclado = [['Baloncesto 🏀', 'Fútbol ⚽', 'Tenis 🎾'], ['Esquí ⛷️', 'Golf ⛳', 'Hockey 🏒'], ['Voleibol 🏐', 'Natación 🏊']]
    markup = ReplyKeyboardMarkup(teclado, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text("3️⃣ ¿Qué **deporte** está practicando?", reply_markup=markup, parse_mode=ParseMode.MARKDOWN)
    return DEPORTE

async def preguntar_ropa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['deporte'] = update.message.text.split(' ')[0] 
    teclado = [['Verde', 'Azul', 'Amarilla'], ['Roja', 'Blanca']]
    markup = ReplyKeyboardMarkup(teclado, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text("4️⃣ ¿De qué color es su **ropa** principal?", reply_markup=markup, parse_mode=ParseMode.MARKDOWN)
    return ROPA

async def preguntar_accesorio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['ropa'] = update.message.text
    teclado = [['Balón', 'Stick', 'Raqueta', 'Palos de golf'], ['Gorro de nieve', 'Gafas de buceo', 'Casco'], ['Visera', 'Cintillo', 'Gorra', 'Ninguno']]
    markup = ReplyKeyboardMarkup(teclado, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text("5️⃣ Por último, ¿qué **accesorio** o implemento tiene?", reply_markup=markup, parse_mode=ParseMode.MARKDOWN)
    return ACCESORIO

async def procesar_prediccion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    accesorio = update.message.text
    if accesorio == 'Ninguno': accesorio = ""
    
    frase_usuario = f"{context.user_data['genero']} {context.user_data['pelo']} juega {context.user_data['deporte']} ropa {context.user_data['ropa']} {accesorio}"
    context.user_data['frase_generada'] = frase_usuario
    
    await update.message.reply_text("🧠 Analizando tus respuestas...", reply_markup=ReplyKeyboardRemove())
    
    es_confiable, resultado, score = predecir_personaje_avanzado(frase_usuario)
    
    if es_confiable:
        personaje = resultado
        try:
            ruta_imagen = f"asset/{personaje}.jpg"
            with open(ruta_imagen, 'rb') as foto:
                await update.message.reply_photo(photo=foto, caption=f"¡Es **{personaje}**! 🎯\n(Confianza: {score*100:.1f}%)", parse_mode=ParseMode.MARKDOWN)
        except FileNotFoundError:
            await update.message.reply_text(f"¡Es **{personaje}**! 🎯\n(Confianza: {score*100:.1f}%)\n\n_[No pude cargar la imagen de {personaje}.jpg]_", parse_mode=ParseMode.MARKDOWN)

        teclado = [['Sí 🎉', 'No 🤨']]
        markup = ReplyKeyboardMarkup(teclado, resize_keyboard=True, one_time_keyboard=True)
        await update.message.reply_text("¿Este es el personaje que seleccionaste?", reply_markup=markup)
        
        return CONFIRMAR_GANADOR
        
    else:
        opcion1, opcion2 = resultado
        teclado = [[opcion1, opcion2]]
        markup = ReplyKeyboardMarkup(teclado, resize_keyboard=True, one_time_keyboard=True)
        
        await update.message.reply_text(
            f"Hmm... Esa combinación es rara. Tu nivel de coincidencia es súper bajo ({score*100:.1f}%).\n\n"
            f"Pero mi red neuronal dice que tiene que ser uno de estos dos. ¿Cuál de los dos elegiste?",
            reply_markup=markup
        )
        return ELEGIR_SUPOSICION

async def confirmar_ganador(update: Update, context: ContextTypes.DEFAULT_TYPE):
    respuesta = update.message.text
    
    if 'Sí' in respuesta:
        await update.message.reply_text("¡Excelente! Mi algoritmo no falla. 🤖🔥\n\nPresiona /start para jugar de nuevo.", reply_markup=ReplyKeyboardRemove())
    else:
        frase = context.user_data.get('frase_generada', '')
        await update.message.reply_text(f"¡Imposible! Seguro me diste las pistas mal. Esto es lo que entendí: _{frase}_\n\nPresiona /start para la revancha.", parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
        
    context.user_data.clear()
    return ConversationHandler.END

async def tiguere_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    personaje_elegido = update.message.text
    
    try:
        ruta_imagen = f"asset/{personaje_elegido}.jpg"
        with open(ruta_imagen, 'rb') as foto:
            await update.message.reply_photo(photo=foto)
    except FileNotFoundError:
        pass 

    await update.message.reply_text(
        f"¡Aja! Quisiste ser más tíguere que yo, pero sabía que estabas dando las descripciones mal. 😎🇩🇴\n\n"
        f"Presiona /start para jugar de nuevo sin hacer trampa.",
        reply_markup=ReplyKeyboardRemove()
    )
    context.user_data.clear()
    return ConversationHandler.END

async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Juego cancelado. Presiona /start para volver a empezar.", reply_markup=ReplyKeyboardRemove())
    context.user_data.clear()
    return ConversationHandler.END

# --- 4. ARRANQUE DEL BOT ---
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto_about = (
        "🤖 *Acerca de este Bot: ¿Quién es Quién? (Edición AI)*\n\n"
        "Soy un bot interactivo impulsado por *Machine Learning* y *Procesamiento de Lenguaje Natural (NLP)*.\n\n"
        "🧠 *¿Cómo funciono?*\n"
        "Convierto tus respuestas en vectores matemáticos usando *TF-IDF* y aplico *Similitud del Coseno* para encontrar al personaje en mi base de datos con mayor porcentaje de coincidencia.\n\n"
        "🛠️ *Tecnologías:*\n"
        "• Python\n"
        "• Scikit-Learn\n"
        "• Pandas\n\n"
        "👨‍💻 *Propósito:*\n"
        "Demostrar el despliegue en producción de un modelo de Machine Learning real."
    )
    await update.message.reply_text(texto_about, parse_mode=ParseMode.MARKDOWN)

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 10000))
    app = ApplicationBuilder().token(TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            PREGUNTA_JUGAR: [MessageHandler(filters.TEXT & ~filters.COMMAND, inicio_juego)],
            GENERO: [MessageHandler(filters.TEXT & ~filters.COMMAND, preguntar_pelo)],
            PELO: [MessageHandler(filters.TEXT & ~filters.COMMAND, preguntar_deporte)],
            DEPORTE: [MessageHandler(filters.TEXT & ~filters.COMMAND, preguntar_ropa)],
            ROPA: [MessageHandler(filters.TEXT & ~filters.COMMAND, preguntar_accesorio)],
            ACCESORIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, procesar_prediccion)],
            CONFIRMAR_GANADOR: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirmar_ganador)],
            ELEGIR_SUPOSICION: [MessageHandler(filters.TEXT & ~filters.COMMAND, tiguere_check)]
        },
        fallbacks=[CommandHandler('cancelar', cancelar)]
    )
    
    app.add_handler(CommandHandler("about", about))
    app.add_handler(conv_handler)
    
    if ENTORNO == "local":
        print("Iniciando bot en modo LOCAL (Polling)...")
        app.run_polling(allowed_updates=[Update.MESSAGE])
    else:
        print("Iniciando bot en modo NUBE (Webhook protegido)...")
        app.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            webhook_url=f"{RENDER_URL}/{TOKEN}",
            url_path=TOKEN,
            secret_token=WEBHOOK_SECRET, 
            allowed_updates=[Update.MESSAGE]
        )