from src.external.ocr.textract import Textract
from src.forms.ten_ninety_nine_nec import TenNinetyNineNec

if __name__ == "__main__":
    scanner = Textract()
    form = TenNinetyNineNec()
    result = scanner.scan("s3://document-extractor-gsa-dev-documents/test_1099.jpg", queries=form.queries())

    for key, value in result.items():
        print(key)
        print(f"\t{value}")
