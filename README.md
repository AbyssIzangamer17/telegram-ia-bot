# Telegram IA Bot

> Bot de Telegram con IA creado completamente con OpenCode AI, usando OpenRouter y OpenClaw.

[![Python 3.12+](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-2CA5E0?logo=telegram)](https://core.telegram.org/bots)
[![OpenRouter](https://img.shields.io/badge/OpenRouter-Gateway-FF6B35?logo=openai)](https://openrouter.ai/)
[![Created with OpenCode](https://img.shields.io/badge/Created%20with-OpenCode-00D4AA)](https://opencode.ai/)

## Descripción

Bot de Telegram desarrollado íntegramente mediante prompts a OpenCode AI. Combina procesamiento de lenguaje natural (NLP) con un sistema multi-agente extensible. Utiliza modelos LLM de última generación (GPT-4o-mini vía OpenRouter) para mantener conversaciones naturales y ejecutar tareas complejas como búsqueda web, análisis de productos, consulta del clima y más.

**Nota importante**: Este proyecto no tiene código escrito manualmente. Todo fue generado por OpenCode AI siguiendo especificaciones profesionales de prompts.

## Proceso de Creación

Para conocer el detalle completo de cómo se creó este bot (desde el formateo del ordenador con Linux Mint hasta la implementación final), consulta el documento [**CREACION.md**](CREACION.md).

Resumen del proceso:
1. Formateo del ordenador e instalación de Linux Mint
2. Instalación de OpenCode AI
3. Generación del bot mediante prompts profesionales a OpenCode

**Autor**: Izan Urios  

## Características Principales

### 🤖 Conversación Inteligente
- Integración con OpenRouter AI (soporte para múltiples modelos)
- Detección automática de intención (búsqueda, clima, noticias, precios)
- Respuestas con formato Markdown y emojis
- Historial de conversación para contexto

### 🔍 Búsqueda y Web
- Búsqueda web multi-fuente (Google, Bing, DuckDuckGo)
- Scraping inteligente de URLs
- Análisis de productos y comparación de precios
- Noticias en tiempo real (Bing News)

### 🌡️ Clima y Tiempo
- Consulta del clima actual (wttr.in API gratuita)
- Soporte para cualquier ciudad del mundo
- Datos detallados: temperatura, humedad, viento

### 🧠 Sistema Multi-Agente
12 agentes especializados que trabajan en pipeline:
- **Orchestrator**: Planifica qué agentes ejecutar
- **Researcher**: Búsqueda web especializada
- **Analyzer**: Análisis de productos y precios
- **Writer**: Redacción de respuestas
- **System**: Información del sistema (CPU, RAM, disco)
- **Scraper**: Extracción de contenido web
- **Summarizer**: Resúmenes de textos largos
- **Filter**: Filtrado de resultados duplicados
- **Compare**: Comparación de productos con tablas
- **Alert**: Monitoreo y alertas del sistema
- **News**: Búsqueda de noticias
- **Weather**: Consulta de clima

### 🎓 Fine-Tuning Expert
- Gestión de proyectos de fine-tuning
- Preparación de datos en formato JSONL
- Generación de datos sintéticos vía LLM
- Validación de datos y estimación de costes
- Recomendación de modelos según caso de uso

### 📝 Productividad Diaria
- **Notas rápidas**: Guarda y recupera notas
- **Lista de compras**: Gestiona lista de supermercado
- **Pomodoro Timer**: Temporizador de productividad
- **Mood Tracking**: Registro de estado de ánimo (1-10)
- **Expense Tracker**: Control de gastos diarios
- **Ideas**: Captura de ideas rápidas

### 🔔 Recordatorios Inteligentes
- Sistema de recordatorios con APScheduler
- Parsing de tiempo natural ("in 2 hours", "tomorrow at 9:00")
- Soporte para recordatorios one-time y recurrentes
- Persistencia en archivos JSON

### 🎙️ Voz Integrada
- **Speech-to-Text**: Whisper para transcribir notas de voz
- **Text-to-Speech**: gTTS para leer respuestas en audio
- Activación automática (configurable)

## Instalación

### Prerrequisitos
- Python 3.12+
- Token de Telegram Bot (obtener de [@BotFather](https://t.me/BotFather))
- API Key de OpenRouter (registrarse en [openrouter.ai](https://openrouter.ai/))

### Pasos

1. Clonar el repositorio:
```bash
git clone <repo-url>
cd telegram-ia-bot-plus
```

2. Instalar dependencias:
```bash
pip install python-telegram-bot requests beautifulsoup4 gtts faster-whisper apscheduler psutil duckduckgo-search httpx
```

3. Configurar variables de entorno:
```bash
export TELEGRAM_TOKEN="tu_token_aqui"
export OPENROUTER_API_KEY="tu_openrouter_key_aqui"
```

4. Ejecutar el bot:
```bash
python3 telegram_bot.py
```

Para asegurar una sola instancia:
```bash
./run_bot.sh
```

## Uso

### Comandos Principales

| Comando | Descripción |
|----------|-------------|
| `/start` | Inicia el bot y muestra mensaje de bienvenida |
| `/help` | Muestra ayuda detallada y todos los comandos |
| `/hora` | Muestra fecha y hora actual (Madrid) |
| `/clima [ciudad]` | Consulta el clima actual (ej: `/clima Madrid`) |
| `/pipe <tarea>` | Ejecuta pipeline multi-agente automático |
| `/agent <tipo> <tarea>` | Usa un agente específico |
| `/agents` | Lista todos los agentes disponibles |
| `/remind <msg> in <tiempo>` | Crea un recordatorio |
| `/reminders` | Ver recordatorios activos |
| `/note <text>` | Guarda una nota rápida |
| `/ftcreate <nombre>` | Crea proyecto de fine-tuning |
| `/ftgen <tema> <num>` | Genera datos sintéticos |

### Ejemplos de Conversación

```
Usuario: Busca noticias recientes sobre IA
Bot: 🔍 *Resultados de búsqueda web:*
    1. **Últimos avances en IA generativa**
       Los modelos de lenguaje han evolucionado...
       🔗 https://...

Usuario: Qué hora es?
Bot: 🕒 *Fecha y hora actual (Madrid):*
     • Fecha: martes, 5 de mayo de 2026
     • Hora: 20:30:45

Usuario: Clima en Barcelona
Bot: ☀️ *Clima en Barcelona, Spain*
     🌡️ Temperatura: 22°C (sensación 21°C)
     💧 Humedad: 65%
     💨 Viento: 12 km/h
```

## Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│                 TELEGRAM IA BOT PLUS                  │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌──────────────┐    ┌────────┐ │
│  │  Telegram    │    │   Multi-     │    │ Fine-  │ │
│  │  Bot Core    │◄──►│   Agent      │◄──►│ Tuning │ │
│  │  (Main)      │    │   Pipeline   │    │ Expert │ │
│  └──────┬──────┘    └──────┬───────┘    └────┬───┘ │
│         │                   │                   │       │
│         ▼                   ▼                   ▼       │
│  ┌─────────────┐    ┌──────────────┐    ┌────────┐ │
│  │ OpenRouter  │    │ 12 Specialized│   │ Training│ │
│  │ API (LLM)   │    │ Agents        │   │ Data    │ │
│  └─────────────┘    └──────────────┘    └────────┘ │
└─────────────────────────────────────────────────────────┘
```

## Estructura del Proyecto

```
/home/izan/
├── telegram_bot.py          # Bot principal (~236 líneas)
├── multi_agent_pipeline.py  # Sistema multi-agente (~844 líneas)
├── fine_tuning_expert.py   # Sistema fine-tuning (~438 líneas)
├── remote_control.sh        # Panel acceso remoto
├── run_bot.sh              # Script ejecución con lock file
├── docs/
│   └── adr/              # Architecture Decision Records
│       ├── README.md
│       ├── 0001-openrouter-llm-gateway.md
│       ├── 0002-multi-agent-pipeline-pattern.md
│       ├── 0003-single-bot-instance-lock.md
│       ├── 0004-environment-variables-secrets.md
│       └── 0005-async-http-requests.md
├── PRODUCTION_AUDIT_REPORT.md  # Auditoría completa
├── TECHNICAL_MEMORY.md         # Memoria técnica exhaustiva
└── README.md                   # Este archivo
```

## Tecnologías Utilizadas

- **Lenguaje**: Python 3.12
- **Bot Framework**: python-telegram-bot v20+
- **LLM Gateway**: OpenRouter AI
- **Modelo Principal**: GPT-4o-mini
- **HTTP Client**: requests (migrando a httpx para async)
- **Web Scraping**: BeautifulSoup4, DuckDuckGo Search
- **Voz**: Whisper (STT), gTTS (TTS)
- **Scheduling**: APScheduler
- **Sistema**: psutil

## Estado del Proyecto

| Aspecto | Estado | Notas |
|---------|--------|-------|
| Funcionalidad Core | ✅ Completo | Chat, búsqueda, clima, noticias |
| Multi-Agent Pipeline | ✅ Completo | 12 agentes implementados |
| Fine-Tuning Expert | ✅ Completo | Gestión de proyectos y datos |
| Productividad | ✅ Completo | Notas, compras, pomodoro, mood |
| Seguridad | ⚠️ En progreso | Moviendo secrets a env vars |
| Testing | ❌ Pendiente | 0% coverage, necesita pytest |
| Documentación | ✅ Completo | README, ADRs, memoria técnica |
| Producción | ⚠️ En progreso | Falta Docker, CI/CD, monitoring |

## Próximas Mejoras

- [ ] Mover API keys a variables de entorno (ADR-0004)
- [ ] Implementar rate limiting para APIs
- [ ] Migrar a httpx para requests async (ADR-0005)
- [ ] Escribir tests (target 80% coverage)
- [ ] Añadir Dockerfile y docker-compose
- [ ] Configurar CI/CD pipeline
- [ ] Implementar health check endpoint
- [ ] Añadir structured logging (structlog)
- [ ] Integración con Google Calendar
- [ ] Fine-tuning real con datos recogidos

## Contribución

Este es un proyecto personal, pero siéntete libre de:
1. Hacer fork del proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## Recursos

- [Documentación de python-telegram-bot](https://docs.python-telegram-bot.org/)
- [OpenRouter API Docs](https://openrouter.ai/docs)
- [Beautiful Soup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [APScheduler Docs](https://apscheduler.readthedocs.io/)

---

**Desarrollado con ❤️ por [Izan](https://github.com/izan) usando [OpenCode AI](https://opencode.ai/)**
