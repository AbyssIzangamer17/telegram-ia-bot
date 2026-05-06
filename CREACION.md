# Proceso de Creación del Bot de Telegram IA

**Autor**: Izan Urios  
**Fecha**: Mayo 2026  
**Descripción**: Documento que detalla todo el proceso de creación del bot, desde la preparación del sistema hasta su implementación final con OpenCode.

---

## 1. Formateo del Ordenador e Instalación de Linux Mint

**1.- Prompt**:  
> "Necesito formatear mi ordenador e instalar Linux Mint. Quiero hacerlo desde un USB bootable. ¿Cómo procedo?"

**2.- Resultado**:  
Se creó un USB bootable con Linux Mint usando herramientas como Rufus o Etcher. Se procedió al formateo completo del disco duro e instalación limpia de Linux Mint en el sistema.

**3.- Problemas que ocasionó**:  
- Pérdida de datos anteriores en el disco duro (solucionado haciendo backup previo).
- Configuración inicial de drivers y periféricos tras la instalación.

**4.- Prompt que lo solucionó**:  
> "Ayúdame a configurar los drivers básicos y el sistema después de instalar Linux Mint para dejarlo listo para desarrollo."

---

## 2. Instalación de OpenCode

**1.- Prompt**:  
> "Quiero instalar OpenCode en Linux Mint. Necesito que me proporciones los pasos para instalarlo correctamente y verificar que funciona."

**2.- Resultado**:  
Se instaló OpenCode mediante los comandos apropiados para Linux Mint (basado en Ubuntu). Se verificó la instalación ejecutando `opencode --version` y configurando el entorno inicial.

**3.- Problemas que ocasionó**:  
- Dependencias faltantes en el sistema base de Linux Mint.

**4.- Prompt que lo solucionó**:  
> "Instala las dependencias necesarias para OpenCode en Linux Mint que falten en el sistema."

---

## 3. Creación del Bot de Telegram con OpenRouter, OpenClaw y Telegram

### 3.1. Prompt Inicial - Creación del Bot Básico

**1.- Prompt**:  
> "Actúa como un ingeniero de software senior especializado en bots de Telegram y sistemas IA. Necesito que crees un bot de Telegram completo y profesional que utilice OpenRouter como gateway para múltiples modelos LLM y que se integre con OpenClaw para capacidades avanzadas. El bot debe cumplir con los siguientes requisitos:
>
> 1. **Funcionalidades Core**:
>    - Integración con Telegram Bot API usando python-telegram-bot
>    - Integración con OpenRouter para acceso a modelos GPT-4o-mini y otros
>    - Detección inteligente de intenciones (búsqueda web, clima, noticias, precios)
>    - Historial de conversación para mantener contexto
>
> 2. **Capacidades de Búsqueda**:
>    - Búsqueda web en tiempo real usando DuckDuckGo
>    - Consulta de clima usando wttr.in API (sin necesidad de API key)
>    - Scraping inteligente de URLs cuando sea necesario
>
> 3. **Requisitos Técnicos**:
>    - Código Python limpio siguiendo PEP 8
>    - Manejo de errores robusto con logging
>    - Variables de entorno para tokens y API keys (usar os.getenv)
>    - Estructura modular y extensible
>    - Soporte para comandos: /start, /help, /clima, /hora, /status
>
> 4. **Formato de Respuesta**:
>    - Usar Markdown en las respuestas de Telegram
>    - Incluir emojis apropiados para mejorar UX
>    - Respuestas concisas pero informativas
>
> Por favor, genera el código completo del bot listo para ejecutar."

**2.- Resultado**:  
Se generó el archivo `telegram_bot.py` con una implementación completa que incluye:
- Integración con Telegram Bot API
- Conexión a OpenRouter para modelos LLM
- Búsqueda web con DuckDuckGo
- Consulta de clima con wttr.in
- Comandos básicos implementados
- Manejo de errores y logging

**3.- Problemas que ocasionó**:  
- Las API keys estaban hardcodeadas en el código (problema de seguridad).
- Faltaban algunas dependencias en el archivo de requisitos.

**4.- Prompt que lo solucionó**:  
> "Modifica el código del bot para que las API keys (Telegram Token y OpenRouter Key) se lean exclusivamente desde variables de entorno usando os.getenv. Crea también un archivo .env.example con las variables necesarias. Asegúrate de que el .gitignore excluya el archivo .env para no subir secrets a GitHub."

---

### 3.2. Prompt - Sistema Multi-Agente

**1.- Prompt**:  
> "Como ingeniero de sistemas experto en arquitecturas multi-agente, extiende el bot de Telegram actual para implementar un sistema de 12 agentes especializados que trabajen en pipeline. Los agentes deben ser:
>
> 1. **Orchestrator**: Planifica qué agentes ejecutar según la tarea
> 2. **Researcher**: Búsqueda web especializada
> 3. **Analyzer**: Análisis de productos y precios
> 4. **Writer**: Redacción de respuas completas
> 5. **System**: Información del sistema (CPU, RAM, disco)
> 6. **Scraper**: Extracción de contenido web
> 7. **Summarizer**: Resúmenes de textos largos
> 8. **Filter**: Filtrado de resultados duplicados
> 9. **Compare**: Comparación de productos con tablas
> 10. **Alert**: Monitoreo y alertas del sistema
> 11. **News**: Búsqueda de noticias especializada
> 12. **Weather**: Consulta de clima especializada
>
> Requisitos:
> - Cada agente debe ser una clase independiente
> - Comunicación entre agentes mediante un pipeline central
> - El Orchestrator debe decidir qué agentes activar
> - Logging detallado de cada paso del pipeline
> - Manejo de errores entre agentes
>
> Genera el código completo en un archivo `multi_agent_pipeline.py`."

