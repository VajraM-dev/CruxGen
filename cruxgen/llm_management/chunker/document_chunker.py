from langchain_docling.loader import ExportType
from docling.chunking import HybridChunker
from langchain_docling import DoclingLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter

class CustomDocSpliter:
    def __init__(self, 
                 model_id: str = "Qwen/Qwen3-Embedding-0.6B",
                 export_type: ExportType = ExportType.DOC_CHUNKS,
                 embedding_dimensions: int = 1024,
                 max_tokens: int = 1000,
                 ):
        self.model_id = model_id
        self.export_type = export_type
        self.embedding_dimensions = embedding_dimensions
        self.max_tokens = max_tokens
        self.chunker = HybridChunker(tokenizer=self.model_id, max_tokens=self.max_tokens)
        
    def _load_doc_split(self, file_path: str):
        loader = DoclingLoader(
            file_path=file_path,
            export_type=self.export_type,
            chunker=self.chunker
        )
        docs = loader.load()

        if self.export_type == ExportType.DOC_CHUNKS:
            splits = docs
        elif self.export_type == ExportType.MARKDOWN:
            
            splitter = MarkdownHeaderTextSplitter(
                headers_to_split_on=[
                    ("#", "Header_1"),
                    ("##", "Header_2"),
                    ("###", "Header_3"),
                ],
            )
            splits = [split for doc in docs for split in splitter.split_text(doc.page_content)]

        else:
            raise ValueError(f"Unexpected export type: {self.export_type}")
        
        splits = [split.page_content for split in splits]

        return splits
    
    def _club_chunks(self, chunks: list[str], max_tokens: int) -> list[str]:
        result = []
        current_batch = []
        current_tokens = 0
        
        for chunk in chunks:
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
    
    def load_and_club(self, file_path: str) -> list[str]:
        splits = self._load_doc_split(file_path)
        clubbed_splits = self._club_chunks(splits, self.max_tokens)
        return clubbed_splits