#!/usr/bin/env python3
"""
Multi-Agent Pipeline System para el Bot de Telegram
Sistema de agentes especializados que trabajan en cadena.
"""
import logging
import os
import re
import json
import time
import uuid
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import requests
from urllib.parse import quote

logger = logging.getLogger(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

class AgentType(Enum):
    ORCHESTRATOR = "orchestrator"
    RESEARCHER = "researcher"
    WRITER = "writer"
    ANALYZER = "analyzer"
    SYSTEM = "system"
    SCHEDULER = "scheduler"
    SCRAPER = "scraper"
    SUMMARIZER = "summarizer"
    FILTER = "filter"
    COMPARE = "compare"
    ALERT = "alert"
    NEWS = "news"
    WEATHER = "weather"

@dataclass
class AgentResult:
    agent_type: AgentType
    success: bool
    output: str
    metadata: Dict = field(default_factory=dict)
    error: Optional[str] = None
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None

@dataclass
class PipelineContext:
    task_id: str
    user_request: str
    results: List[AgentResult] = field(default_factory=list)
    shared_data: Dict = field(default_factory=dict)
    metadata: Dict = field(default_factory=dict)

class Agent:
    """Base class para todos los agentes"""
    
    def __init__(self, agent_type: AgentType, model: str = "openai/gpt-4o-mini"):
        self.agent_type = agent_type
        self.model = model
        self.system_prompt = self._get_system_prompt()
    
    def _get_system_prompt(self) -> str:
        raise NotImplementedError
    
    def _call_llm(self, messages: List[Dict], max_tokens: int = 2000) -> str:
        try:
            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": 0.7
            }
            
            response = requests.post(OPENROUTER_API_URL, headers=headers, json=data, timeout=60)
            result = response.json()
            
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            return "Error: Sin respuesta del modelo"
        except Exception as e:
            logger.error(f"LLM error: {e}")
            return f"Error: {e}"
    
    def execute(self, context: PipelineContext) -> AgentResult:
        """Ejecuta el agente y retorna un AgentResult"""
        start = datetime.now()
        try:
            output = self._execute(context)
            return AgentResult(
                agent_type=self.agent_type,
                success=True,
                output=output,
                start_time=start,
                end_time=datetime.now()
            )
        except Exception as e:
            logger.error(f"Agent {self.agent_type.value} error: {e}")
            return AgentResult(
                agent_type=self.agent_type,
                success=False,
                output="",
                error=str(e),
                start_time=start,
                end_time=datetime.now()
            )
    
    def _execute(self, context: PipelineContext) -> str:
        raise NotImplementedError

# ============== AGENTES ESPECIALIZADOS ==============

class OrchestratorAgent(Agent):
    """Analiza la petición y decide qué agentes usar y en qué orden"""
    
    def _get_system_prompt(self) -> str:
        return """Eres un orquestador de IA. Tu trabajo es analizar la petición del usuario 
y decidir qué agentes deben ejecutarse y en qué orden.

AGENTES DISPONIBLES:
- researcher: Para buscar información en la web
- analyzer: Para analizar productos, precios, datos
- writer: Para redactar contenido, resúmenes
- system: Para ejecutar comandos del sistema
- scheduler: Para crear recordatorios
- scraper: Para extraer contenido de URLs
- summarizer: Para resumir textos largos

RESPUESTA FORMATO JSON:
{
  "intent": "tipo de intención detectada",
  "agents_needed": ["agente1", "agente2"],
  "order": "parallel|sequential",
  "shared_data": {"dato1": "valor1"},
  "confidence": 0.9
}

Sé conciso y preciso."""

    def _execute(self, context: PipelineContext) -> str:
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"Petición del usuario: {context.user_request}"}
        ]
        
        response = self._call_llm(messages)
        
        try:
            if response.startswith("```"):
                response = response.split("```")[1]
                if response.startswith("json"):
                    response = response[4:]
            
            parsed = json.loads(response.strip())
            context.metadata.update(parsed)
            return json.dumps(parsed, ensure_ascii=False)
        except:
            return response

