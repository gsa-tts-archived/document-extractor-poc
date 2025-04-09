from src.external.aws.textract import Textract
from src.forms.w2 import W2


def test_textract_split_w2_queries_by_30():
    w2 = W2()
    textract = Textract()

    response = textract._split_list_by_30(w2.queries())

    assert len(response[0]) == 30
    assert len(response[1]) == 5


def test_textract_parse_query_response():
    mock_textract_response = {
        "DocumentMetadata": {"Pages": 1},
        "Blocks": [
            {
                "BlockType": "QUERY",
                "Confidence": 0.99,
                "Text": "What does a dogcow say?",
                "TextType": "PRINTED",
                "RowIndex": 1,
                "ColumnIndex": 1,
                "RowSpan": 1,
                "ColumnSpan": 1,
                "Id": "123",
                "Page": 1,
                "Relationships": [
                    {
                        "Type": "ANSWER",
                        "Ids": [
                            "1234",
                        ],
                    },
                ],
                "Query": {
                    "Text": "What did the DogCow say?",
                    "Alias": "DogCow",
                    "Pages": [
                        "1",
                    ],
                },
            },
            {
                "BlockType": "QUERY_RESULT",
                "Confidence": 0.99,
                "Text": "Moof!",
                "TextType": "PRINTED",
                "RowIndex": 1,
                "ColumnIndex": 1,
                "RowSpan": 1,
                "ColumnSpan": 1,
                "Id": "1234",
                "Page": 1,
                "Relationships": [
                    {
                        "Type": "ANSWER",
                        "Ids": [
                            "1234",
                        ],
                    },
                ],
                "Query": {
                    "Text": "What did the DogCow say?",
                    "Alias": "DogCow",
                    "Pages": [
                        "1",
                    ],
                },
            },
        ],
        "AnalyzeDocumentModelVersion": "1.0",
    }

    textract = Textract()

    actual_parsed_response = textract._parse_textract_queries(mock_textract_response)

    assert actual_parsed_response == {"What did the DogCow say?": {"value": "Moof!", "confidence": 0.99}}


def test_textract_parse_textract_form():
    mocked_textract_response = {
        "DocumentMetadata": {"Pages": 1},
        "Blocks": [
            {
                "BlockType": "KEY_VALUE_SET",
                "Confidence": 0.99,
                "Text": "Dogcow",
                "TextType": "PRINTED",
                "RowIndex": 1,
                "ColumnIndex": 1,
                "RowSpan": 1,
                "ColumnSpan": 1,
                "Id": "1234",
                "Relationships": [
                    {
                        "Type": "CHILD",
                        "Ids": [
                            "123",
                        ],
                    },
                ],
                "EntityTypes": ["KEY"],
                "Page": 1,
            },
            {
                "BlockType": "LINE",
                "Confidence": 0.99,
                "Text": "Moof!",
                "TextType": "PRINTED",
                "RowIndex": 1,
                "ColumnIndex": 1,
                "RowSpan": 1,
                "ColumnSpan": 1,
                "Id": "123",
                "EntityTypes": ["VALUE"],
                "Page": 1,
            },
        ],
        "AnalyzeDocumentModelVersion": "1",
    }

    textract = Textract()

    actual_parsed_response = textract._parse_textract_forms(mocked_textract_response)

    print(actual_parsed_response)
    assert True
