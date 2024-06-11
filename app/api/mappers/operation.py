from typing import Any

from pydantic import create_model, ValidationError
from typer.models import NoneType

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

    def get_class_attributes(self, attributes: dict | None) -> dict:
        typed_attributes = {}
        for attribute, value in attributes.items():
            attrib_type = type(value)
            required_attrib = None if isinstance(value, NoneType) else ...
            typed_attributes[attribute] = (attrib_type, required_attrib)

        return typed_attributes

    def build_object(self, data_template: DataTemplate) -> object:
        class_name = data_template.object_value.class_name
        attributes_values = data_template.object_value.attributes

        typed_attributes = {}
        for attribute, value in attributes_values.items():
            if isinstance(value, dict):
                try:
                    inner_data_template = DataTemplate.model_validate(value)
                    inner_object = self.build_object(data_template=inner_data_template)
                    required_attrib = None if isinstance(value, NoneType) else ...
                    typed_attributes[attribute] = (type(inner_object), required_attrib)
                    attributes_values[attribute] = inner_object
                except ValidationError as err:
                    attrib_type = type(value)
                    required_attrib = None if isinstance(value, NoneType) else ...
                    typed_attributes[attribute] = (attrib_type, required_attrib)
            else:
                attrib_type = type(value)
                required_attrib = None if isinstance(value, NoneType) else ...
                typed_attributes[attribute] = (attrib_type, required_attrib)

        dynamic_class = create_model(class_name, **typed_attributes)
        return dynamic_class(**attributes_values)

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

# def build_objects(response: DataTemplate) -> object:
#     data_type = response.data_type
#     new_obj = instantiate_data(data_type=data_type, response=response)
#     return new_obj


# def instantiate_data(data_type: DataType, response: DataTemplate):
#     create_type_function = CAST_FUNCTIONS_BY_TYPE.get(data_type)
#     new_instance = create_type_function(response=response)
#     return new_instance


# def _create_class_type(response: DataTemplate) -> object:
#     class_name = response.object_value.class_name
#     attributes_values = response.object_value.attributes
#     class_attributes = _get_attributes(attributes=attributes_values)
#
#     # TODO: Refatorar para que o template da Classe não precise ser recriado toda vez,
#     #  podemos reutilizar o mesmo template criado anteriormente
#     dynamic_class = create_model(class_name, **class_attributes)
#     return dynamic_class(**attributes_values)


# def _get_base_classes(base_classes: str | None) -> Tuple:
#     base_classes_set = ()
#     if base_classes:
#         base_classes_set = tuple(tp.strip() for tp in base_classes.split(","))
#
#     return base_classes_set + (BaseModel,)
#
#
# def _get_attributes(attributes: dict | None) -> dict:
#     typed_attributes = {}
#     for attribute, value in attributes.items():
#         attrib_type = type(value)
#         required_attrib = None if type(value) is type(None) else ...
#         typed_attributes[attribute] = (attrib_type, required_attrib)
#
#     return typed_attributes

# def _create_class_type(data_template: DataTemplate) -> object:
#     class_name = data_template.object_value.class_name
#     attributes_values = data_template.object_value.attributes
#     class_attributes = _get_attributes(attributes=attributes_values)
#
#     # TODO: Refatorar para que o template da Classe não precise ser recriado toda vez,
#     #  podemos reutilizar o mesmo template criado anteriormente
#     dynamic_class = create_model(class_name, **class_attributes)
#     return dynamic_class(**attributes_values)
#
#
# def _create_str_type(response: DataTemplate | str) -> object:
#     if isinstance(response, DataTemplate):
#         return str(response.simple_value.value)
#
#     return str(response)
#
#
# def _create_list_type(response: DataTemplate):
#     objects = []
#     values = response.list_value.values
#     list_type = response.list_value.data_type
#
#     for value in values:
#         value_type = value.data_type if list_type == DataType.CLASS else list_type
#         objects.append(instantiate_data(data_type=value_type, response=value))
#
#     return objects
#
#
# CAST_FUNCTIONS_BY_TYPE = {
#     DataType.CLASS: _create_class_type,
#     DataType.STR: _create_str_type,
#     DataType.LIST: _create_list_type,
# }
