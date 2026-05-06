# Proceso de Creación del Bot de Telegram IA

**Autor**: Izan Urios  
**Fecha**: Mayo 2026  
**Descripción**: Documento que detalla todo el proceso de creación del bot, desde la preparación del sistema hasta su implementación final con OpenCode.

---

## 1. Formateo del Ordenador e Instalación de Linux Mint

**1.- Prompt**:  
> "Oye, mi ordenador va super lento y quiero empezar de cero. Quiero instalarle Linux Mint porque dicen que es fácil. Tengo un USB por ahí, ¿cómo lo hago?"

**2.- Resultado**:  
Se creó un USB bootable con Linux Mint usando Rufus. Se formateó el disco duro e instaló Linux Mint limpio.

**3.- Problemas que ocasionó**:  
- Se borró todo lo que tenía antes (menos mal hice copia de seguridad).
- Al principio no me funcionaba el wifi ni el sonido.

**4.- Prompt que lo solucionó**:  
> "Acabo de instalar Linux Mint y no me va bien el wifi ni el sonido. ¿Me arreglas esto? Ah, y ponme también lo básico para poder programar."

---

## 2. Instalación de OpenCode

**1.- Prompt**:  
> "Quiero usar OpenCode para hacer cosas con inteligencia artificial. ¿Me lo instalas en mi Linux Mint? Luego me dices cómo comprobar que funciona."

**2.- Resultado**:  
Se instaló OpenCode y funcionaba, se comprobó con `opencode --version`.

**3.- Problemas que ocasionó**:  
- Faltaban algunas cosas que OpenCode necesitaba para funcionar.

**4.- Prompt que lo solucionó**:  
> "OpenCode me da errores de que faltan cosas. ¿Me instalas todo lo que necesita para que funcione bien?"

---

## 3. Creación del Bot de Telegram con OpenRouter y OpenClaw

### 3.1. Prompt Inicial - Creación del Bot Básico

**1.- Prompt**:  
> "Quiero hacer un bot para Telegram que hable conmigo usando inteligencia artificial. Que use OpenRouter para conectarse a esos modelos que son tan buenos.
>
> Lo que quiero es que:
> - Le pueda escribir de forma normal y me conteste bien
> - Si le pregunto algo que necesite buscar por internet (noticias, precios, clima...), que busque automáticamente
> - Que use DuckDuckGo para buscar, que no me haga poner keys ni nada raro
> - Que me diga el clima de donde le diga, usando wttr.in que dicen que es gratis
> - Que me diga la hora y fecha actual de Madrid cuando le pregunte
> - Que tenga comandos básicos: /start para empezar, /help para ayuda, /hora, /clima, /status
> - Que me conteste con emojis y quede bonito
> - Que las claves del bot y de OpenRouter las pongas en variables de entorno, no directamente en el código porque eso es peligroso
>
> ¿Me puedes hacer el código completo en un archivo `telegram_bot.py` para poder ejecutarlo ya?"

**2.- Resultado**:  
Se generó el archivo `telegram_bot.py` con:
- Conexión a Telegram y OpenRouter
- Búsqueda web con DuckDuckGo
- Consulta de clima con wttr.in
- Comandos básicos funcionando
- Manejo de errores

**3.- Problemas que ocasionó**:  
- Al mirar el código vi que las claves estaban puestas tal cual (peligroso).

**4.- Prompt que lo solucionó**:  
> "Oye, has puesto las claves directamente en el código. Cámbialo para que las lea de variables de entorno con os.getenv. Y hazme un archivo .env.example para saber qué tengo que poner. Ah, y que el .gitignore tenga el .env para no subir las claves a GitHub cuando lo suba."

---

### 3.2. Prompt - Mejorar Detección de lo que Pregunto

**1.- Prompt**:  
> "El bot funciona bien, pero a veces no busca cuando debería. ¿Le puedes añadir más palabras para que sepa cuándo buscar en internet? Cosas como 'noticias', 'precio', 'actual', 'reciente', 'cuánto', 'qué pasó'...
>
> Y otra cosa: cuando le pregunto 'qué hora es' o 'qué día es hoy', que me lo diga directamente sin pasar por la IA ni buscar en internet."

**2.- Resultado**:  
Se mejoró el bot con:
- Más palabras para detectar cuándo buscar
- Respuesta directa a preguntas de hora/fecha sin usar IA

---

### 3.3. Prompt - Mejorar las Respuestas

**1.- Prompt**:  
> "Quiero que el bot sea más útil. ¿Podrías hacer que:
> - Le pase la fecha y hora actual a la IA para que sepa qué día es
> - A la IA le digas que si le pasas resultados de búsqueda, use eso como información (que no diga que no sabe nada)
> - Las respuestas sean cortas y usen emojis
> - Si la respuesta no tiene un emoji al principio, que le ponga uno (🤖)"

**2.- Resultado**:  
Las respuestas de la IA mejoraron mucho con:
- Fecha y hora actual en el prompt
- Instrucciones claras para usar resultados de búsqueda
- Formato consistente con emojis

---

### 3.4. Prompt - Scripts para Gestionar el Bot

**1.- Prompt**:  
> "Para terminar, hazme unos scripts que me ayuden:
>
> 1. Un `run_bot.sh` que asegure que solo hay una instancia del bot (que no se ejecuten dos a la vez)
> 2. Un `requirements.txt` con todo lo que necesito instalar
> 3. Un `README.md` bonito con ejemplos de uso y todo en español
>
> Que todo se vea profesional."

**2.- Resultado**:  
Se crearon todos los scripts y el README con buena pinta.

---

## Resumen del Proceso

Todo el desarrollo del bot se hizo hablando con OpenCode, sin escribir nada de código a mano. El proceso fue:

1. **Preparar el PC**: Formateo e instalación de Linux Mint
2. **Instalar herramientas**: OpenCode
3. **Crear el bot**: Pedirle a OpenCode que me lo hiciera con todas las funciones que quería
4. **Mejoras**: Ir pidiendo mejoras poco a poco (búsqueda, clima, hora...)
5. **Documentación**: README y este documento

**Nota importante**: Todo fue generado por OpenCode. Yo solo pedía lo que quería y él me hacía el código.

---

**Autor**: Izan Urios  
**Fecha de documentación**: Mayo 2026  
**Herramienta utilizada**: OpenCode AI (opencode.ai)
