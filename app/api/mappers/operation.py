from typing import Any

from pydantic import create_model, ValidationError
from typer.models import NoneType

from app.api.mappers.exceptions import ClassNameNotProvidedError
from app.api.schemas.operation import CreateEndpointRequest, DataType, DataTemplate
from app.domain.models.operation import Operation, Method


class DataLoader:

    def __init__(self):
        self.CAST_FUNCTIONS_BY_TYPE = {
            DataType.CLASS: self._create_class_type,
            DataType.STR: self._create_str_type,
            DataType.INT: self._create_int_type,
            DataType.BOOL: self._create_bool_type,
            DataType.DICT: self._create_dict_type,
            DataType.LIST: self._create_list_type,
        }

    def compile(self, data_template: DataTemplate) -> object:
        return self.build_objects(data_template=data_template)

    def build_objects(self, data_template: DataTemplate) -> object:
        data_type = data_template.data_type
        new_obj = self.instantiate_data(data_type=data_type, data_template=data_template)
        return new_obj

    def instantiate_data(self, data_type: DataType, data_template: DataTemplate | Any):
        if data_type == DataType.CLASS and not isinstance(data_template, DataTemplate):
            data_template = DataTemplate.model_validate(data_template)

        create_type_function = self.CAST_FUNCTIONS_BY_TYPE.get(data_type, self._create_str_type)
        new_instance = create_type_function(data_template)
        return new_instance

    def _create_class_type(self, data_template: DataTemplate) -> object:
        return self.build_object(data_template=data_template)

    def build_object(self, data_template: DataTemplate) -> object:
        class_name = data_template.object_value.class_name
        attributes_values = data_template.object_value.attributes

        typed_attributes = {}
        for attribute, value in attributes_values.items():
            if isinstance(value, dict):
                try:
                    inner_data_template = DataTemplate.model_validate(value)
                    inner_object = self.build_object(data_template=inner_data_template)
                    required_attrib = self.is_required_field(value=value)
                    typed_attributes[attribute] = (type(inner_object), required_attrib)
                    attributes_values[attribute] = inner_object
                except ClassNameNotProvidedError as err:
                    attrib_type = type(value)
                    required_attrib = self.is_required_field(value=value)
                    typed_attributes[attribute] = (attrib_type, required_attrib)
            else:
                attrib_type = type(value)
                required_attrib = self.is_required_field(value=value)
                typed_attributes[attribute] = (attrib_type, required_attrib)

        if class_name is None:
            raise ClassNameNotProvidedError("Class name attribute not provided for a dict object")

        dynamic_class = create_model(class_name, **typed_attributes)
        return dynamic_class(**attributes_values)

    @staticmethod
    def is_required_field(value):
        return None if isinstance(value, NoneType) else ...

    def _create_str_type(self, data_template: DataTemplate | Any) -> object:
        return self._to_value(create_type_function=str, data_template=data_template)

    def _create_int_type(self, data_template: DataTemplate | Any) -> object:
        return self._to_value(create_type_function=int, data_template=data_template)

    def _create_bool_type(self, data_template: DataTemplate | Any) -> object:
        return self._to_value(create_type_function=bool, data_template=data_template)

    def _create_dict_type(self, data_template: DataTemplate | Any) -> object:
        return self._to_value(create_type_function=dict, data_template=data_template)

    def _to_value(self, create_type_function, data_template: DataTemplate | Any) -> object:
        if isinstance(data_template, DataTemplate):
            return create_type_function(data_template.primitive_value.value)

        return create_type_function(data_template)

    def _create_list_type(self, data_template: DataTemplate):
        objects = []
        values = data_template.list_value.values
        list_type = data_template.list_value.data_type

        for value in values:
            objects.append(self.instantiate_data(data_type=list_type, data_template=value))

        return objects


class OperationMapper:
    @staticmethod
    def mapping(request: CreateEndpointRequest) -> Operation:
        data_loader = DataLoader()

        return Operation(
            name=request.name,
            summary=request.summary,
            description=request.description,
            method=Method(request.method),
            path=request.path,
            response=data_loader.compile(data_template=request.response)
        )
