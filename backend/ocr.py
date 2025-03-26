from src import context
from src.external.ocr.textract import Textract
from src.forms.dd214 import DDTwoOneFour
from src.ocr import Ocr

appContext = context.ApplicationContext()
appContext.register(Ocr, Textract())


@context.inject
def get_ocr_engine(ocr_engine: Ocr = None, asdf: str = None):
    print(f"asdf={asdf}")
    return ocr_engine


if __name__ == "__main__":
    scanner = get_ocr_engine()
    form = DDTwoOneFour()
    result = scanner.scan("s3://document-extractor-gsa-dev-documents/test_dd214.jpg", queries=form.queries())

    for key, value in result.items():
        print(key)
        print(f"\t{value}")
