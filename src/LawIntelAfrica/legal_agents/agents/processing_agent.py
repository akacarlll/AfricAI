from typing import Dict, Any
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from models.documents import AgentResponse
from utils.setup import setup_llm
class DocumentProcessingAgent(BaseAgent):
    """Agent that processes and analyzes retrieved documents."""
    
    def __init__(self, agent_id: str):
        super().__init__(agent_id)
        self.llm = setup_llm()
        self.prompt_template = PromptTemplate(
            input_variables=["documents", "question"],
            template="""
            You are a legal document analysis assistant. Based on the provided documents, 
            answer the following question:
            
            Question: {question}
            
            Documents:
            {documents}
            
            Provide a detailed analysis of the information found in these documents relevant to the question.
            Include citations to the specific documents where you found the information.
            """
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt_template)
    
    async def process(self, data: Dict[str, Any]) -> AgentResponse:
        """Process retrieved documents and extract relevant information."""
        try:
            self.logger.info("Processing documents")
            documents = data.get("documents", [])
            question = data.get("question", "")
            
            if not documents:
                return AgentResponse(
                    agent_id=self.agent_id,
                    content="No documents provided for analysis.",
                    metadata={"status": "error", "reason": "no_documents"}
                )
            
            # Format documents for the prompt
            formatted_docs = "\n\n".join(
                [f"Document {i+1} (Source: {doc.metadata.get('source', 'Unknown')}): {doc.content}" 
                 for i, doc in enumerate(documents)]
            )
            
            # Run the analysis chain
            result = self.chain.run(documents=formatted_docs, question=question)
            
            return AgentResponse(
                agent_id=self.agent_id,
                content=result,
                source_documents=documents,
                metadata={"analysis_type": "legal", "document_count": len(documents)}
            )
        except Exception as e:
            self.logger.error(f"Error processing documents: {str(e)}")
            return AgentResponse(
                agent_id=self.agent_id,
                content=f"Error processing documents: {str(e)}",
                metadata={"error": str(e)}
            )