class ResearchAgent(Agent):
    """Busca información en la web"""
    
    def _get_system_prompt(self) -> str:
        return """Eres un agente investigador. Tu trabajo es buscar información relevante en la web.
Proporciona resultados claros, concisos y con fuentes."""

    def _execute(self, context: PipelineContext) -> str:
        from urllib.parse import quote
        
        request = context.user_request
        
        for skip in ['busca', 'búscame', 'dime', 'investiga', 'search']:
            request = re.sub(skip, '', request, flags=re.I).strip()
        
        if not request:
            return "No se pudo extraer la consulta de búsqueda"
        
        encoded = quote(request)
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml',
            'Accept-Language': 'es-ES,es;q=0.9',
        }
        
        try:
            url = f"https://www.google.com/search?q={encoded}&hl=es&gl=es"
            response = requests.get(url, headers=headers, timeout=15)
            
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            results = []
            items = soup.select('.g, [data-hveid]')[:5]
            
            for item in items:
                title_elem = item.select_one('h3, .DKV0Md')
                snippet_elem = item.select_one('.VwiC3b, .IsZvec')
                
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    snippet = snippet_elem.get_text(strip=True)[:150] if snippet_elem else ""
                    results.append(f"📌 *{title}*\n{snippet}\n")
            
            if results:
                output = f"🔍 *Resultados para:* {request}\n\n" + "\n".join(results)
                context.shared_data['research_results'] = output
                return output
            return "No se encontraron resultados"
        except Exception as e:
            return f"Error en búsqueda: {e}"

class AnalyzerAgent(Agent):
    """Analiza productos, precios, datos comparativos"""
    
    def _get_system_prompt(self) -> str:
        return """Eres un agente analista. Tu trabajo es analizar productos, precios 
y proporcionar comparaciones útiles.

Proporciona:
- Lista de productos con precios
- Comparaciones relevantes
- Recomendaciones basadas en el análisis"""

    def _execute(self, context: PipelineContext) -> str:
        from urllib.parse import quote
        
        request = context.user_request
        
        price_keywords = ['precio', 'cuánto cuesta', 'comprar', 'barato', 'oferta', 'catalogo']
        
        if any(kw in request.lower() for kw in price_keywords):
            encoded = quote(request)
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept-Language': 'es-ES,es;q=0.9',
            }
            
            try:
                url = f"https://www.google.com/search?q={encoded}&tbm=shop&hl=es&gl=es"
                response = requests.get(url, headers=headers, timeout=15)
                
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')
                
                items = soup.select('.A2sYd, .sh-dgr__content')[:8]
                
                results = []
                for item in items:
                    name_elem = item.select_one('.tAxDx, .A2sYd')
                    price_elem = item.select_one('.HRLxBb, [class*="price"]')
                    store_elem = item.select_one('.vEjMR, .SLIej')
                    
                    if name_elem:
                        name = name_elem.get_text(strip=True)[:60]
                        price = price_elem.get_text(strip=True) if price_elem else "N/A"
                        store = store_elem.get_text(strip=True)[:25] if store_elem else ""
                        
                        results.append(f"🛒 *{name}*\n   💰 {price}" + (f" | 🏪 {store}" if store else ""))
                
                if results:
                    output = f"💰 *Análisis de precios:*\n\n" + "\n\n".join(results)
                    context.shared_data['analysis_results'] = output
                    return output
                    
            except Exception as e:
                pass
        
        return "No se detectó intención de análisis de precios"

class WriterAgent(Agent):
    """Redacta contenido, resúmenes, mensajes"""
    
    def _get_system_prompt(self) -> str:
        return """Eres un agente redactor. Tu trabajo es crear contenido claro, 
bien estructurado y en español natural.

Puedes usar:
- Encabezados con emojis
- Listas con bullets
- Texto markdown
- Formato amigable"""

    def _execute(self, context: PipelineContext) -> str:
        previous_results = "\n\n".join([
            r.output for r in context.results if r.success
        ]) if context.results else ""
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"""Petición original: {context.user_request}

Resultados previos de otros agentes:
{previous_results}

Redacta una respuesta completa y útil para el usuario."""}
        ]
        
        response = self._call_llm(messages, max_tokens=2500)
        context.shared_data['written_content'] = response
        return response

