from dataclasses_json import dataclass_json, Undefined, CatchAll
from dataclasses_jsonschema import JsonSchemaMixin
from dataclasses import dataclass


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class Product(JsonSchemaMixin):
  iprcode: int
  cprcode: int
#   data: CatchAll
@dataclass_json
@dataclass
class ValueUpdate(JsonSchemaMixin):
  items: List[Product]
