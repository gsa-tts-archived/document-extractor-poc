from src.external.ocr.textract import Textract

if __name__ == "__main__":
    scanner = Textract()
    result = scanner.detect_document_type("s3://document-extractor-gsa-dev-documents/test_1099.jpg")

    print(f"Document type is {result}")
