from src import context
from src.external.ocr.textract import Textract
from src.forms.dd214 import DDTwoOneFour

appContext = context.ApplicationContext()
appContext.register("ocr_engine", Textract())

if __name__ == "__main__":
    scanner = appContext.implementation("ocr_engine")
    form = DDTwoOneFour()
    result = scanner.scan("s3://document-extractor-gsa-dev-documents/test_dd214.jpg", queries=form.queries())

    for key, value in result.items():
        print(key)
        print(f"\t{value}")
