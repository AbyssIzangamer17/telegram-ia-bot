# Telegram IA Bot

> Bot de Telegram con IA creado completamente con OpenCode AI, usando OpenRouter y OpenClaw.

[![Python 3.12+](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-2CA5E0?logo=telegram)](https://core.telegram.org/bots)
[![OpenRouter](https://img.shields.io/badge/OpenRouter-Gateway-FF6B35?logo=openai)](https://openrouter.ai/)
[![Created with OpenCode](https://img.shields.io/badge/Created%20with-OpenCode-00D4AA)](https://opencode.ai/)

## Descripción

Bot de Telegram desarrollado íntegramente mediante prompts a OpenCode AI. Utiliza modelos LLM de última generación (GPT-4o-mini vía OpenRouter) para mantener conversaciones naturales y ejecutar tareas como búsqueda web, consulta del clima y más.

**Nota importante**: Este proyecto no tiene código escrito manualmente. Todo fue generado por OpenCode AI siguiendo las especificaciones dadas en los prompts.

## Características Principales

### 🤖 Conversación Inteligente
- Integración con OpenRouter AI (GPT-4o-mini)
- Respuestas con formato Markdown y emojis
- Historial de conversación para contexto

### 🔍 Búsqueda Web
- Búsqueda web en tiempo real usando DuckDuckGo
- Detección automática de preguntas que requieren búsqueda
- Resultados formateados con títulos, descripciones y enlaces

### 🌡️ Clima y Tiempo
- Consulta del clima actual usando wttr.in (API gratuita, sin key necesaria)
- Soporte para cualquier ciudad del mundo
- Datos detallados: temperatura, sensación térmica, humedad, viento

### 🕒 Fecha y Hora
- Consulta de fecha y hora actual (zona horaria Madrid)
- Detección automática de preguntas sobre tiempo/fecha

## Instalación

### Prerrequisitos
- Python 3.12+
- Token de Telegram Bot (obtener de [@BotFather](https://t.me/BotFather))
- API Key de OpenRouter (registrarse en [openrouter.ai](https://openrouter.ai/))

### Pasos

1. Clonar el repositorio:
```bash
git clone https://github.com/AbyssIzangamer17/telegram-ia-bot.git
cd telegram-ia-bot
```

2. Instalar dependencias:
```bash
pip install python-telegram-bot requests duckduckgo-search --break-system-packages
```

3. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env y poner tus tokens
```

4. Ejecutar el bot:
```bash
python3 telegram_bot.py
```

## Uso

### Comandos Disponibles

| Comando | Descripción |
|---------|-------------|
| `/start` | Inicia el bot y muestra mensaje de bienvenida |
| `/help` | Muestra ayuda detallada y todos los comandos |
| `/status` | Ver el estado actual del bot |
| `/hora` | Muestra fecha y hora actual (Madrid) |
| `/clima [ciudad]` | Consulta el clima actual (ej: `/clima Madrid`) |

### Ejemplos de Conversación

```
Usuario: Hola, ¿cómo estás?
Bot: 🤖 ¡Hola! Estoy bien, gracias por preguntar. ¿En qué puedo ayudarte?

Usuario: ¿Qué hora es?
Bot: 🕒 *Fecha y hora actual (Madrid):*
     • Fecha: miércoles, 6 de mayo de 2026
     • Hora: 20:45:30

Usuario: Busca noticias sobre IA
Bot: 🔍 *Resultados de búsqueda web:*
     1. **Últimos avances en IA...**
        Los modelos de lenguaje han evolucionado...
        🔗 https://...

Usuario: /clima Barcelona
Bot: ☀️ *Clima en Barcelona, Spain*
     • Temperatura: 22°C
     • Sensación térmica: 21°C
     • Humedad: 65%
     • Viento: 12 km/h
```

## Estructura del Proyecto

```
/home/izan/
├── telegram_bot.py          # Bot principal (~250 líneas)
├── requirements.txt         # Dependencias de Python
├── .env.example           # Ejemplo de variables de entorno
├── .gitignore             # Archivos excluidos del repo
├── README.md              # Este archivo
├── CREACION.md            # Documento con proceso de creación
└── bot_output.log         # Logs del bot (no subido al repo)
```

## Tecnologías Utilizadas

- **Lenguaje**: Python 3.12
- **Bot Framework**: python-telegram-bot v20+
- **LLM Gateway**: OpenRouter AI
- **Modelo Principal**: GPT-4o-mini
- **Web Search**: DuckDuckGo Search
- **Clima**: wttr.in API
- **HTTP Client**: requests

## Proceso de Creación

Para conocer el detalle completo de cómo se creó este bot (desde el formateo del ordenador con Linux Mint hasta la implementación final), consulta el documento [**CREACION.md**](CREACION.md).

**Autor**: Izan Urios  
**Fecha**: Mayo 2026  
**Herramienta utilizada**: OpenCode AI (opencode.ai)
