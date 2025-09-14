"""
Professional AI Service for Web Scraping
Clean, efficient, and scalable AI-powered content extraction
"""
import time
import logging
from typing import List, Dict, Any, Optional
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from config import AI_MODEL, AI_TEMPERATURE, CHUNK_SIZE

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProfessionalAIService:
    """
    Professional AI service for intelligent content extraction
    Features: Error handling, logging, chunking, and performance monitoring
    """
    
    def __init__(self):
        """Initialize the AI service with proper error handling"""
        try:
            self.model = OllamaLLM(
                model=AI_MODEL,
                temperature=AI_TEMPERATURE
            )
            self.prompt_template = self._create_optimized_prompt()
            logger.info(f"AI Service initialized with model: {AI_MODEL}")
        except Exception as e:
            logger.error(f"Failed to initialize AI service: {e}")
            raise
    
    def _create_optimized_prompt(self) -> ChatPromptTemplate:
        """Create an optimized prompt template for better extraction"""
        template = """
You are an expert AI assistant specialized in extracting structured information from web content.

TASK: Extract specific information from the provided content.

CONTENT:
{content}

INSTRUCTIONS:
{instructions}

REQUIREMENTS:
1. Extract only the requested information
2. Maintain data accuracy and consistency
3. If no relevant data is found, return "No relevant data found"
4. Format output clearly and structured
5. Preserve original data relationships

OUTPUT:
"""
        return ChatPromptTemplate.from_template(template)
    
    def extract_content(self, content: str, instructions: str) -> Dict[str, Any]:
        """
        Extract content using AI with professional error handling
        
        Args:
            content: The web content to extract from
            instructions: What to extract (e.g., "Extract all product names and prices")
        
        Returns:
            Dictionary with extracted content and metadata
        """
        start_time = time.time()
        
        try:
            # Validate inputs
            if not content or not content.strip():
                return self._create_error_result("Empty content provided", start_time)
            
            if not instructions or not instructions.strip():
                return self._create_error_result("No extraction instructions provided", start_time)
            
            # Split content into manageable chunks
            chunks = self._intelligent_chunking(content)
            logger.info(f"Processing {len(chunks)} chunks for extraction")
            
            # Process each chunk
            results = []
            successful_chunks = 0
            
            for i, chunk in enumerate(chunks):
                try:
                    result = self._process_chunk(chunk, instructions, i + 1, len(chunks))
                    results.append(result)
                    if result.strip():
                        successful_chunks += 1
                except Exception as e:
                    logger.warning(f"Error processing chunk {i + 1}: {e}")
                    results.append("")
            
            # Combine and clean results
            combined_result = self._combine_results(results)
            processing_time = time.time() - start_time
            
            # Calculate confidence score
            confidence = successful_chunks / len(chunks) if chunks else 0
            
            logger.info(f"Extraction completed in {processing_time:.2f}s with {confidence:.2f} confidence")
            
            return {
                "success": True,
                "content": combined_result,
                "confidence": confidence,
                "processing_time": processing_time,
                "chunks_processed": len(chunks),
                "successful_chunks": successful_chunks,
                "model_used": AI_MODEL,
                "metadata": {
                    "content_length": len(content),
                    "chunk_size": CHUNK_SIZE,
                    "temperature": AI_TEMPERATURE
                }
            }
            
        except Exception as e:
            logger.error(f"Extraction failed: {e}")
            return self._create_error_result(str(e), start_time)
    
    def _process_chunk(self, chunk: str, instructions: str, chunk_num: int, total_chunks: int) -> str:
        """Process a single chunk with error handling"""
        try:
            chain = self.prompt_template | self.model
            response = chain.invoke({
                "content": chunk,
                "instructions": instructions
            })
            
            result = str(response).strip()
            logger.debug(f"Processed chunk {chunk_num}/{total_chunks}")
            return result
            
        except Exception as e:
            logger.warning(f"Failed to process chunk {chunk_num}: {e}")
            return ""
    
    def _intelligent_chunking(self, content: str) -> List[str]:
        """
        Intelligent content chunking that preserves context
        """
        if len(content) <= CHUNK_SIZE:
            return [content]
        
        chunks = []
        
        # Try to split by paragraphs first
        paragraphs = content.split('\n\n')
        current_chunk = ""
        
        for paragraph in paragraphs:
            # If adding this paragraph would exceed chunk size
            if len(current_chunk) + len(paragraph) > CHUNK_SIZE and current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = paragraph
            else:
                current_chunk += "\n\n" + paragraph if current_chunk else paragraph
        
        # Add the last chunk
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        # If still too large, split by sentences
        if len(chunks) == 1 and len(chunks[0]) > CHUNK_SIZE:
            return self._split_by_sentences(content)
        
        return chunks
    
    def _split_by_sentences(self, content: str) -> List[str]:
        """Fallback: split by sentences if paragraphs don't work"""
        sentences = content.split('. ')
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) > CHUNK_SIZE and current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:
                current_chunk += ". " + sentence if current_chunk else sentence
        
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def _combine_results(self, results: List[str]) -> str:
        """Combine results from multiple chunks intelligently"""
        # Filter out empty results
        valid_results = [r for r in results if r and r.strip()]
        
        if not valid_results:
            return "No relevant data found"
        
        # Remove duplicates while preserving order
        seen = set()
        unique_results = []
        for result in valid_results:
            if result not in seen:
                seen.add(result)
                unique_results.append(result)
        
        return "\n\n".join(unique_results)
    
    def _create_error_result(self, error_message: str, start_time: float) -> Dict[str, Any]:
        """Create a standardized error result"""
        return {
            "success": False,
            "content": "",
            "error": error_message,
            "confidence": 0.0,
            "processing_time": time.time() - start_time,
            "chunks_processed": 0,
            "successful_chunks": 0,
            "model_used": AI_MODEL
        }
    
    def get_service_info(self) -> Dict[str, Any]:
        """Get comprehensive service information"""
        return {
            "model": AI_MODEL,
            "temperature": AI_TEMPERATURE,
            "chunk_size": CHUNK_SIZE,
            "status": "operational",
            "features": [
                "intelligent_chunking",
                "error_handling",
                "confidence_scoring",
                "performance_monitoring"
            ]
        }
    
    def health_check(self) -> Dict[str, Any]:
        """Perform a health check on the AI service"""
        try:
            # Test with a simple query
            test_result = self.extract_content(
                "Test content for health check",
                "Extract any text"
            )
            
            return {
                "status": "healthy" if test_result["success"] else "degraded",
                "model": AI_MODEL,
                "response_time": test_result["processing_time"],
                "timestamp": time.time()
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": time.time()
            }