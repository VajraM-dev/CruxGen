# --- CRUD Functions ---

from sqlalchemy.orm import sessionmaker, declarative_base
from cruxgen.database.crud_models import File, Chunk, QAPair
from cruxgen.database.db_config import engine
from typing import List

Base = declarative_base()

Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

# file -------------------------------------
def create_file(session, file_name, dataset_generated):
    """Creates a new File record."""
    new_file = File(file_name=file_name, dataset_generated=dataset_generated)
    session.add(new_file)
    session.commit()
    return new_file

def get_file_by_id(session, file_id):
    """Retrieves a File by its ID."""
    return session.query(File).filter_by(file_id=file_id).one_or_none()

def get_file_id_by_name(session, file_name):
    """Retrieves a File ID by its name."""
    return session.query(File.file_id).filter_by(file_name=file_name).one_or_none()

def update_file_name(session, file_id, new_file_name):
    """Updates the file_name for a given file ID."""
    file = get_file_by_id(session, file_id)
    if file:
        file.file_name = new_file_name
        session.commit()
        return file
    return None

def update_dataset_generated(session, file_id, dataset_generated):
    """Updates the dataset_generated flag for a given file ID."""
    file = get_file_by_id(session, file_id)
    if file:
        file.dataset_generated = dataset_generated
        session.commit()
        return file
    return None

def delete_file(session, file_id):
    """Deletes a File and its related records (Chunk, QAPair) via cascading delete."""
    file = get_file_by_id(session, file_id)
    if file:
        session.delete(file)
        session.commit()
        return True
    return False

# chunk -------------------------------------

def create_chunk(session, file_id, chunk_text):
    """Creates a new Chunk record."""
    new_chunk = Chunk(file_id=file_id, chunk_text=chunk_text)
    session.add(new_chunk)
    session.commit()
    return new_chunk

def create_chunks_bulk(session, file_id: str, chunk_texts: List[str]):
   """Creates multiple Chunk records in bulk."""
   chunks = [Chunk(file_id=file_id, chunk_text=text) for text in chunk_texts]
   session.add_all(chunks)
   session.commit()
   return chunks

def get_chunk_by_id(session, chunk_id):
    """Retrieves a Chunk by its ID."""
    return session.query(Chunk).filter_by(chunk_id=chunk_id).one_or_none()

def update_chunk_text(session, chunk_id, new_chunk_text):
    """Updates the chunk_text for a given chunk ID."""
    chunk = get_chunk_by_id(session, chunk_id)
    if chunk:
        chunk.chunk_text = new_chunk_text
        session.commit()
        return chunk
    return None

def delete_chunk(session, chunk_id):
    """Deletes a Chunk and its related QAPair record."""
    chunk = get_chunk_by_id(session, chunk_id)
    if chunk:
        session.delete(chunk)
        session.commit()
        return True
    return False

def delete_chunks_by_file_id(session, file_id: str):
   """Deletes all Chunks for a given file_id."""
   deleted_count = session.query(Chunk).filter_by(file_id=file_id).delete()
   session.commit()
   return deleted_count

def get_chunks_by_file_id(session, file_id: str):
   """Gets all chunks for a given file_id."""
   return session.query(Chunk).filter_by(file_id=file_id).all()

def chunks_exist_for_file(session, file_id: str) -> bool:
    """Checks if chunks exist for a given file_id."""
    return session.query(Chunk).filter_by(file_id=file_id).first() is not None

# qa_pair -------------------------------------

def create_qa_pair(session, chunk_id, question, answer):
    """Creates a new QAPair record."""
    new_qa_pair = QAPair(chunk_id=chunk_id, question=question, answer=answer)
    session.add(new_qa_pair)
    session.commit()
    return new_qa_pair

def get_qa_pair_by_id(session, qa_id):
    """Retrieves a QAPair by its ID."""
    return session.query(QAPair).filter_by(qa_id=qa_id).one_or_none()

def update_qa_pair(session, qa_id, new_question, new_answer):
    """Updates the question and answer for a given QA pair ID."""
    qa_pair = get_qa_pair_by_id(session, qa_id)
    if qa_pair:
        qa_pair.question = new_question
        qa_pair.answer = new_answer
        session.commit()
        return qa_pair
    return None

def delete_qa_pair(session, qa_id):
    """Deletes a QAPair record."""
    qa_pair = get_qa_pair_by_id(session, qa_id)
    if qa_pair:
        session.delete(qa_pair)
        session.commit()
        return True
    return False

def delete_qa_pairs_by_file_id(session, file_id: str):
   """Deletes all QAPairs for a given file_id."""
   deleted_count = (
        session.query(QAPair)
        .filter(
            QAPair.chunk_id.in_(
                session.query(Chunk.chunk_id).filter(Chunk.file_id == file_id)
            )
        )
        .delete(synchronize_session=False)
    )
   session.commit()
   return deleted_count

def qa_pairs_exist_for_file(session, file_id: str) -> bool:
    """Checks if QA pairs exist for a given file_id."""
    return (
        session.query(QAPair)
        .join(Chunk, QAPair.chunk_id == Chunk.chunk_id)
        .filter(Chunk.file_id == file_id)
        .first()
        is not None
    )

def get_qa_pairs_by_file_id(session, file_id: str):
    """Gets all QA pairs for a given file_id."""
    qa_pairs = (
        session.query(QAPair)
        .join(Chunk, QAPair.chunk_id == Chunk.chunk_id)
        .filter(Chunk.file_id == file_id)
        .all()
    )
    questions_answers = [{"question": qa.question, "answer": qa.answer} for qa in qa_pairs]
    return questions_answers
# Example usage:
# if __name__ == '__main__':
#     with Session() as session:
#         print("Creating a new file...")
#         file_record = create_file(session, "my_document.txt", True)
#         print(f"Created file: {file_record}")

#         print("\nCreating a chunk for the file...")
#         chunk_record = create_chunk(session, file_record.file_id, "This is the first chunk of text from the document.")
#         print(f"Created chunk: {chunk_record}")

#         print("\nCreating a QA pair for the chunk...")
#         qa_pair_record = create_qa_pair(session, chunk_record.chunk_id, "What is this document about?", "The document is about a first chunk of text.")
#         print(f"Created QA pair: {qa_pair_record}")

#         print("\nUpdating the QA pair...")
#         updated_qa_pair = update_qa_pair(session, qa_pair_record.qa_id, "What is the content?", "The content is the first section of a document.")
#         print(f"Updated QA pair: {updated_qa_pair}")

#         print("\nDeleting the file record...")
#         # Note: Deleting the file will also cascade and delete the chunk and qa_pair
#         delete_file(session, file_record.file_id)
#         print("File and associated records deleted.")
        
#         # Verify deletion
#         print("\nChecking if records exist after deletion:")
#         print(f"File exists: {get_file_by_id(session, file_record.file_id) is not None}")
#         print(f"Chunk exists: {get_chunk_by_id(session, chunk_record.chunk_id) is not None}")
#         print(f"QA Pair exists: {get_qa_pair_by_id(session, qa_pair_record.qa_id) is not None}")
