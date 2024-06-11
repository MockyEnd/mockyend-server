from typing import Any, List

import pytest

from app.api.mappers.operation import DataLoader
from app.api.schemas.operation import DataTemplate, DataType


@pytest.fixture
def raw_list_data_template_with_class_type():
    return {
        "data_type": "LIST",
        "list_value": {
            "data_type": "CLASS",
            "values": [
                {
                    "object_value": {
                        "class_name": "Person",
                        "attributes": {
                            "name": "Raphael",
                            "age": 35
                        }
                    }
                },
                {
                    "object_value": {
                        "class_name": "Person",
                        "attributes": {
                            "name": "Marianne",
                            "age": 30
                        }
                    }
                }
            ]
        }
    }


@pytest.fixture
def data_template_with_list_of_class_type(raw_list_data_template_with_class_type) -> DataTemplate:
    return DataTemplate.model_validate(raw_list_data_template_with_class_type)


def test_data_loader(data_template_with_list_of_class_type):
    # Given
    data_loader = DataLoader()

    # When
    result = data_loader.compile(data_template=data_template_with_list_of_class_type)

    # Then
    assert result is not None
    assert isinstance(result, list)
    first = result[0]
    assert str(type(first)) == "<class 'app.api.mappers.operation.Person'>"
    assert first.name == 'Raphael'
    assert first.age == 35


def create_data_template_with_list_of_primitive_type(data_type: DataType, values: List) -> DataTemplate:
    raw_data = {
        "data_type": "LIST",
        "list_value": {
            "data_type": data_type.value,
            "values": values
        }
    }
    return DataTemplate.model_validate(raw_data)


@pytest.mark.parametrize(
    "data_type, values",
    [
        (DataType.STR, ["Python", "Java", "Rust", "Crystal", "Javascript"]),
        (DataType.INT, [i for i in range(100)]),
    ]
)
def test_data_loader_with_list_of_primitive_values(data_type: DataType, values: List):
    # Given
    data_template = create_data_template_with_list_of_primitive_type(data_type=data_type, values=values)

    # When
    data_loader = DataLoader()
    result = data_loader.compile(data_template=data_template)

    # Then
    assert len(values) == len(result)
    assert result == values


def create_data_template_with_primitive_value(data_type: DataType, value: Any) -> DataTemplate:
    raw_data = {
        "data_type": data_type.value if data_type else None,
        "primitive_value": {
            "value": value
        }
    }
    return DataTemplate.model_validate(raw_data)


@pytest.mark.parametrize(
    "data_type, value",
    [
        (DataType.STR, "OK"),
        (None, "OK"),
        (DataType.INT, 100),
        (DataType.BOOL, True),
        (DataType.BOOL, False),
        (DataType.DICT, {
            "status": 200,
            "message": "OK",
            "detail": {
                "inner_dict": "OK"
            },
        })
    ]
)
def test_data_loader_with_primitive_value(data_type: DataType, value: Any):
    # Given
    data_template = create_data_template_with_primitive_value(data_type=data_type, value=value)

    # When
    data_loader = DataLoader()
    result = data_loader.compile(data_template=data_template)

    # Then
    assert result == value


def test_data_loader_with_object_value():
    # Given
    shipping_attributes = {
        "data_type": DataType.CLASS,
        "object_value": {
            "class_name": "Shipping",
            "attributes": {
                "package_id": "P_123",
                "sender": {
                    "data_type": DataType.CLASS,
                    "object_value": {
                        "class_name": "Customer",
                        "attributes": {
                            "name": "Sender",
                            "document": "123.456.789-01"
                        }
                    }
                },
                "recipient": {
                    "data_type": DataType.CLASS,
                    "object_value": {
                        "class_name": "Customer",
                        "attributes": {
                            "name": "Recipient",
                            "document": "987.654.321-01"
                        }
                    }
                },
            }
        }
    }
    data_template = DataTemplate.model_validate(shipping_attributes)

    # When
    data_loader = DataLoader()
    shipping = data_loader.compile(data_template=data_template)

    # Then
    assert shipping is not None
    assert str(type(shipping)) == "<class 'app.api.mappers.operation.Shipping'>"
    assert shipping.package_id == "P_123"

    assert str(type(shipping.sender)) == "<class 'app.api.mappers.operation.Customer'>"
    assert shipping.sender.name == "Sender"
    assert shipping.sender.document == "123.456.789-01"

    assert str(type(shipping.recipient)) == "<class 'app.api.mappers.operation.Customer'>"
    assert shipping.recipient.name == "Recipient"
    assert shipping.recipient.document == "987.654.321-01"
