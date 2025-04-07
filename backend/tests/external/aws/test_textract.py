from src.external.aws import textract
from src.forms.w2 import W2


def test_textract():
    w2 = W2()
    response = textract.Textract._split_list_by_30(w2.queries())

    print(len(response[0]))
    print(len(response[1]))
    assert True
