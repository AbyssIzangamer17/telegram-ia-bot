import logging
import os
import requests
from datetime import datetime
import re
from urllib.parse import quote
from zoneinfo import ZoneInfo
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

TOKEN = os.getenv("TELEGRAM_TOKEN", "")
OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def search_web(query: str, num_results: int = 3) -> str:
    """Búsqueda web en tiempo real usando DDGS"""
    try:
        from ddgs import DDGS
        
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=num_results))
            
            if results:
                formatted = []
                for i, r in enumerate(results, 1):
                    title = r.get('title', 'Sin título')
                    body = r.get('body', '')[:300]
                    href = r.get('href', '')
                    formatted.append(f"{i}. **{title}**\n   {body}...\n   🔗 {href}")
                
                return "🔍 *Resultados de búsqueda web:*\n\n" + "\n\n".join(formatted)
        
        return "❌ No se encontraron resultados."
    except Exception as e:
        logger.error(f"Search error: {e}")
        return f"❌ Error en búsqueda: {e}"

# Siempre hacer búsqueda para cualquier pregunta que no sea saludo simple
SEARCH_KEYWORDS = ['?', 'qué', 'que', 'quién', 'quien', 'cuándo', 'cuando', 
                'dónde', 'donde', 'cómo', 'como', 'por qué', 'porque',
                'noticia', 'noticias', 'busca', 'buscar', 'buscame', 'actual', 'reciente',
                'precio', 'precios', 'clima', 'tiempo', 'temperatura', 
                'último', 'última', 'cuánto', 'qué pasó', 'qué pasa',
                'dame', 'información', 'google', 'web', 'internet',
                'sucedió', 'pasó', 'ocurrió', 'ocurre', 'hoy', 'ayer',
                'semana', 'mes', 'año', '2024', '2025', '2026',
                'diario', 'periódico', 'mundo', 'españa', 'internacional',
                'última hora', 'breaking', 'news', 'latest']

TIME_DATE_KEYWORDS = ['hora', 'horas', 'tiempo', 'fecha', 'fechas', 'día', 'días', 'mes', 'año',
                     'qué hora', 'qué día', 'qué fecha', 'cuál es la hora', 'cuál es la fecha',
                     'fecha actual', 'hora actual', 'fecha de hoy', 'hora de hoy', 'día de hoy',
                     'qué día es hoy', 'qué fecha es hoy', 'cuánto tiempo', 'ayer', 'mañana',
                     'semana', 'mes', 'año', 'calendario', 'reloj', 'ahora mismo', 'en este momento']

async def start(update, context):
    await update.message.reply_text(
        "🤖 *¡Hola! Soy tu Bot IA* 🤖\n\n"
        "Puedes hablarme con naturalidad. ¡Pruebame!",
        parse_mode="Markdown"
    )

async def help_command(update, context):
    help_text = "📖 *Guía completa del Bot IA*\n\n"
    
    help_text += "*📌 Comandos disponibles:*\n"
    help_text += "• `/start` - Inicia el bot y muestra mensaje de bienvenida\n"
    help_text += "• `/help` - Muestra esta ayuda detallada\n"
    help_text += "• `/status` - Ver el estado actual del bot\n"
    help_text += "• `/hora` - Muestra fecha y hora actual (Madrid)\n"
    help_text += "• `/clima [ciudad]` - Consulta el clima actual (ej: `/clima Madrid`)\n\n"
    
    help_text += "*🤖 Funciones inteligentes:*\n"
    help_text += "• *IA integrada*: Respondo con inteligencia artificial a cualquier mensaje\n"
    help_text += "• *Detección de fecha/hora*: Escribe 'qué hora es' o 'qué día es' y te respondo automáticamente\n"
    help_text += "• *Búsqueda web*: Busco en internet cuando preguntas por noticias, precios, clima, etc.\n"
    help_text += "• *Clima en tiempo real*: Usa `/clima` seguido de la ciudad para saber el clima\n\n"
    
    help_text += "*💡 Ejemplos de uso:*\n"
    help_text += "• \"Hola, ¿cómo estás?\" → Te respondo con IA\n"
    help_text += "• \"¿Qué hora es?\" → Te doy la hora actual\n"
    help_text += "• \"Busca noticias actuales\" → Busco en internet\n"
    help_text += "• `/clima Barcelona` → Clima actual en Barcelona\n"
    help_text += "• \"¿Cuánto cuesta el iPhone 15?\" → Busco precios\n\n"
    
    help_text += "*🌍 Configuración:*\n"
    help_text += "• Zona horaria: Madrid, España\n"
    help_text += "• Bot activo 24/7 con reinicio automático cada 6h"
    
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def status(update, context):
    now = datetime.now()
    status_msg = "🤖 *Estado del Bot*\n\n"
    status_msg += "*Bot:*\n"
    status_msg += "• Estado: 🟢 Activo\n"
    status_msg += f"• Fecha: {now.strftime('%d/%m/%Y')}\n"
    status_msg += f"• Hora: {now.strftime('%H:%M:%S')}\n"
    await update.message.reply_text(status_msg, parse_mode="Markdown")

async def hora_comando(update, context):
    now = datetime.now(ZoneInfo("Europe/Madrid"))
    fecha = now.strftime("%A, %d de %B de %Y")
    hora = now.strftime("%H:%M:%S")
    time_msg = "🕒 *Fecha y hora actual (Madrid):*\n\n"
    time_msg += f"• Fecha: {fecha}\n"
    time_msg += f"• Hora: {hora}\n\n"
    time_msg += "🌍 Zona horaria: Madrid, España"
    await update.message.reply_text(time_msg, parse_mode="Markdown")

