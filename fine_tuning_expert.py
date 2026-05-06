#!/usr/bin/env python3
"""
Fine-Tuning Expert System para el Bot de Telegram
Sistema para preparar datos, entrenar y gestionar modelos fine-tuned.
"""
import logging
import os
import re
import json
import uuid
import subprocess
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import requests

logger = logging.getLogger(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

FINETUNE_DIR = os.path.expanduser("~/.finetune")
os.makedirs(FINETUNE_DIR, exist_ok=True)

@dataclass
class FineTuneConfig:
    model_name: str
    base_model: str
    training_data_path: str
    epochs: int = 3
    batch_size: int = 1
    learning_rate: float = 2e-4
    status: str = "pending"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    trained_at: Optional[str] = None
    model_path: Optional[str] = None
    metrics: Dict = field(default_factory=dict)

def load_finetune_projects() -> Dict:
    config_file = os.path.join(FINETUNE_DIR, "projects.json")
    try:
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return json.load(f)
    except:
        pass
    return {}

def save_finetune_projects(projects: Dict) -> None:
    config_file = os.path.join(FINETUNE_DIR, "projects.json")
    with open(config_file, 'w') as f:
        json.dump(projects, f, indent=2)

class FineTuningExpert:
    
    def __init__(self):
        self.projects = load_finetune_projects()
    
    def prepare_training_data(self, conversations: List[Dict], output_file: str = None) -> str:
        """Convierte conversaciones a formato JSONL para fine-tuning"""
        if output_file is None:
            output_file = os.path.join(FINETUNE_DIR, f"training_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl")
        
        formatted_data = []
        
        for conv in conversations:
            messages = conv.get('messages', [])
            if len(messages) >= 2:
                prompt = ""
                completion = ""
                
                for i, msg in enumerate(messages):
                    role = msg.get('role', '')
                    content = msg.get('content', '')
                    
                    if role == 'user':
                        prompt += content + "\n"
                    elif role == 'assistant':
                        completion += content + "\n"
                
                if prompt and completion:
                    entry = {
                        "messages": [
                            {"role": "system", "content": "Eres un asistente útil en español."},
                            {"role": "user", "content": prompt.strip()},
                            {"role": "assistant", "content": completion.strip()}
                        ]
                    }
                    formatted_data.append(entry)
        
        with open(output_file, 'w') as f:
            for entry in formatted_data:
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')
        
        return output_file
    
    def prepare_conversation_data(self, chat_history: List[Dict], persona: str = None) -> str:
        """Prepara datos de conversación con un persona específico"""
        output_file = os.path.join(FINETUNE_DIR, f"persona_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl")
        
        system_prompt = persona or "Eres un asistente útil, conversacional y amigable en español."
        
        formatted_data = []
        
        for conv in chat_history:
            user_msg = conv.get('user', '')
            assistant_msg = conv.get('assistant', '')
            
            if user_msg and assistant_msg:
                entry = {
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_msg},
                        {"role": "assistant", "content": assistant_msg}
                    ]
                }
                formatted_data.append(entry)
        
        with open(output_file, 'w') as f:
            for entry in formatted_data:
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')
        
        return output_file
    
    def create_project(self, name: str, base_model: str = "gpt-4o-mini", 
                      persona: str = None, epochs: int = 3) -> str:
        """Crea un nuevo proyecto de fine-tuning"""
        project_id = str(uuid.uuid4())[:8]
        
        self.projects[project_id] = {
            "id": project_id,
            "name": name,
            "base_model": base_model,
            "persona": persona,
            "epochs": epochs,
            "status": "created",
            "training_data": None,
            "model_id": None,
            "created_at": datetime.now().isoformat(),
            "trained_at": None
        }
        
        save_finetune_projects(self.projects)
        return project_id
    
    def add_training_data(self, project_id: str, data_source: str, 
                         conversation_history: List[Dict] = None) -> str:
        """Añade datos de entrenamiento a un proyecto"""
        if project_id not in self.projects:
            return "❌ Proyecto no encontrado"
        
        project = self.projects[project_id]
        
        if data_source == "history" and conversation_history:
            output_file = self.prepare_conversation_data(
                conversation_history,
                project.get('persona')
            )
        else:
            return "❌ Fuente de datos no válida"
        
        project['training_data'] = output_file
        project['status'] = 'data_ready'
        save_finetune_projects(self.projects)
        
        return f"✅ Datos añadidos a proyecto {project_id}\n📁 {output_file}"
    
    def validate_data(self, data_file: str) -> Dict:
        """Valida datos de entrenamiento"""
        issues = []
        valid_count = 0
        
        try:
            with open(data_file, 'r') as f:
                for i, line in enumerate(f, 1):
                    try:
                        entry = json.loads(line)
                        messages = entry.get('messages', [])
                        
                        if len(messages) < 2:
                            issues.append(f"Línea {i}: Menos de 2 mensajes")
                            continue
                        
                        has_user = any(m.get('role') == 'user' for m in messages)
                        has_assistant = any(m.get('role') == 'assistant' for m in messages)
                        
                        if not has_user:
                            issues.append(f"Línea {i}: Falta mensaje de usuario")
                        if not has_assistant:
                            issues.append(f"Línea {i}: Falta mensaje de asistente")
                        
                        if has_user and has_assistant:
                            valid_count += 1
                            
                    except json.JSONDecodeError:
                        issues.append(f"Línea {i}: JSON inválido")
            
            return {
                "valid_samples": valid_count,
                "issues": issues[:10],
                "total_issues": len(issues),
                "status": "valid" if valid_count >= 10 and len(issues) < valid_count * 0.1 else "needs_review"
            }
        except Exception as e:
            return {"error": str(e)}
    
    def estimate_cost(self, data_file: str, model: str) -> Dict:
        """Estima coste de fine-tuning"""
        try:
            with open(data_file, 'r') as f:
                line_count = sum(1 for _ in f)
            
            model_costs = {
                "gpt-4o-mini": {"training": 0.008, "input": 0.15, "output": 0.6},
                "gpt-4o": {"training": 0.03, "input": 2.5, "output": 10},
                "gpt-3.5-turbo": {"training": 0.008, "input": 0.5, "output": 1.5}
            }
            
            costs = model_costs.get(model, model_costs["gpt-4o-mini"])
            
            estimated_tokens = line_count * 500
            training_cost = (estimated_tokens / 1000) * costs["training"]
            
            return {
                "samples": line_count,
                "estimated_tokens": estimated_tokens,
                "training_cost_usd": round(training_cost, 2),
                "model": model
            }
        except Exception as e:
            return {"error": str(e)}
    
    def get_project_status(self, project_id: str) -> str:
        """Obtiene estado de un proyecto"""
        if project_id not in self.projects:
            return "❌ Proyecto no encontrado"
        
        project = self.projects[project_id]
        
        status_emoji = {
            "created": "🆕",
            "data_ready": "📁",
            "training": "🔄",
            "completed": "✅",
            "error": "❌"
        }
        emoji = status_emoji.get(project['status'], "❓")
        
        result = f"""{emoji} *Proyecto: {project['name']}*

🆔 ID: `{project_id}`
📊 Estado: {project['status']}
🤖 Modelo base: {project['base_model']}
📅 Creado: {project['created_at'][:10]}"""

        if project.get('trained_at'):
            result += f"\n✅ Entrenado: {project['trained_at'][:10]}"
        
        if project.get('training_data'):
            result += f"\n📁 Datos: {project['training_data']}"
        
        if project.get('model_id'):
            result += f"\n🔗 Modelo: {project['model_id']}"
        
        return result
    
    def list_projects(self) -> str:
        """Lista todos los proyectos"""
        if not self.projects:
            return "📭 No hay proyectos de fine-tuning"
        
        result = "🔧 *Proyectos Fine-Tuning:*\n\n"
        
        for project_id, project in self.projects.items():
            status_emoji = {
                "created": "🆕", "data_ready": "📁",
                "training": "🔄", "completed": "✅", "error": "❌"
            }
            emoji = status_emoji.get(project['status'], "❓")
            
            result += f"{emoji} `{project_id}` {project['name']}\n"
            result += f"   📊 {project['status']} | {project['base_model']}\n\n"
        
        return result
    
    def delete_project(self, project_id: str) -> str:
        """Elimina un proyecto"""
        if project_id not in self.projects:
            return "❌ Proyecto no encontrado"
        
        project = self.projects[project_id]
        
        if project.get('training_data') and os.path.exists(project['training_data']):
            os.unlink(project['training_data'])
        
        del self.projects[project_id]
        save_finetune_projects(self.projects)
        
        return f"🗑️ Proyecto `{project_id}` eliminado"
    
    def generate_synthetic_data(self, topic: str, num_samples: int = 50) -> str:
        """Genera datos sintéticos para entrenamiento usando IA"""
        output_file = os.path.join(FINETUNE_DIR, f"synthetic_{topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.jsonl")
        
        prompt = f"""Genera {num_samples} ejemplos de conversación en español sobre el tema: {topic}

Cada ejemplo debe tener:
- Una pregunta o petición realista del usuario
- Una respuesta útil del asistente

Devuelve en formato JSON array con objetos que tengan:
- "messages": array con role y content
- El primer mensaje debe ser de "user"
- El segundo mensaje debe ser de "assistant"

Sé variado en las preguntas y natural en las respuestas."""

        try:
            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "openai/gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "Eres un generador de datos de entrenamiento. Devuelve SOLO JSON válido, sin explicaciones."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 4000,
                "temperature": 0.8
            }
            
            response = requests.post(OPENROUTER_API_URL, headers=headers, json=data, timeout=60)
            result = response.json()
            
            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0]["message"]["content"]
                
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0]
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0]
                
                data_array = json.loads(content.strip())
                
                with open(output_file, 'w') as f:
                    for entry in data_array:
                        f.write(json.dumps(entry, ensure_ascii=False) + '\n')
                
                return f"✅ Generados {len(data_array)} ejemplos en:\n📁 {output_file}"
            
            return "❌ Error al generar datos"
        except Exception as e:
            return f"❌ Error: {e}"
    
    def recommend_model(self, use_case: str) -> Dict:
        """Recomienda modelo según caso de uso"""
        recommendations = {
            "chatbot": {
                "model": "gpt-4o-mini",
                "reason": "Rápido y económico para conversaciones",
                "cost": "Bajo"
            },
            "codigo": {
                "model": "gpt-4o",
                "reason": "Mejor razonamiento para código",
                "cost": "Alto"
            },
            "analisis": {
                "model": "gpt-4o",
                "reason": "Análisis complejo y detallado",
                "cost": "Alto"
            },
            "resumen": {
                "model": "gpt-4o-mini",
                "reason": "Bueno para resúmenes rápidos",
                "cost": "Bajo"
            },
            "espanol": {
                "model": "openai/gpt-4o-mini",
                "reason": "Excelente en español",
                "cost": "Bajo"
            }
        }
        
        use_case_lower = use_case.lower()
        
        for key, rec in recommendations.items():
            if key in use_case_lower:
                return rec
        
        return recommendations["chatbot"]