class SystemAgent(Agent):
    """Ejecuta comandos del sistema"""
    
    def _get_system_prompt(self) -> str:
        return """Eres un agente de sistema. Tu trabajo es ejecutar comandos
y proporcionar información del sistema.

Comandos seguros permitidos:
- ls, pwd, ps, top, df, free
- whoami, hostname, uname
- cat, head, tail

Comandos bloqueados por seguridad:
- rm -rf, mkfs, shutdown, reboot"""

    def _execute(self, context: PipelineContext) -> str:
        import subprocess
        
        request = context.user_request.lower()
        
        if any(kw in request for kw in ['cómo está', 'estado del', 'info del', 'sistema']):
            import psutil
            
            cpu = psutil.cpu_percent(interval=0.5)
            mem = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            output = f"""🖥️ *Estado del Sistema*

📊 *Uso:*
• CPU: `{cpu}%`
• RAM: `{mem.percent}%` ({mem.used/1024**3:.1f}/{mem.total/1024**3:.1f} GB)
• Disco: `{disk.percent}%` ({disk.used/1024**3:.0f}/{disk.total/1024**3:.0f} GB)"""
            
            context.shared_data['system_status'] = output
            return output
        
        return "No se detectó intención de comando de sistema"

class SummarizerAgent(Agent):
    """Resume textos largos"""
    
    def _get_system_prompt(self) -> str:
        return """Eres un agente resumidor. Tu trabajo es crear resúmenes 
concisos de texto largo.

Reglas:
- Máximo 5 puntos clave
- Usar viñetas
- Preservar la información importante"""

    def _execute(self, context: PipelineContext) -> str:
        text = context.shared_data.get('scraped_content', '')
        
        if not text:
            url_match = re.search(r'https?://\S+', context.user_request)
            if url_match:
                url = url_match.group()
                try:
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    }
                    response = requests.get(url, headers=headers, timeout=15)
                    from bs4 import BeautifulSoup
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    for tag in soup(['script', 'style', 'nav', 'header']):
                        tag.decompose()
                    
                    text = soup.get_text(separator=' ', strip=True)[:3000]
                    context.shared_data['scraped_content'] = text
                except Exception as e:
                    return f"Error al obtener contenido: {e}"
        
        if not text:
            return "No hay contenido para resumir"
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"Resume este texto:\n\n{text[:4000]}"}
        ]
        
        response = self._call_llm(messages, max_tokens=1000)
        context.shared_data['summary'] = response
        return response

# ============== NUEVOS AGENTES ESPECIALIZADOS ==============

class ScraperAgent(Agent):
    """Extrae contenido de URLs"""
    
    def _get_system_prompt(self) -> str:
        return """Eres un agente extractor de contenido web. Tu trabajo es obtener
el contenido completo y limpio de URLs."""

    def _execute(self, context: PipelineContext) -> str:
        from bs4 import BeautifulSoup
        
        url_match = re.search(r'https?://\S+', context.user_request)
        if not url_match:
            url_match = re.search(r'www\.\S+', context.user_request)
        
        if not url_match:
            return "No se encontró URL en la petición"
        
        url = url_match.group()
        if not url.startswith('http'):
            url = 'https://' + url
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept-Language': 'es-ES,es;q=0.9',
            }
            response = requests.get(url, headers=headers, timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for tag in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
                tag.decompose()
            
            paragraphs = soup.select('p, article, main, .content')
            text = ' '.join([p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 50])
            text = re.sub(r'\s+', ' ', text)[:5000]
            
            context.shared_data['scraped_url'] = url
            context.shared_data['scraped_content'] = text
            
            return f"🌐 Contenido extraído de {url}\n\n{text[:500]}..."
        except Exception as e:
            return f"Error al obtener contenido: {e}"

class FilterAgent(Agent):
    """Filtra y prioriza resultados"""
    
    def _get_system_prompt(self) -> str:
        return """Eres un agente filtro. Tu trabajo es analizar resultados,
eliminar duplicados y basura, y priorizar la información más relevante."""

    def _execute(self, context: PipelineContext) -> str:
        research_results = context.shared_data.get('research_results', '')
        
        if not research_results:
            return "No hay resultados para filtrar"
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"""Analiza y filtra estos resultados. Elimina duplicados y resultados irrelevantes.
Prioriza fuentes confiables y información reciente.

Resultados:
{research_results}

Responde con los mejores 5 resultados limpios y priorizados."""}
        ]
        
        response = self._call_llm(messages, max_tokens=1500)
        context.shared_data['filtered_results'] = response
        return response

