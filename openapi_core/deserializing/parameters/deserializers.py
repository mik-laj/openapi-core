import warnings

from openapi_core.deserializing.exceptions import DeserializeError
from openapi_core.deserializing.parameters.exceptions import (
    EmptyParameterValue,
)
from openapi_core.schema.parameters import get_aslist, get_explode, get_style


class PrimitiveDeserializer(object):

    def __init__(self, param_or_header, deserializer_callable):
        self.param_or_header = param_or_header
        self.deserializer_callable = deserializer_callable

        self.aslist = get_aslist(self.param_or_header)
        self.explode = get_explode(self.param_or_header)
        self.style = get_style(self.param_or_header)

    def __call__(self, value):
        # if "in" not defined then it's a Header
        if 'allowEmptyValue' in self.param_or_header:
            warnings.warn(
                "Use of allowEmptyValue property is deprecated",
                DeprecationWarning,
            )
        allow_empty_values = self.param_or_header.getkey(
            'allowEmptyValue', False)
        location_name = self.param_or_header.getkey('in', 'header')
        if (location_name == 'query' and value == "" and
                not allow_empty_values):
            name = self.param_or_header.getkey('name', 'header')
            raise EmptyParameterValue(value, self.style, name)

        if not self.aslist or self.explode:
            return value
        try:
            return self.deserializer_callable(value)
        except (ValueError, TypeError, AttributeError):
            raise DeserializeError(value, self.style)
