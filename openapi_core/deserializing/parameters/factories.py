from openapi_core.deserializing.parameters.deserializers import (
    PrimitiveDeserializer,
)
from openapi_core.schema.parameters import get_style


class ParameterDeserializersFactory(object):

    PARAMETER_STYLE_DESERIALIZERS = {
        'form': lambda x: x.split(','),
        'simple': lambda x: x.split(','),
        'spaceDelimited': lambda x: x.split(' '),
        'pipeDelimited': lambda x: x.split('|'),
    }

    def create(self, param):
        style = get_style(param)

        deserialize_callable = self.PARAMETER_STYLE_DESERIALIZERS[style]
        return PrimitiveDeserializer(param, deserialize_callable)
