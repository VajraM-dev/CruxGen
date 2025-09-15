from cruxgen_sdk.sdk import CruxGenSDK

def main():
    with CruxGenSDK("http://localhost:8000") as sdk:
        
        # Health check
        health = sdk.health_check()
        print("Health:", health)
        
        # Create bucket
        bucket = sdk.create_bucket("test-bucket")
        print("Bucket created:", bucket)
        
        # List buckets
        buckets = sdk.list_buckets()
        print("Buckets:", buckets)
        
        file_path = r"<Path>\file_name"

        # Upload file
        upload = sdk.upload_file(file_path, bucket_name="test-bucket")
        print("File uploaded:", upload)
        file_id = upload["response"]
        
        # Get file ID by name
        file_info = sdk.get_file_id_by_name("file_name")
        print("File info:", file_info)
        
        # List objects in bucket
        objects = sdk.list_objects("test-bucket")
        print("Objects:", objects)
        
        # Get object info
        obj_info = sdk.get_object_info("test-bucket", "file_name")
        print("Object info:", obj_info)

        get_file_id_by_name = sdk.get_file_id_by_name("file_name")
        file_id = get_file_id_by_name["response"]
        print("File ID:", file_id)
        
        # Create chunks from file
        chunks = sdk.create_chunks(file_id, "test-bucket")
        print("Chunks created:", chunks)
        
        # Get chunks
        chunk_list = sdk.get_chunks(file_id)
        print("Chunks:", chunk_list)
        
        # Create QA pairs from chunks
        qa = sdk.create_qa_pairs(file_id)
        print("QA pairs created:", qa)
        
        # Get QA pairs
        qa_pairs = sdk.get_qa_pairs(file_id)
        print("QA pairs:", qa_pairs)
        
        # Get QA pairs as JSONL
        qa_jsonl = sdk.get_qa_pairs(file_id, generate_jsonl=True)
        if isinstance(qa_jsonl, bytes):
            with open(f"qa_pairs_{file_id}.jsonl", "wb") as f:
                f.write(qa_jsonl)
        print("QA JSONL:", qa_jsonl)
        
        # Delete QA pairs
        delete_qa = sdk.delete_qa_pairs(file_id)
        print("QA pairs deleted:", delete_qa)
        
        # Delete chunks
        delete_chunks = sdk.delete_chunks(file_id)
        print("Chunks deleted:", delete_chunks)
        
        # Delete object
        delete_obj = sdk.delete_object("test-bucket", "file_name")
        print("Object deleted:", delete_obj)
        
        # Delete bucket
        delete_bucket = sdk.delete_bucket("test-bucket")
        print("Bucket deleted:", delete_bucket)