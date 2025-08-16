# from cruxgen.document_managment.minio_operations import *
# from cruxgen.pydantic_models.minio_models import *

# # Example usage
# if __name__ == "__main__":
#     bucket_name = "test-bucket"
    
#     # CREATE
#     # create_bucket(MinioBucket(bucket_name=bucket_name))

#     # file_name = r"C:\Users\Prathamesh\Downloads\Data Migration and Validation Demo.pdf"
#     # upload_file(MinioUploadFile(bucket_name=bucket_name, object_name="Data Migration and Validation Demo.pdf", file_path=file_name))

    
#     # # READ
#     # list_buckets(MinioListBuckets())

#     # list_objects(MinioListObjects(bucket_name=bucket_name))

#     # data = get_object_data(MinioObjectInfo(bucket_name=bucket_name, object_name="Data Migration and Validation Demo.pdf"))
#     # print(f"Object data: {data['result'].decode('utf-8')}")
    
#     # # DELETE
#     delete_object(MinioDeleteObject(bucket_name=bucket_name, object_name="Data Migration and Validation Demo.pdf"))
#     # delete_bucket(bucket_name)