from typing import Dict
import pytest

from app.api.schemas.operation import CreateEndpointRequest


@pytest.fixture
def raw_operation_register_request() -> Dict:
    return {
        "name": "Pessoas",
        "summary": "Lista de pessoas",
        "description": "Lista com pessoas",
        "method": "GET",
        "path": "/pessoas",
        "response": {
            "data_type": "LIST",
            "list_value": {
                "data_type": "CLASS",
                "values": [
                    {
                        "data_type": "CLASS",
                        "object_value": {
                            "class_name": "Person",
                            "attributes": {
                                "name": "Rafael",
                                "age": 35
                            }
                        }
                    },
                    {
                        "data_type": "CLASS",
                        "object_value": {
                            "class_name": "Person",
                            "attributes": {
                                "name": "Mariane",
                                "age": 30
                            }
                        }
                    }
                ]
            }
        }
    }


@pytest.fixture()
def create_endpoint_request(raw_operation_register_request) -> CreateEndpointRequest:
    return CreateEndpointRequest(**raw_operation_register_request)