class CompareAgent(Agent):
    """Compara productos, precios, opciones"""
    
    def _get_system_prompt(self) -> str:
        return """Eres un agente comparador. Tu trabajo es crear tablas comparativas
y análisis de diferencias entre opciones."""

    def _execute(self, context: PipelineContext) -> str:
        analysis_results = context.shared_data.get('analysis_results', '')
        
        if not analysis_results:
            return "No hay datos para comparar"
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"""Crea una tabla comparativa clara y análisis de estos productos/opciones:

{analysis_results}

Incluye:
- Tabla comparativa con características
- Mejor opción según precio/calidad
- Recomendación final""" }
        ]
        
        response = self._call_llm(messages, max_tokens=2000)
        context.shared_data['comparison'] = response
        return response

class AlertAgent(Agent):
    """Detecta problemas y genera alertas"""
    
    def _get_system_prompt(self) -> str:
        return """Eres un agente de alertas. Tu trabajo es monitorear datos,
detectar anomalías y generar alertas claras."""

    def _execute(self, context: PipelineContext) -> str:
        system_status = context.shared_data.get('system_status', '')
        
        if not system_status:
            return "No hay datos del sistema para monitorear"
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"""Analiza el estado del sistema y detecta problemas:
{system_status}

Responde con:
- Estado general (OK/WARNING/CRITICAL)
- Problemas detectados
- Acciones recomendadas""" }
        ]
        
        response = self._call_llm(messages, max_tokens=1000)
        
        alerts = []
        if 'WARNING' in response.upper() or 'CRITICAL' in response.upper():
            alerts.append("⚠️")
        if 'OK' in response.upper():
            alerts.append("✅")
        
        context.shared_data['alerts'] = response
        context.shared_data['has_alerts'] = len(alerts) > 0
        return response

class NewsAgent(Agent):
    """Busca y filtra noticias"""
    
    def _get_system_prompt(self) -> str:
        return """Eres un agente de noticias. Tu trabajo es buscar noticias
recientes, filtrar por relevancia y resumir."""

    def _execute(self, context: PipelineContext) -> str:
        topic = context.user_request
        for skip in ['noticias', 'news', 'últimas']:
            topic = re.sub(skip, '', topic, flags=re.I).strip()
        
        if not topic:
            topic = 'últimas noticias'
        
        try:
            encoded = quote(topic)
            url = f"https://www.bing.com/news/search?q={encoded}&hl=es&gl=es"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept-Language': 'es-ES,es;q=0.9',
            }
            response = requests.get(url, headers=headers, timeout=15)
            
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            news_items = []
            seen = set()
            
            for item in soup.select('.news-card, [class*="news-item"]')[:8]:
                title_elem = item.select_one('h3, .title')
                snippet_elem = item.select_one('.snippet, .desc')
                
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    if title and len(title) > 10 and title not in seen:
                        seen.add(title)
                        snippet = snippet_elem.get_text(strip=True)[:100] if snippet_elem else ""
                        news_items.append(f"📰 *{title}*\n{snippet}")
            
            if news_items:
                output = f"📰 *Noticias sobre:* {topic}\n\n" + "\n\n".join(news_items)
                context.shared_data['news'] = output
                return output
            
            return "No se encontraron noticias"
        except Exception as e:
            return f"Error al buscar noticias: {e}"

