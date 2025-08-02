**Epic 1: Data Ingestion & Preparation**

* **As a** Data Scientist, **I want** the system to automatically pick up PDF and DOCX files I place in a specific MinIO bucket, **so that** I don't have to manually upload each file for processing.  
* **As an** ML Engineer, **I want** the system to extract text and break it into logical chunks, **so that** the content is prepared for effective processing by the LLM.

**Epic 2: Synthetic Data Generation**

* **As a** Data Scientist, **I want** to trigger a process that uses an LLM to generate relevant question-answer pairs from my documents, **so that** I can create a domain-specific dataset with minimal effort.  
* **As an** ML Engineer, **I want** all generated Q\&A pairs, along with their source document and chunk metadata, to be stored in a PostgreSQL database, **so that** I can maintain data provenance and traceability.  
* **As a** Data Scientist, **I want** each generated Q\&A pair to have an `is_reviewed` flag, **so that** my team can later implement a curation workflow and filter for high-quality data.

**Epic 3: Data Access & Integration**

* **As a** Data Scientist, **I want** to easily export the entire Q\&A dataset into a single JSON file, **so that** I can load it directly into my fine-tuning scripts (e.g., for Hugging Face or Axolotl).  
* **As an** ML Engineer, **I want** to use a simple Python SDK to programmatically start the generation process and export the results, **so that** I can integrate this tool into our automated MLOps pipelines.  
* **As a** new Developer, **I want** to read clear and comprehensive documentation on MkDocs, **so that** I can quickly understand how to set up the environment and use the SDK.

