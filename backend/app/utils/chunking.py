"""Document chunking utilities for optimal RAG performance"""

from typing import List, Dict
import re

class DocumentChunker:
    def __init__(
        self,
        chunk_size: int = 512,
        chunk_overlap: int = 128,
        min_chunk_size: int = 100
    ):
        """
        Initialize document chunker
        
        Args:
            chunk_size: Target size for each chunk (in characters)
            chunk_overlap: Overlap between chunks to preserve context
            min_chunk_size: Minimum chunk size to avoid tiny fragments
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.min_chunk_size = min_chunk_size
    
    def chunk_by_sentences(self, text: str) -> List[str]:
        """
        Chunk text by sentences, respecting chunk_size
        
        Better for legal documents as it preserves semantic boundaries
        """
        # Split into sentences (simple regex, can be improved)
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        chunks = []
        current_chunk = []
        current_size = 0
        
        for sentence in sentences:
            sentence_size = len(sentence)
            
            # If adding this sentence exceeds chunk_size, save current chunk
            if current_size + sentence_size > self.chunk_size and current_chunk:
                chunks.append(' '.join(current_chunk))
                
                # Keep last few sentences for overlap
                overlap_text = ' '.join(current_chunk)
                overlap_sentences = []
                overlap_size = 0
                
                for s in reversed(current_chunk):
                    if overlap_size + len(s) <= self.chunk_overlap:
                        overlap_sentences.insert(0, s)
                        overlap_size += len(s)
                    else:
                        break
                
                current_chunk = overlap_sentences
                current_size = overlap_size
            
            current_chunk.append(sentence)
            current_size += sentence_size
        
        # Add remaining chunk
        if current_chunk and current_size >= self.min_chunk_size:
            chunks.append(' '.join(current_chunk))
        
        return chunks
    
    def chunk_by_sections(self, text: str, section_markers: List[str] = None) -> List[Dict]:
        """
        Chunk legal document by sections (e.g., "Section 1", "Article 14")
        
        Args:
            text: Document text
            section_markers: List of regex patterns for section markers
            
        Returns:
            List of chunks with metadata
        """
        if section_markers is None:
            section_markers = [
                r'Section\s+\d+',
                r'Article\s+\d+',
                r'Chapter\s+[IVX]+',
                r'Part\s+[IVX]+',
                r'\d+\.\s+[A-Z]'  # Numbered sections
            ]
        
        # Combine patterns
        pattern = '|'.join(f'({marker})' for marker in section_markers)
        
        # Split by sections
        sections = re.split(f'({pattern})', text)
        
        chunks = []
        current_section = None
        current_content = []
        
        for part in sections:
            if not part or part.isspace():
                continue
            
            # Check if this is a section marker
            if re.match(pattern, part):
                # Save previous section
                if current_section and current_content:
                    content = ' '.join(current_content).strip()
                    if len(content) >= self.min_chunk_size:
                        chunks.append({
                            "section": current_section,
                            "content": content,
                            "size": len(content)
                        })
                
                # Start new section
                current_section = part.strip()
                current_content = []
            else:
                current_content.append(part.strip())
        
        # Add last section
        if current_section and current_content:
            content = ' '.join(current_content).strip()
            if len(content) >= self.min_chunk_size:
                chunks.append({
                    "section": current_section,
                    "content": content,
                    "size": len(content)
                })
        
        return chunks
    
    def chunk_with_metadata(
        self,
        text: str,
        doc_id: str,
        title: str,
        **metadata
    ) -> List[Dict]:
        """
        Chunk document and preserve metadata for each chunk
        
        Returns:
            List of chunks with full metadata
        """
        # Try section-based chunking first
        section_chunks = self.chunk_by_sections(text)
        
        if section_chunks:
            # Use section-based chunks
            chunks = []
            for i, chunk in enumerate(section_chunks):
                chunks.append({
                    "chunk_id": f"{doc_id}_chunk_{i}",
                    "doc_id": doc_id,
                    "title": title,
                    "section": chunk["section"],
                    "content": chunk["content"],
                    "chunk_index": i,
                    "total_chunks": len(section_chunks),
                    **metadata
                })
            return chunks
        else:
            # Fall back to sentence-based chunking
            sentence_chunks = self.chunk_by_sentences(text)
            chunks = []
            for i, content in enumerate(sentence_chunks):
                chunks.append({
                    "chunk_id": f"{doc_id}_chunk_{i}",
                    "doc_id": doc_id,
                    "title": title,
                    "content": content,
                    "chunk_index": i,
                    "total_chunks": len(sentence_chunks),
                    **metadata
                })
            return chunks

# Global chunker instance
document_chunker = DocumentChunker()
