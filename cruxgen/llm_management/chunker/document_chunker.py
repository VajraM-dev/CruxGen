from pathlib import Path
from typing import List
from pydantic import BaseModel, Field, field_validator
from langchain_docling.loader import ExportType
from docling.chunking import HybridChunker
# from langchain_docling import DoclingLoader
from docling.document_converter import DocumentConverter
from langchain_text_splitters import MarkdownHeaderTextSplitter
from cruxgen.configuration.logging_config import monitor
import tempfile
from cruxgen.document_managment.minio_config import client
from cruxgen.pydantic_models.generic_output_model import OutputResponse
from cruxgen.database.crud_functions import get_file_by_id, Session, create_chunks_bulk, chunks_exist_for_file

with Session() as session:
    # Create a new session for database operations
    db = session

class ChunkerConfig(BaseModel):
    model_id: str = Field(default="Qwen/Qwen3-Embedding-0.6B")
    export_type: ExportType = Field(default=ExportType.DOC_CHUNKS)
    embedding_dimensions: int = Field(default=1024, gt=0)
    max_tokens: int = Field(default=1024, gt=0)
    
    @field_validator('model_id')
    def validate_model_id(cls, v):
        if not v or not isinstance(v, str):
            raise ValueError("model_id must be non-empty string")
        return v

class DocumentSplitter:
    def __init__(self, config: ChunkerConfig):
        self.config = config
        try:
            self.chunker = HybridChunker(
                tokenizer=config.model_id, 
                max_tokens=config.max_tokens
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize chunker: {e}")
        
    # @monitor
    # def _load_doc_split(self, file_path: Path) -> List[str]:
    #     if not file_path.exists():
    #         raise FileNotFoundError(f"File not found: {file_path}")
        
    #     try:
    #         loader = DoclingLoader(
    #             file_path=str(file_path),
    #             export_type=self.config.export_type,
    #             chunker=self.chunker
    #         )
    #         docs = loader.load()
            
    #         if not docs:
    #             return []

    #         splits = self._process_docs(docs)
            
    #     except Exception as e:
    #         raise RuntimeError(f"Failed to load document: {e}")
        
    #     return [split.page_content for split in splits if hasattr(split, 'page_content')]
    
    def _load_doc_split(self, file_path: Path) -> List[str]:
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            converter = DocumentConverter()
            doc = converter.convert(file_path).document
            chunk_iter = self.chunker.chunk(dl_doc=doc)

            enriched_text = []
            for _, chunk in enumerate(chunk_iter):
                enriched_text.append(self.chunker.contextualize(chunk=chunk) + "\n\n")

            return enriched_text
        except Exception as e:
            raise RuntimeError(f"Failed to load document: {e}")

    def _process_docs(self, docs):
        if self.config.export_type == ExportType.DOC_CHUNKS:
            return docs
        
        elif self.config.export_type == ExportType.MARKDOWN:
            splitter = MarkdownHeaderTextSplitter(
                headers_to_split_on=[
                    ("#", "Header_1"),
                    ("##", "Header_2"),  
                    ("###", "Header_3"),
                ],
            )
            splits = []
            for doc in docs:
                try:
                    doc_splits = splitter.split_text(doc.page_content)
                    splits.extend(doc_splits)
                except Exception:
                    splits.append(doc)
            return splits
        
        else:
            raise ValueError(f"Unsupported export type: {self.config.export_type}")

    def _club_chunks(self, chunks: List[str], max_tokens: int) -> List[str]:
        if not chunks:
            return []
        
        result = []
        current_batch = []
        current_tokens = 0
        
        for chunk in chunks:
            if not chunk or not chunk.strip():
                continue
                
            chunk_tokens = len(chunk.split())
            
            if current_tokens + chunk_tokens <= max_tokens:
                current_batch.append(chunk)
                current_tokens += chunk_tokens
            else:
                if current_batch:
                    result.append(' '.join(current_batch))
                current_batch = [chunk]
                current_tokens = chunk_tokens
        
        if current_batch:
            result.append(' '.join(current_batch))
        
        return result

    def _download_from_minio(self, file_id: str, bucket_name: str) -> Path:
        result = get_file_by_id(db, file_id)
        
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_path = Path(temp_file.name)
        temp_file.close()  # Close before fget_object uses it
        
        client.fget_object(bucket_name, result.file_name, str(temp_path))
        return temp_path

    @monitor
    def load_and_club(self, file_id: str, bucket_name: str) -> List[str]:

        if chunks_exist_for_file(db, file_id=file_id):
            return OutputResponse(
                success=True,
                message="There are chunks already present for this file",
            )
        
        try:
            temp_file = self._download_from_minio(file_id, bucket_name)

            splits = self._load_doc_split(temp_file)

            if not splits:
                return OutputResponse(success=False, message="Error creating chunks from chunker. Got empty list.") #[]
            
            splits = self._club_chunks(splits, self.config.max_tokens)
            
            _ = create_chunks_bulk(db, file_id=file_id, chunk_texts=splits)

            return OutputResponse(
                success=True,
                message="Splits created",
            )
            
        except Exception as e:
            return OutputResponse(success=False, message=f"Error creating chunks: {e}")