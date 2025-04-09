from __future__ import annotations

from dataclasses import dataclass
from pydantic import BaseModel, Field, field_validator
from pydantic_ai import Agent, RunContext
from typing import List, Optional, Dict
import logfire

from archon_agent.agent_prompts import SYSTEM_PROMPT
from archon_agent.agent_tools import obtener_gitignore_python

logfire.configure(send_to_logfire='if-token-present')


class RepoRequest(BaseModel):
    """
    Solicitud para generar instrucciones y comandos para crear un repositorio Git de un proyecto Python.

    language: Debe ser 'es' (Español).
    description: Breve descripción del proyecto (no obligatorio).
    """
    language: str = Field(..., description="Idioma para la respuesta. Solo 'es' soportado actualmente.")
    description: Optional[str] = Field(None, description="Descripción opcional del proyecto Python.")

    @field_validator("language")
    @classmethod
    def validate_language(cls, v):
        if v.strip().lower() != 'es':
            raise ValueError("Actualmente, solo se soporta el idioma 'es' (español).")
        return v.strip().lower()


class CommandStep(BaseModel):
    """
    Un paso en la configuración, con texto explicativo y un bloque de comandos en shell.
    """
    paso: str
    comando: str


class RepoSetupResponse(BaseModel):
    """
    Respuesta estructurada con pasos y comandos para crear el repositorio Git.
    """
    pasos: List[CommandStep]


@dataclass
class Deps:
    """
    Dependencias para el agente. Actualmente vacías, reservadas para extensiones futuras.
    """
    pass


repo_agent = Agent[Deps, RepoSetupResponse](
    model='openai:gpt-4o',
    deps_type=Deps,
    result_type=RepoSetupResponse,
    system_prompt=SYSTEM_PROMPT,
    instrument=True,
    retries=2,
)


@repo_agent.tool
async def obtener_gitignore(ctx: RunContext[Deps], dummy: str = "") -> str:
    """
    Punto de entrada para obtener una plantilla .gitignore Python estándar.

    Args:
        ctx: Contexto.
        dummy: Sin usar. Reservado.

    Returns:
        Contenido de la plantilla .gitignore estándar.
    """
    return await obtener_gitignore_python(ctx, dummy)
