import logging
from typing import Optional
from prompts.types import PromptTemplate
from prompts.versions import PROMPT_VERSIONS

logger = logging.getLogger(__name__)

class PromptRegistry:
    @staticmethod
    def get_prompt_template(name: str, version: Optional[str] = None) -> PromptTemplate:
        if name not in PROMPT_VERSIONS:
            raise ValueError(f"Prompt '{name}' not found in registry.")
            
        versions = PROMPT_VERSIONS[name]
        
        # If no version specified, get the latest
        if not version:
            version = sorted(versions.keys())[-1]
            
        if version not in versions:
            raise ValueError(f"Version '{version}' not found for prompt '{name}'.")
            
        return versions[version]

    @staticmethod
    def get_rag_prompt(context: str, history: str, question: str, version: Optional[str] = "v1.1") -> str:
        template_obj = PromptRegistry.get_prompt_template("rag_base", version)
        
        try:
            return template_obj.template.format(
                context=context,
                history=history,
                question=question
            )
        except KeyError as e:
            logger.error(f"Missing required prompt variable: {e}")
            raise
