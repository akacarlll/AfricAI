from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class Document(BaseModel):
    """Represents a legal document with its metadata."""
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

class Query(BaseModel):
    """Represents a query for retrieving documents."""
    text: str
    filters: Optional[Dict[str, Any]] = None
    top_k: int = 5

class AgentResponse(BaseModel):
    """Represents an agent's response."""
    agent_id: str
    content: str
    source_documents: List[Document] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)