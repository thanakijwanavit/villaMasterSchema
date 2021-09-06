#export

######## input #########
@dataclass_json
@dataclass
class Product(JsonSchemaMixin):
  cprcode: (int,str)
  productName: str
  quantity: int
  scheduleId: Optional[int] = None
  isPreOrder: bool = False
  usedForCoupon: Optional[CouponCode] = None
    
# shipping
class ShippingMode(Enum):
  nationwide = 'NATIONWIDE'
  regular = 'REGULAR'
  express = 'EXPRESS'
  pickup = 'PICKUP'

class ShippingType(Enum):
  delivery = 'DELIVERY'
  pickup = 'PICKUP'

class NationwideMode(Enum):
  fresh = 'FRESH'
  dry = 'DRY'
  mix = 'MIX'
@dataclass_json
@dataclass
class Schedule(JsonSchemaMixin):
  mode: ShippingMode = ShippingMode.nationwide
  dateTime: str = ''
  scheduleId: int = 0
  deliveryFee: Number = 0
  nationwideMode: Optional[NationwideMode] = None
@dataclass_json
@dataclass
class Shipping(JsonSchemaMixin):
  scheduleList: List[Schedule] = field(default_factory=list)
  shippingType: ShippingType = ShippingType.pickup
  shippingPostcode: str = '10110'
  shippingLat: Number = 0
  shippingLon: Number = 0
  shippingFirstName: str = ''
  shippingLastName: str = '' 
  shippingAddress:str = ''
  shippingSubDistrict:str = ''
  shippingProvince : str = ''
  shippingPostcode : str = ''
  shippingPhone : str = ''
  shippingEmail: str = ''
  shippingDate: Number = 0
# main input    
@dataclass_json
@dataclass
class GetCostInput(JsonSchemaMixin):
  branchId:str
  productList:List[Product]
  voucherId: List[int] = field(default_factory=list)
  ownerId:Optional[str] = None
  shipping:Optional[Shipping] = None
  couponCodeList:List['str'] = field(default_factory=list)
    
  def toDict(self):
    return json.loads(self.to_json())