async def clima_comando(update, context):
    if not context.args:
        await update.message.reply_text(
            "🌤️ *Consulta del clima*\n\n"
            "Usa: `/clima [ciudad]`\n"
            "Ejemplo: `/clima Madrid`\n"
            "Ejemplo: `/clima Barcelona, España`",
            parse_mode="Markdown"
        )
        return
    
    ciudad = " ".join(context.args)
    await update.message.reply_text(f"🌤️ Consultando clima en {ciudad}...")
    
    try:
        # Using wttr.in - free weather API, no key needed
        url = f"https://wttr.in/{quote(ciudad)}?format=j1"
        response = requests.get(url, timeout=10, headers={'User-Agent': 'curl/7.68.0'})
        
        if response.status_code == 200:
            data = response.json()
            current = data['current_condition'][0]
            area = data['nearest_area'][0]
            
            ciudad_nombre = f"{area['areaName'][0]['value']}, {area['country'][0]['value']}"
            temp = current['temp_C']
            feels_like = current['FeelsLikeC']
            humidity = current['humidity']
            wind = current['windspeedKmph']
            desc = current['weatherDesc'][0]['value']
            
            # Weather emoji
            if 'sun' in desc.lower() or 'clear' in desc.lower():
                emoji = "☀️"
            elif 'rain' in desc.lower() or 'lluvia' in desc.lower():
                emoji = "🌧️"
            elif 'cloud' in desc.lower() or 'nube' in desc.lower():
                emoji = "☁️"
            elif 'snow' in desc.lower():
                emoji = "❄️"
            else:
                emoji = "🌤️"
            
            msg = f"{emoji} *Clima en {ciudad_nombre}*\n\n"
            msg += f"• Temperatura: {temp}°C\n"
            msg += f"• Sensación térmica: {feels_like}°C\n"
            msg += f"• Descripción: {desc}\n"
            msg += f"• Humedad: {humidity}%\n"
            msg += f"• Viento: {wind} km/h"
            
            await update.message.reply_text(msg, parse_mode="Markdown")
        else:
            await update.message.reply_text("❌ No pude encontrar esa ciudad. Intenta con otra.")
    except Exception as e:
        logger.error(f"Weather error: {e}")
        await update.message.reply_text(f"❌ Error al consultar el clima: {e}")


async def handle(update, context):
    chat_id = update.message.chat_id
    text = update.message.text
    logger.info(f"Received: {text}")
    
    await update.message.chat.send_action("typing")
    
    # Check if asking ONLY for time/date (simple queries)
    text_lower = text.lower()
    if text_lower in ['qué hora es', 'que hora es', 'hora', 'fecha', 'día', 'qué día es hoy', 'que día es hoy'] or text_lower.startswith('hora') or text_lower.startswith('fecha'):
        await hora_comando(update, context)
        return
    
    # Check if we need web search (cualquier pregunta con ?, qué, quién, etc.)
    needs_search = any(kw in text.lower() for kw in SEARCH_KEYWORDS)
    
    if needs_search:
        await update.message.reply_text("🔍 Buscando en internet...")
        search_result = search_web(text)
        logger.info(f"Search result for '{text}': {search_result[:200]}...")
        if "❌" not in search_result:
            # Mostrar resultados directamente
            await update.message.reply_text(search_result[:4000], parse_mode="Markdown")
            return
        else:
            logger.warning(f"Search failed for: {text}")
            await update.message.reply_text("❌ No pude buscar en internet en este momento. Por favor, intenta más tarde.")
            return
    
    # Para saludos y conversación casual, usar IA
    try:
        now = datetime.now(ZoneInfo("Europe/Madrid"))
        date_str = now.strftime("%A, %d de %B de %Y, %H:%M horas")
        
        system_content = f"Eres un asistente útil. La fecha y hora actual es: {date_str}. "
        system_content += "Responde de forma concisa. Usa emojis. "
        system_content += "INSTRUCCIÓN OBLIGATORIA: Cuando se te proporcionen resultados de búsqueda web, "
        system_content += "ESA ES TU ÚNICA FUENTE DE INFORMACIÓN. "
        system_content += "NUNCA digas que no tienes información reciente o que tu conocimiento tiene fecha límite. "
        system_content += "Los resultados de búsqueda SON la información actual."
        
        messages = [{"role": "system", "content": system_content}]
        messages.append({"role": "user", "content": text})
        
        headers = {"Authorization": f"Bearer {OPENROUTER_KEY}", "Content-Type": "application/json"}
        data = {
            "model": "openai/gpt-4o-mini",
            "messages": messages,
            "max_tokens": 600,
            "temperature": 0.7
        }
        r = requests.post(OPENROUTER_URL, headers=headers, json=data, timeout=30)
        result = r.json()
        if "choices" in result and len(result["choices"]) > 0:
            ai_response = result["choices"][0]["message"]["content"]
            # Improve formatting
            if not any(emoji in ai_response for emoji in ["🤖", "✅", "📌", "🔍", "😊", "💡"]):
                ai_response = "🤖 " + ai_response
            await update.message.reply_text(ai_response[:4000], parse_mode="Markdown")
        else:
            await update.message.reply_text("😅 No pude procesar eso. ¿Puedes repetir?")
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text(f"😅 Error: {e}")

def main():
    logger.info("Iniciando bot...")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("hora", hora_comando))
    app.add_handler(CommandHandler("clima", clima_comando))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    logger.info("Bot iniciado - esperando mensajes...")
    app.run_polling(allowed_updates=["message", "edited_message"])

if __name__ == "__main__":
    main()