class WeatherAgent(Agent):
    """Obtiene datos del clima"""
    
    def _get_system_prompt(self) -> str:
        return """Eres un agente meteorológico. Tu trabajo es obtener
el clima actual y pronóstico de forma clara."""

    def _execute(self, context: PipelineContext) -> str:
        location = None
        location_patterns = [
            r'clima\s+(?:en|de|para)?\s*(\w+)',
            r'tiempo\s+(?:en|de|para)?\s*(\w+)',
            r'temperature\s+(?:en|de|para)?\s*(\w+)',
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, context.user_request, re.I)
            if match:
                location = match.group(1)
                break
        
        if not location:
            location = 'Madrid'
        
        try:
            url = f"https://wttr.in/{quote(location)}?format=j1"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            current = data.get('current_condition', [{}])[0]
            area = data.get('nearest_area', [{}])
            if area and isinstance(area, list):
                area = area[0]
            area_name = area.get('areaName', [{'value': location}])
            if isinstance(area_name, list):
                area_name = area_name[0].get('value', location)
            
            temp = current.get('temp_C', '?')
            feels = current.get('FeelsLikeC', '?')
            humidity = current.get('humidity', '?')
            wind = current.get('windspeedKmph', '?')
            desc = current.get('weatherDesc', [{}])
            if isinstance(desc, list):
                desc = desc[0].get('value', 'Unknown')
            
            weather_icons = {
                'Sunny': '☀️', 'Clear': '🌙', 'Partly cloudy': '⛅', 'Cloudy': '☁️',
                'Overcast': '☁️', 'Mist': '🌫️', 'Fog': '🌫️', 'Light rain': '🌧️',
                'Moderate rain': '🌧️', 'Heavy rain': '🌧️', 'Snow': '❄️', 'Thunderstorm': '⛈️'
            }
            icon = weather_icons.get(desc, '🌡️')
            
            output = f"{icon} *Clima en {area_name}*\n\n"
            output += f"🌡️ Temperatura: {temp}°C (sensación {feels}°C)\n"
            output += f"💧 Humedad: {humidity}%\n"
            output += f"💨 Viento: {wind} km/h\n"
            output += f"☁️ Estado: {desc}"
            
            context.shared_data['weather'] = output
            return output
        except Exception as e:
            return f"Error al obtener clima: {e}"

# ============== PIPELINE EXECUTOR ==============

class Pipeline:
    """Ejecuta un pipeline de agentes"""
    
    def __init__(self):
        self.agents: Dict[AgentType, Agent] = {}
        self._register_agents()
    
    def _register_agents(self):
        self.agents[AgentType.ORCHESTRATOR] = OrchestratorAgent(AgentType.ORCHESTRATOR)
        self.agents[AgentType.RESEARCHER] = ResearchAgent(AgentType.RESEARCHER)
        self.agents[AgentType.ANALYZER] = AnalyzerAgent(AgentType.ANALYZER)
        self.agents[AgentType.WRITER] = WriterAgent(AgentType.WRITER)
        self.agents[AgentType.SYSTEM] = SystemAgent(AgentType.SYSTEM)
        self.agents[AgentType.SUMMARIZER] = SummarizerAgent(AgentType.SUMMARIZER)
        self.agents[AgentType.SCRAPER] = ScraperAgent(AgentType.SCRAPER)
        self.agents[AgentType.FILTER] = FilterAgent(AgentType.FILTER)
        self.agents[AgentType.COMPARE] = CompareAgent(AgentType.COMPARE)
        self.agents[AgentType.ALERT] = AlertAgent(AgentType.ALERT)
        self.agents[AgentType.NEWS] = NewsAgent(AgentType.NEWS)
        self.agents[AgentType.WEATHER] = WeatherAgent(AgentType.WEATHER)
    
    def execute(self, user_request: str) -> PipelineContext:
        context = PipelineContext(
            task_id=str(uuid.uuid4())[:8],
            user_request=user_request
        )
        
        orchestrator = self.agents[AgentType.ORCHESTRATOR]
        plan_result = orchestrator.execute(context)
        
        if plan_result.success:
            try:
                plan = json.loads(plan_result.output)
                agents_needed = plan.get('agents_needed', [])
                order = plan.get('order', 'sequential')
                
                logger.info(f"Pipeline {context.task_id}: {agents_needed} ({order})")
                
                if order == 'parallel':
                    for agent_name in agents_needed:
                        agent_type = AgentType(agent_name)
                        if agent_type in self.agents:
                            result = self.agents[agent_type].execute(context)
                            context.results.append(result)
                else:
                    for agent_name in agents_needed:
                        agent_type = AgentType(agent_name)
                        if agent_type in self.agents:
                            result = self.agents[agent_type].execute(context)
                            context.results.append(result)
                
                writer = self.agents[AgentType.WRITER]
                final_result = writer.execute(context)
                context.results.append(final_result)
                
            except Exception as e:
                logger.error(f"Pipeline execution error: {e}")
                context.results.append(AgentResult(
                    agent_type=AgentType.ORCHESTRATOR,
                    success=False,
                    output="",
                    error=str(e)
                ))
        
        return context
    
    def execute_single(self, agent_type: AgentType, user_request: str) -> AgentResult:
        context = PipelineContext(
            task_id=str(uuid.uuid4())[:8],
            user_request=user_request
        )
        
        if agent_type in self.agents:
            return self.agents[agent_type].execute(context)
        
        return AgentResult(
            agent_type=agent_type,
            success=False,
            output="",
            error="Agente no encontrado"
        )

