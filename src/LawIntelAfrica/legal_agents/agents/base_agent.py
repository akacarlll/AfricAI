import logging
from typing import Any
from models.documents import AgentResponse
# Configure logging
from main import logger
class BaseAgent:
    """Base class for all agents in the system."""
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.logger = logging.getLogger(f"Agent:{agent_id}")
    
    async def process(self, query: Any) -> AgentResponse:
        """Process a query and return a response."""
        raise NotImplementedError("Subclasses must implement this method.")