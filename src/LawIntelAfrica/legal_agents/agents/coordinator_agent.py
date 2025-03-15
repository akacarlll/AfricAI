
from typing import List
import asyncio
from base_agent import BaseAgent
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from utils.setup import setup_llm
from models.documents import (
    AgentResponse,
    Query
)

class CoordinatorAgent(BaseAgent):
    """Agent that coordinates the workflow between other agents."""
    
    def __init__(self, agent_id: str, retrieval_agents: List[BaseAgent], processing_agent: BaseAgent):
        super().__init__(agent_id)
        self.retrieval_agents = retrieval_agents
        self.processing_agent = processing_agent
        self.llm = setup_llm()
        
        # Define prompt for the coordinator
        coordinator_prompt = PromptTemplate(
            input_variables=["retrieval_results", "question"],
            template="""
            You are a legal research coordinator. You have received results from multiple retrieval systems
            for the following question:
            
            Question: {question}
            
            Retrieval Results:
            {retrieval_results}
            
            Decide which retrieved documents are most relevant to the question and should be
            analyzed further. Provide a list of document IDs you select for deeper analysis.
            """
        )
        
        self.selection_chain = LLMChain(llm=self.llm, prompt=coordinator_prompt)
    
    async def process(self, query: str) -> AgentResponse:
        """Coordinate the workflow between agents."""
        try:
            self.logger.info(f"Coordinating workflow for query: {query}")
            
            # Step 1: Query all retrieval agents
            retrieval_tasks = [
                agent.process(Query(text=query, top_k=5))
                for agent in self.retrieval_agents
            ]
            
            retrieval_results = await asyncio.gather(*retrieval_tasks)
            
            # Step 2: Combine and deduplicate results
            all_documents = []
            for result in retrieval_results:
                all_documents.extend(result.source_documents)
            
            # Basic deduplication by content
            unique_documents = {}
            for doc in all_documents:
                # Use first 100 chars as a simple hash
                doc_hash = doc.content[:100]
                if doc_hash not in unique_documents:
                    unique_documents[doc_hash] = doc
            
            unique_docs_list = list(unique_documents.values())
            
            # Step 3: Send combined results to processing agent
            processing_result = await self.processing_agent.process({
                "documents": unique_docs_list,
                "question": query
            })
            
            # Step 4: Return final response
            return AgentResponse(
                agent_id=self.agent_id,
                content=processing_result.content,
                source_documents=unique_docs_list,
                metadata={
                    "retrieval_agents": [agent.agent_id for agent in self.retrieval_agents],
                    "processing_agent": self.processing_agent.agent_id,
                    "total_documents_retrieved": len(all_documents),
                    "unique_documents_processed": len(unique_docs_list)
                }
            )
        except Exception as e:
            self.logger.error(f"Error coordinating workflow: {str(e)}")
            return AgentResponse(
                agent_id=self.agent_id,
                content=f"Error coordinating workflow: {str(e)}",
                metadata={"error": str(e)}
            )