# ============== PIPELINE REGISTRY ==============

PIPELINES = {
    "web_search": {
        "agents": ["researcher", "filter", "writer"],
        "order": "sequential",
        "description": "Búsqueda web completa con filtrado"
    },
    "price_analysis": {
        "agents": ["researcher", "analyzer", "compare", "writer"],
        "order": "sequential",
        "description": "Análisis comparativo de precios"
    },
    "url_summary": {
        "agents": ["scraper", "summarizer", "writer"],
        "order": "sequential",
        "description": "Resumen inteligente de URLs"
    },
    "system_monitor": {
        "agents": ["system", "alert"],
        "order": "sequential",
        "description": "Monitoreo con alertas del sistema"
    },
    "morning_briefing": {
        "agents": ["weather", "news", "system", "writer"],
        "order": "sequential",
        "description": "Resumen matutino completo"
    },
    "product_research": {
        "agents": ["researcher", "analyzer", "compare", "writer"],
        "order": "sequential",
        "description": "Investigación completa de productos"
    }
}

def get_pipeline(name: str) -> Optional[List[str]]:
    if name in PIPELINES:
        return PIPELINES[name]['agents']
    return None

def get_all_commands() -> str:
    return """🤖 *COMANDOS DEL BOT - Lista Completa*

━━━━━━━━━━━━━━━━━━━━
🌐 *BÚSQUEDA Y WEB*
━━━━━━━━━━━━━━━━━━━━
`/pipe <tarea>` - Pipeline automático inteligente
`/agent <tipo> <tarea>` - Usar agente específico
`/agents` - Ver agentes disponibles
`/search <query>` - Búsqueda web rápida

━━━━━━━━━━━━━━━━━━━━
🌡️ *CLIMA Y NOTICIAS*
━━━━━━━━━━━━━━━━━━━━
`/clima <ciudad>` - Clima actual
`/noticias <tema>` - Noticias recientes

━━━━━━━━━━━━━━━━━━━━
💰 *PRODUCTOS Y PRECIOS*
━━━━━━━━━━━━━━━━━━━━
`/price <producto>` - Análisis de precios
`/compare <producto1> vs <producto2>` - Comparar

━━━━━━━━━━━━━━━━━━━━
🖥️ *SISTEMA*
━━━━━━━━━━━━━━━━━━━━
`/sysinfo` - Estado del PC
`/procs` - Procesos activos
`/network` - Estado de red

━━━━━━━━━━━━━━━━━━━━
🔔 *RECORDATORIOS*
━━━━━━━━━━━━━━━━━━━━
`/remind <msg> in <tiempo>` - Crear recordatorio
`/reminders` - Ver recordatorios
`/delremind <id>` - Eliminar

━━━━━━━━━━━━━━━━━━━━
🔄 *RALPH WIGGUM LOOP*
━━━━━━━━━━━━━━━━━━━━
`/ralph <tarea>` - Crear tarea iterativa
`/rstart <id>` - Iniciar loop
`/rstatus <id>` - Ver estado
`/rlist` - Ver tareas
`/riter <id>` - Iteración manual
`/rcancel <id>` - Cancelar

━━━━━━━━━━━━━━━━━━━━
📝 *CONVERSACIÓN*
━━━━━━━━━━━━━━━━━━━━
`/voz` - Activar/desactivar audio
`/reset` - Borrar historial
`/help` - Este mensaje

━━━━━━━━━━━━━━━━━━━━
🔧 *FINE-TUNING EXPERT*
━━━━━━━━━━━━━━━━━━━━
`/ftcreate <nombre>` - Crear proyecto
`/ftlist` - Ver proyectos
`/ftstatus <id>` - Estado de proyecto
`/ftdata <id>` - Añadir datos
`/ftgen <tema> <num>` - Generar datos
`/ftrec <caso>` - Recomendar modelo
`/ftvalidate <archivo>` - Validar datos
`/ftcost <archivo> <modelo>` - Estimar coste
`/ft` - Ayuda fine-tuning

━━━━━━━━━━━━━━━━━━━━
*También puedes hablarme con naturalidad!* 💬"""

# Instancia global del pipeline
pipeline = Pipeline()
