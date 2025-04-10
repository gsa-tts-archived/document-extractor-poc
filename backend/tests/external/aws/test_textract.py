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
                "BlockType": "WORD",
                "Confidence": 99.58535766601562,
                "Text": "Moof!",
                "TextType": "PRINTED",
                "Geometry": {
                    "BoundingBox": {
                        "Width": 0.07255866378545761,
                        "Height": 0.016273578628897667,
                        "Left": 0.24834169447422028,
                        "Top": 0.1792915314435959,
                    },
                    "Polygon": [
                        {"X": 0.24834217131137848, "Y": 0.17980238795280457},
                        {"X": 0.3208998739719391, "Y": 0.1792915314435959},
                        {"X": 0.3209003508090973, "Y": 0.1950606405735016},
                        {"X": 0.24834169447422028, "Y": 0.1955651193857193},
                    ],
                },
                "Id": "1111",
            },
            {
                "BlockType": "KEY_VALUE_SET",
                "Confidence": 96.22223663330078,
                "Geometry": {
                    "BoundingBox": {
                        "Width": 0.07295869290828705,
                        "Height": 0.016150739043951035,
                        "Left": 0.24823342263698578,
                        "Top": 0.17927560210227966,
                    },
                    "Polygon": [
                        {"X": 0.2482338845729828, "Y": 0.17978927493095398},
                        {"X": 0.3211916387081146, "Y": 0.17927560210227966},
                        {"X": 0.3211921155452728, "Y": 0.19491903483867645},
                        {"X": 0.24823342263698578, "Y": 0.195426344871521},
                    ],
                },
                "Id": "1112",
                "Relationships": [{"Type": "CHILD", "Ids": ["1111"]}],
                "EntityTypes": ["VALUE"],
            },
            {
                "BlockType": "LINE",
                "Confidence": 98.49639892578125,
                "Text": "What does DogCow Say?",
                "Geometry": {
                    "BoundingBox": {
                        "Width": 0.20893728733062744,
                        "Height": 0.021120533347129822,
                        "Left": 0.04019082710146904,
                        "Top": 0.15129978954792023,
                    },
                    "Polygon": [
                        {"X": 0.04019477963447571, "Y": 0.15280407667160034},
                        {"X": 0.24912811815738678, "Y": 0.15129978954792023},
                        {"X": 0.2491275519132614, "Y": 0.17093893885612488},
                        {"X": 0.04019082710146904, "Y": 0.17242032289505005},
                    ],
                },
                "Id": "2225",
                "Relationships": [
                    {
                        "Type": "CHILD",
                        "Ids": [
                            "2221",
                            "2222",
                            "2223",
                            "2224",
                        ],
                    }
                ],
            },
            {
                "BlockType": "KEY_VALUE_SET",
                "Confidence": 96.22223663330078,
                "Geometry": {
                    "BoundingBox": {
                        "Width": 0.2097739726305008,
                        "Height": 0.021547991782426834,
                        "Left": 0.039657481014728546,
                        "Top": 0.15101690590381622,
                    },
                    "Polygon": [
                        {"X": 0.039661526679992676, "Y": 0.1525275558233261},
                        {"X": 0.24943146109580994, "Y": 0.15101690590381622},
                        {"X": 0.24943087995052338, "Y": 0.17107774317264557},
                        {"X": 0.039657481014728546, "Y": 0.17256489396095276},
                    ],
                },
                "Id": "2226",
                "Relationships": [
                    {"Type": "VALUE", "Ids": ["1112"]},
                    {
                        "Type": "CHILD",
                        "Ids": [
                            "2221",
                            "2222",
                            "2223",
                            "2224",
                        ],
                    },
                ],
                "EntityTypes": ["KEY"],
            },
            {
                "BlockType": "WORD",
                "Confidence": 99.90831756591797,
                "Text": "What",
                "TextType": "PRINTED",
                "Geometry": {
                    "BoundingBox": {
                        "Width": 0.007296636234968901,
                        "Height": 0.013462036848068237,
                        "Left": 0.04019129276275635,
                        "Top": 0.15665747225284576,
                    },
                    "Polygon": [
                        {"X": 0.04019399359822273, "Y": 0.15670982003211975},
                        {"X": 0.047487929463386536, "Y": 0.15665747225284576},
                        {"X": 0.04748530685901642, "Y": 0.170067697763443},
                        {"X": 0.04019129276275635, "Y": 0.170119509100914},
                    ],
                },
                "Id": "2221",
            },
            {
                "BlockType": "WORD",
                "Confidence": 99.96954345703125,
                "Text": "does",
                "TextType": "PRINTED",
                "Geometry": {
                    "BoundingBox": {
                        "Width": 0.049453478306531906,
                        "Height": 0.017190800979733467,
                        "Left": 0.05397174879908562,
                        "Top": 0.15513181686401367,
                    },
                    "Polygon": [
                        {"X": 0.053974948823451996, "Y": 0.1554870754480362},
                        {"X": 0.10342522710561752, "Y": 0.15513181686401367},
                        {"X": 0.10342270880937576, "Y": 0.17197200655937195},
                        {"X": 0.05397174879908562, "Y": 0.172322615981102},
                    ],
                },
                "Id": "2222",
            },
            {
                "BlockType": "WORD",
                "Confidence": 92.77710723876953,
                "Text": "DogCow",
                "TextType": "PRINTED",
                "Geometry": {
                    "BoundingBox": {
                        "Width": 0.06911756098270416,
                        "Height": 0.015228607691824436,
                        "Left": 0.10593035072088242,
                        "Top": 0.15308326482772827,
                    },
                    "Polygon": [
                        {"X": 0.10593251883983612, "Y": 0.1535804122686386},
                        {"X": 0.17504791915416718, "Y": 0.15308326482772827},
                        {"X": 0.17504657804965973, "Y": 0.16782042384147644},
                        {"X": 0.10593035072088242, "Y": 0.16831187903881073},
                    ],
                },
                "Id": "2223",
            },
            {
                "BlockType": "WORD",
                "Confidence": 99.9212646484375,
                "Text": "say?",
                "TextType": "PRINTED",
                "Geometry": {
                    "BoundingBox": {
                        "Width": 0.04313291981816292,
                        "Height": 0.014579955488443375,
                        "Left": 0.17771314084529877,
                        "Top": 0.1521969437599182,
                    },
                    "Polygon": [
                        {"X": 0.17771439254283905, "Y": 0.15250732004642487},
                        {"X": 0.2208460569381714, "Y": 0.1521969437599182},
                        {"X": 0.2208453118801117, "Y": 0.16646996140480042},
                        {"X": 0.17771314084529877, "Y": 0.1667768955230713},
                    ],
                },
                "Id": "2224",
            },
        ],
        "AnalyzeDocumentModelVersion": "1",
    }

    textract = Textract()

    actual_parsed_response = textract._parse_textract_forms(mocked_textract_response)

    assert actual_parsed_response == {"What does DogCow say?": {"value": "Moof!", "confidence": 99.58535766601562}}
