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
    # mocked_textract_response = {
    #     "DocumentMetadata": {"Pages": 1},
    #     "Blocks": [
    #         {
    #             "BlockType": "KEY_VALUE_SET"
    #             | "PAGE"
    #             | "LINE"
    #             | "WORD"
    #             | "TABLE"
    #             | "CELL"
    #             | "SELECTION_ELEMENT"
    #             | "MERGED_CELL"
    #             | "TITLE"
    #             | "QUERY"
    #             | "QUERY_RESULT"
    #             | "SIGNATURE"
    #             | "TABLE_TITLE"
    #             | "TABLE_FOOTER"
    #             | "LAYOUT_TEXT"
    #             | "LAYOUT_TITLE"
    #             | "LAYOUT_HEADER"
    #             | "LAYOUT_FOOTER"
    #             | "LAYOUT_SECTION_HEADER"
    #             | "LAYOUT_PAGE_NUMBER"
    #             | "LAYOUT_LIST"
    #             | "LAYOUT_FIGURE"
    #             | "LAYOUT_TABLE"
    #             | "LAYOUT_KEY_VALUE",
    #             "Confidence": ...,
    #             "Text": "string",
    #             "TextType": "PRINTED",
    #             "RowIndex": 1,
    #             "ColumnIndex": 1,
    #             "RowSpan": 1,
    #             "ColumnSpan": 1,
    #             "Geometry": {
    #                 "BoundingBox": {"Width": ..., "Height": ..., "Left": ..., "Top": ...},
    #                 "Polygon": [
    #                     {"X": ..., "Y": ...},
    #                 ],
    #             },
    #             "Id": "string",
    #             "Relationships": [
    #                 {
    #                     "Type": "VALUE"
    #                     | "CHILD"
    #                     | "COMPLEX_FEATURES"
    #                     | "MERGED_CELL"
    #                     | "TITLE"
    #                     | "ANSWER"
    #                     | "TABLE"
    #                     | "TABLE_TITLE"
    #                     | "TABLE_FOOTER",
    #                     "Ids": [
    #                         "string",
    #                     ],
    #                 },
    #             ],
    #             "EntityTypes": [
    #                 "KEY"
    #                 | "VALUE"
    #                 | "COLUMN_HEADER"
    #                 | "TABLE_TITLE"
    #                 | "TABLE_FOOTER"
    #                 | "TABLE_SECTION_TITLE"
    #                 | "TABLE_SUMMARY"
    #                 | "STRUCTURED_TABLE"
    #                 | "SEMI_STRUCTURED_TABLE",
    #             ],
    #             "SelectionStatus": "SELECTED" | "NOT_SELECTED",
    #             "Page": 123,
    #             "Query": {
    #                 "Text": "string",
    #                 "Alias": "string",
    #                 "Pages": [
    #                     "string",
    #                 ],
    #             },
    #         },
    #     ],
    #     "HumanLoopActivationOutput": {
    #         "HumanLoopArn": "string",
    #         "HumanLoopActivationReasons": [
    #             "string",
    #         ],
    #         "HumanLoopActivationConditionsEvaluationResults": "string",
    #     },
    #     "AnalyzeDocumentModelVersion": "string",
    # }

    assert True