**2.- Resultado**:  
Se creó el archivo `multi_agent_pipeline.py` con la implementación de los 12 agentes especializados y el sistema de pipeline centralizado.

---

### 3.3. Prompt - Sistema de Fine-Tuning

**1.- Prompt**:  
> "Actúa como un experto en machine learning e implementa un sistema de fine-tuning integrado en el bot. El sistema debe:
>
> 1. **Gestión de Proyectos**: Crear, listar y gestionar proyectos de fine-tuning
> 2. **Preparación de Datos**: Convertir datos al formato JSONL requerido
> 3. **Generación Sintética**: Usar LLM para generar datos de entrenamiento
> 4. **Validación**: Verificar que los datos estén correctamente formateados
> 5. **Estimación de Costes**: Calcular costes de entrenamiento
> 6. **Recomendación**: Sugerir el mejor modelo según el caso de uso
>
> Implementa comandos como `/ftcreate`, `/ftgen`, `/ftlist`, etc.
> Crea el archivo `fine_tuning_expert.py` con toda la funcionalidad."

**2.- Resultado**:  
Se generó `fine_tuning_expert.py` con el sistema completo de gestión de fine-tuning.

---

### 3.4. Prompt - Funcionalidades de Productividad

**1.- Prompt**:  
> "Agrega al bot de Telegram un módulo de productividad diaria con las siguientes funciones:
>
> - **Notas rápidas**: Guardar y recuperar notas (`/note`, `/notes`)
> - **Lista de compras**: Gestionar lista del supermercado (`/shop`, `/shoplist`)
> - **Pomodoro Timer**: Temporizador de productividad (`/pomodoro`)
> - **Mood Tracking**: Registro de estado de ánimo del 1 al 10 (`/mood`)
> - **Expense Tracker**: Control de gastos diarios (`/expense`, `/expenses`)
> - **Ideas**: Captura rápida de ideas (`/idea`, `/ideas`)
>
> Toda la información debe persistir en archivos JSON. Usa el sistema de archivos local para almacenamiento."

**2.- Resultado**:  
Se implementaron todas las funcionalidades de productividad integrándolas en el bot principal.

---

### 3.5. Prompt - Sistema de Recordatorios

**1.- Prompt**:  
> "Implementa un sistema de recordatorios inteligente para el bot de Telegram usando APScheduler. Los recordatorios deben:
>
> - Permitir parsing de tiempo natural: 'in 2 hours', 'tomorrow at 9:00', 'next Friday'
> - Soporte para recordatorios one-time y recurrentes
> - Persistencia en archivos JSON para sobrevivir reinicios
> - Comandos: `/remind`, `/reminders`, `/delreminder`
>
> Asegúrate de que el bot pueda enviar el recordatorio incluso si el usuario no ha interactuado recientemente."

**2.- Resultado**:  
Se integró el sistema de recordatorios con APScheduler y persistencia JSON.

---

### 3.6. Prompt - Integración de Voz

**1.- Prompt**:  
> "Añade capacidades de voz al bot de Telegram:
>
> 1. **Speech-to-Text**: Usar Whisper para transcribir notas de voz recibidas
> 2. **Text-to-Speech**: Usar gTTS para leer respuestas en audio cuando el usuario lo pida
> 3. Activación configuable (puede activarse/desactivarse)
>
> Comandos: `/voice on/off`, y transcripción automática de mensajes de voz."

**2.- Resultado**:  
Se integraron las capacidades de voz usando faster-whisper y gTTS.

---

### 3.7. Prompt - Scripts de Utilidad y Documentación

**1.- Prompt**:  
> "Crea los siguientes scripts de utilidad para el bot:
>
> 1. `run_bot.sh`: Script para ejecutar el bot asegurando una sola instancia usando lock files
> 2. `remote_control.sh`: Panel de acceso remoto para gestionar el bot
> 3. `generate_pdf.py`: Script para generar documentación en PDF
> 4. `README.md`: Documentación completa del proyecto con badges, tablas, ejemplos de uso
> 5. `TECHNICAL_MEMORY.md`: Memoria técnica exhaustiva de todo el proyecto
> 6. `PRODUCTION_AUDIT_REPORT.md`: Auditoría completa de producción
>
> Asegúrate de que toda la documentación esté en español y sea profesional."

**2.- Resultado**:  
Se generaron todos los scripts y documentación solicitada con un nivel de calidad profesional.

---

## Resumen del Proceso

Todo el desarrollo del bot se realizó mediante prompts profesionales a OpenCode, sin programar nada manualmente. El proceso siguió estos pasos:

1. **Preparación del entorno**: Formateo e instalación de Linux Mint
2. **Herramientas**: Instalación de OpenCode
3. **Desarrollo iterativo**: Múltiples prompts para añadir funcionalidades
4. **Documentación**: Generación automática de toda la documentación
5. **Preparación para producción**: Scripts, auditorías y optimizaciones

**Nota importante**: Ningún código fue escrito manualmente. Todo fue generado por OpenCode siguiendo las especificaciones dadas en los prompts.

---

**Autor**: Izan Urios  
**Fecha de documentación**: Mayo 2026  
**Herramienta utilizada**: OpenCode AI (opencode.ai)
