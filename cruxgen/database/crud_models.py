import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

# Define the base for declarative models
Base = declarative_base()

# --- Model Definitions ---

class File(Base):
    """
    SQLAlchemy model for the 'files' table.
    A file can have one associated chunk.
    """
    __tablename__ = 'files'

    file_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    file_name = Column(String, nullable=False)
    dataset_generated = Column(Boolean, nullable=False)

    # Defines a one-to-one relationship to Chunk.
    # The 'uselist=False' argument is crucial for a one-to-one relationship.
    # The 'back_populates' argument links the relationship back to the 'Chunk' model.
    chunk = relationship("Chunk", back_populates="file", uselist=False)

    def __repr__(self):
        return f"<File(file_id='{self.file_id}', file_name='{self.file_name}')>"


class Chunk(Base):
    """
    SQLAlchemy model for the 'chunks' table.
    A chunk is associated with one file and one QA pair.
    """
    __tablename__ = 'chunks'

    chunk_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    file_id = Column(UUID(as_uuid=True), ForeignKey('files.file_id'), unique=True, nullable=False)
    chunk_text = Column(String, nullable=False)

    # Defines a one-to-one relationship to File.
    file = relationship("File", back_populates="chunk", uselist=False)
    
    # Defines a one-to-one relationship to QAPair.
    qa_pair = relationship("QAPair", back_populates="chunk", uselist=False)

    def __repr__(self):
        return f"<Chunk(chunk_id='{self.chunk_id}', file_id='{self.file_id}')>"


class QAPair(Base):
    """
    SQLAlchemy model for the 'qa_pairs' table.
    A QA pair is associated with one chunk.
    """
    __tablename__ = 'qa_pairs'

    qa_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    chunk_id = Column(UUID(as_uuid=True), ForeignKey('chunks.chunk_id'), unique=True, nullable=False)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)

    # Defines a one-to-one relationship to Chunk.
    chunk = relationship("Chunk", back_populates="qa_pair", uselist=False)

    def __repr__(self):
        return f"<QAPair(qa_id='{self.qa_id}', chunk_id='{self.chunk_id}')>"
