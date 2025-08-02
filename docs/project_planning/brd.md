**Project Name:** SynthDataGen **Version:** 1.0 **Date:** August 2, 2025

**1\. Introduction** This document outlines the business requirements for the SynthDataGen project. The project's goal is to create a system that automates the generation of synthetic datasets from internal company documents to support LLM fine-tuning and optimization efforts.

**2\. Business Problem** The manual creation of question-answer datasets from domain-specific documents is a critical bottleneck for enterprise AI adoption. This process is slow, expensive, and non-scalable, which hinders the ability to build and deploy custom AI solutions that understand the unique context of the business.

**3\. Project Goals and Objectives**

* **Goal:** To significantly reduce the time and effort required to create training datasets for LLMs.  
* **Objective 1:** Automate the end-to-end process from document ingestion to dataset export.  
* **Objective 2:** Generate high-relevance question-answer pairs from unstructured PDF and DOCX documents.  
* **Objective 3:** Provide a robust, developer-friendly SDK for integration into CI/CD and MLOps workflows.  
* **Objective 4:** Ensure data is stored in a structured, queryable format that allows for future enhancements like manual review and curation.

**4\. Scope**

* **In-Scope:**  
  * Ingestion of `.pdf` and `.docx` files from a specified MinIO bucket.  
  * Text extraction from these documents.  
  * Strategic chunking of extracted text.  
  * Creation of "context chunks" by combining related text chunks.  
  * Using a pre-existing LLM (via API) to generate question-answer pairs.  
  * Storing documents, chunks, and Q\&A pairs in a PostgreSQL database with the specified schema.  
  * Functionality to export the Q\&A dataset as a JSON file.  
  * A Python SDK for programmatic control of the pipeline.  
  * Project documentation created using MkDocs.  
* **Out-of-Scope:**  
  * A user interface (UI) for uploading documents or reviewing Q\&A pairs.  
  * The fine-tuning process of the target LLM itself.  
  * Hosting or deployment of the fine-tuned models.  
  * Processing of structured data sources (e.g., CSV, JSON) in this phase.  
  * Real-time data generation. The process is designed to be run as a batch job.

**5\. Functional Requirements**

* **FR-1: Document Ingestion:** The system shall monitor a designated MinIO bucket and process new PDF and DOCX documents.  
* **FR-2: Content Processing:** The system shall accurately extract all text content from the documents and split it into smaller, coherent chunks.  
* **FR-3: Context Generation:** The system shall implement a mechanism to group related chunks to form a larger "context chunk" to be fed to the LLM.  
* **FR-4: Q\&A Generation:** The system shall send context chunks to a configured LLM API and parse the returned question-answer pairs.  
* **FR-5: Data Storage:** The system shall store all data and metadata in a PostgreSQL database according to the defined schema (Documents, Chunks, Context Chunk, Master Q\&A Table).  
* **FR-6: Data Export:** The system shall provide a function to export all reviewed Q\&A pairs from the `Master` table into a single JSON file.  
* **FR-7: SDK:** The system shall provide a Python SDK with functions to initiate the generation process, check status, and trigger the export.

**6\. Non-Functional Requirements**

* **NFR-1: Scalability:** The system should be able to process a corpus of at least 1,000 documents without significant performance degradation.  
* **NFR-2: Reliability:** The system must include robust error handling for failed document parsing, API calls, and database connections.  
* **NFR-3: Usability:** The SDK must be well-documented with clear examples to ensure ease of use for ML Engineers.  
* **NFR-4: Maintainability:** The code should be modular and well-commented to allow for future extensions (e.g., supporting new file types).

**7\. Assumptions & Constraints**

* **Assumption:** Access to a MinIO instance, a PostgreSQL database, and valid API keys for a generator LLM will be provided.  
* **Assumption:** Documents contain machine-readable text. Scanned PDFs (images of text) are not in scope for V1.  
* **Constraint:** The initial development will be in Python.  
* **Constraint:** The quality of the generated Q\&A pairs is dependent on the quality of the source documents and the capabilities of the generator LLM.

