CREATE TABLE public.files (
    file_id UUID PRIMARY KEY,
    file_name VARCHAR(255) NOT NULL,
    dataset_generated BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE public.chunks (
    chunk_id UUID PRIMARY KEY,
    file_id UUID NOT NULL UNIQUE,  -- Add UNIQUE constraint here
    chunk_text TEXT NOT NULL,
    FOREIGN KEY (file_id) REFERENCES files (file_id) ON DELETE CASCADE
);

CREATE TABLE public.qa_pairs (
    qa_id UUID PRIMARY KEY,
    chunk_id UUID NOT NULL UNIQUE, -- Add UNIQUE constraint here
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    FOREIGN KEY (chunk_id) REFERENCES chunks (chunk_id) ON DELETE CASCADE
);


CREATE INDEX idx_chunks_file_id ON chunks(file_id);
CREATE INDEX idx_qa_pairs_chunk_id ON qa_pairs(chunk_id);