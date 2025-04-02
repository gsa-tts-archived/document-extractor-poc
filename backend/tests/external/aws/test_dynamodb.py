from decimal import Decimal

from src.external.aws.dynamodb import DynamoDb


def test_convert_decimal_direct_decimal():
    output = DynamoDb._convert_from_decimal(Decimal("1.2"))
    assert output == 1.2


def test_convert_decimal_list():
    test_input = [Decimal("1.2"), Decimal("2.3"), Decimal("3.4")]
    output = DynamoDb._convert_from_decimal(test_input)
    assert output == [1.2, 2.3, 3.4]


def test_convert_decimal_dict():
    test_input = {
        "a": Decimal("1.2"),
        "b": Decimal("2.3"),
        "c": Decimal("3.4"),
    }
    output = DynamoDb._convert_from_decimal(test_input)
    assert output == {
        "a": 1.2,
        "b": 2.3,
        "c": 3.4,
    }


def test_convert_decimal_complex():
    test_input = {
        "a": Decimal("1.2"),
        "b": [
            Decimal("2.3"),
            Decimal("3.4"),
            {
                "1": Decimal("3.4"),
                "2": Decimal("2.3"),
            },
        ],
        "c": {
            "1": Decimal("1.2"),
            "2": Decimal("2.3"),
            "3": [Decimal("3.4"), Decimal("2.3")],
        },
        "d": "Something else",
    }
    output = DynamoDb._convert_from_decimal(test_input)
    assert output == {
        "a": 1.2,
        "b": [
            2.3,
            3.4,
            {
                "1": 3.4,
                "2": 2.3,
            },
        ],
        "c": {
            "1": 1.2,
            "2": 2.3,
            "3": [
                3.4,
                2.3,
            ],
        },
        "d": "Something else",
    }
