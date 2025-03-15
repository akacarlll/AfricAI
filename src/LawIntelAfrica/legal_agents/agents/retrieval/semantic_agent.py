
class SemanticSearchAgent(BaseAgent):
    """Agent that performs semantic search on vector database."""
    
    def __init__(self, agent_id: str, db_path: str):
        super().__init__(agent_id)
        self.db_path = db_path
        self.embeddings = setup_embeddings()
        self.vectorstore = self._load_vectorstore()
        
    def _load_vectorstore(self):
        """Load the vector store from the database path."""
        try:
            self.logger.info(f"Loading vector store from {self.db_path}")
            return Chroma(persist_directory=self.db_path, embedding_function=self.embeddings)
        except Exception as e:
            self.logger.error(f"Failed to load vector store: {str(e)}")
            raise
    
    async def process(self, query: Query) -> AgentResponse:
        """Perform semantic search based on the query."""
        try:
            self.logger.info(f"Processing query: {query.text}")
            docs = self.vectorstore.similarity_search(
                query.text, 
                k=query.top_k,
                filter=query.filters
            )
            
            documents = [Document(content=doc.page_content, metadata=doc.metadata) for doc in docs]
            
            return AgentResponse(
                agent_id=self.agent_id,
                content=f"Retrieved {len(documents)} documents using semantic search.",
                source_documents=documents,
                metadata={"method": "semantic_search"}
            )
        except Exception as e:
            self.logger.error(f"Error processing query: {str(e)}")
            return AgentResponse(
                agent_id=self.agent_id,
                content=f"Error retrieving documents: {str(e)}",
                metadata={"error": str(e)}
            )
