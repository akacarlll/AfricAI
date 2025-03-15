
class KeywordSearchAgent(BaseAgent):
    """Agent that performs keyword-based search on documents."""
    
    def __init__(self, agent_id: str, db_path: str):
        super().__init__(agent_id)
        self.db_path = db_path
        self.client = chromadb.PersistentClient(path=db_path)
        self._load_collections()
        
    def _load_collections(self):
        """Load all collections from the database."""
        try:
            self.logger.info(f"Loading collections from {self.db_path}")
            self.collections = self.client.list_collections()
            self.logger.info(f"Found {len(self.collections)} collections")
        except Exception as e:
            self.logger.error(f"Failed to load collections: {str(e)}")
            raise
    
    async def process(self, query: Query) -> AgentResponse:
        """Perform keyword search based on the query."""
        try:
            self.logger.info(f"Processing query: {query.text}")
            results = []
            
            for collection_info in self.collections:
                collection = self.client.get_collection(collection_info.name)
                result = collection.query(
                    query_texts=[query.text],
                    n_results=query.top_k
                )
                
                for i, doc_id in enumerate(result['ids'][0]):
                    document = Document(
                        content=result['documents'][0][i],
                        metadata={
                            "id": doc_id,
                            "collection": collection_info.name,
                            "distance": result['distances'][0][i] if 'distances' in result else None,
                            **result['metadatas'][0][i] if 'metadatas' in result and result['metadatas'][0][i] else {}
                        }
                    )
                    results.append(document)
            
            return AgentResponse(
                agent_id=self.agent_id,
                content=f"Retrieved {len(results)} documents using keyword search.",
                source_documents=results,
                metadata={"method": "keyword_search"}
            )
        except Exception as e:
            self.logger.error(f"Error processing query: {str(e)}")
            return AgentResponse(
                agent_id=self.agent_id,
                content=f"Error retrieving documents: {str(e)}",
                metadata={"error": str(e)}
            )
