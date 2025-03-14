from src.external.ocr.paddle import Paddle

if __name__ == "__main__":
    # Example usage
    scanner = Paddle()

    # Scan a single image
    result = scanner.scan("s3://document-extractor-gsa-dev-documents/test_ws.jpg")

    print(result)
    # for key, value in result.items():
    #     print(key)
    #     print(value)
