# filename: memory_utils.py

import json
import os
from typing import Dict, Any

MEMORY_PATH = "memory.json"


def load_memory(path: str = MEMORY_PATH) -> Dict[str, Any]:
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"{path} not found. Make sure memory.json is in the project root."
        )
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_memory(memory: Dict[str, Any], path: str = MEMORY_PATH) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=4, ensure_ascii=False)


def build_system_prompt(memory: Dict[str, Any]) -> str:
    project_descriptions = []
    for project in memory.get("projects", []):
        name = project.get("name", "")
        desc = project.get("description", "")
        techs = ", ".join(project.get("technologies", []))
        project_descriptions.append(f"- {name}: {desc} (Tech: {techs})")

    projects_block = "\n".join(project_descriptions) if project_descriptions else "None"

    system_prompt = f"""
You are Chiranjeevi's personal AI assistant.

User profile:
- Name: {memory.get('name', '')}
- Age: {memory.get('age', '')}
- Location: {memory.get('location', '')}
- Profession: {memory.get('profession', '')}
- College: {memory.get('college', '')}
- Branch: {memory.get('branch', '')}
- Year: {memory.get('year', '')}

Skills:
{', '.join(memory.get('skills', []))}

Interests:
{', '.join(memory.get('interests', []))}

Currently learning:
{', '.join(memory.get('current_learning', []))}

Career goals:
{', '.join(memory.get('career_goals', []))}

Projects:
{projects_block}

Daily tasks:
{', '.join(memory.get('daily_tasks', []))}

Notes:
{', '.join(memory.get('notes', []))}

Behavior rules:
- You are an assistant helping Chiranjeevi.
- Use this information as background context only.
- Do NOT pretend to be Chiranjeevi.
- Never say things like "I study at SRM AP" or "I am Chiranjeevi".
- Instead, refer to Chiranjeevi in third person.
- Keep answers concise and practical.
- When helpful, connect advice to Chiranjeevi's skills, interests, and goals.
"""
    return system_prompt