finetune_expert = FineTuningExpert()

def get_finetune_help() -> str:
    return """🔧 *Fine-Tuning Expert*

Entrena modelos personalizados para tu bot.

*Proyectos:*
`/ftcreate <nombre>` - Crear proyecto
`/ftlist` - Ver proyectos
`/ftstatus <id>` - Estado de proyecto
`/ftdelete <id>` - Eliminar proyecto

*Datos de entrenamiento:*
`/ftdata <id>` - Añadir datos de historial
`/ftvalidate <archivo>` - Validar datos
`/ftcost <archivo> <modelo>` - Estimar coste

*Generación automática:*
`/ftgen <tema> <num>` - Generar datos sintéticos

*Recomendaciones:*
`/ftrec <caso>` - Recomendar modelo

*Casos de uso:*
chatbot, codigo, analisis, resumen, español

*Ejemplos:*
`/ftcreate asistente-tecnico`
`/ftgen Python 100`
`/ftrec chatbot`"""

def get_finetune_commands() -> Dict:
    return {
        "ftcreate": "Crear proyecto de fine-tuning",
        "ftlist": "Listar proyectos",
        "ftstatus": "Ver estado de proyecto",
        "ftdelete": "Eliminar proyecto",
        "ftdata": "Añadir datos de entrenamiento",
        "ftvalidate": "Validar archivo de datos",
        "ftcost": "Estimar coste de entrenamiento",
        "ftgen": "Generar datos sintéticos",
        "ftrec": "Recomendar modelo"
    }
