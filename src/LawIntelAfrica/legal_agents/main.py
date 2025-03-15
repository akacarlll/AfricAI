import asyncio
from agents.retrieval.keyword_agent import KeywordSearchAgent
from agents.retrieval.semantic_agent import SemanticSearchAgent
from agents.coordinator_agent import CoordinatorAgent
from agents.processing_agent import DocumentProcessingAgent
import logging
from config import CHROMA_PATH_1
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def main():
    """Main function to set up and run the agent workflow."""
    try:
        logger.info("Setting up agents...")
        
        # Set up retrieval agents
        semantic_agent = SemanticSearchAgent("semantic_search", CHROMA_PATH_1)
        keyword_agent = KeywordSearchAgent("keyword_search", CHROMA_PATH_1)
        
        # Set up processing agent
        processing_agent = DocumentProcessingAgent("document_processor")
        
        # Set up coordinator agent
        coordinator = CoordinatorAgent(
            "workflow_coordinator", 
            [semantic_agent, keyword_agent], 
            processing_agent
        )
        
        # Run the workflow
        query = "What are the legal requirements for starting a business in Africa?"
        logger.info(f"Running workflow with query: {query}")
        
        result = await coordinator.process(query)
        
        logger.info("Workflow completed successfully")
        logger.info(f"Final response: {result.content}")
        
        # Print source documents
        print("\nSource Documents:")
        for i, doc in enumerate(result.source_documents[:3]):  # Print first 3 docs
            print(f"\nDocument {i+1}:")
            print(f"Content: {doc.content[:100]}...")  # Print first 100 chars
            print(f"Metadata: {doc.metadata}")
        
        return result
    
    except Exception as e:
        logger.error(f"Error in main workflow: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())