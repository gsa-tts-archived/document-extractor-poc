from src import context
from src.external.aws.textract import Textract
from src.forms.w2 import W2
from src.ocr import Ocr

appContext = context.ApplicationContext()
appContext.register(Ocr, Textract())


if __name__ == "__main__":
    scanner = appContext.implementation(Ocr)
    form = W2()
    result = scanner.scan("s3://document-extractor-gsa-dev-documents/test_w2.jpg", form)

    for key, value in result.items():
        print(key)
        print(f"\t{value}")
