from src.external.ocr.textract import Textract
from src.forms import w2

if __name__ == "__main__":
    scanner = Textract()
    result = scanner.scan("s3://document-extractor-gsa-dev-documents/test_ws.jpg", queries=w2.queries)

    for key, value in result.items():
        print(key)
        print(f"\t{value}")
