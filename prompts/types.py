from dataclasses import dataclass
from typing import List, Optional

@dataclass
class PromptVariable:
    name: str
    description: str
    required: bool = True

@dataclass
class PromptTemplate:
    name: str
    version: str
    template: str
    variables: List[PromptVariable]
    description: Optional[str] = None
