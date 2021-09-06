#export
######### output #########
@dataclass_json
@dataclass
class OutputProduct(JsonSchemaMixin):
  cprcode: (int,str)
  productName: str
  quantity: int
  originalPrice: Number
  price: Number
  settlementPrice: Number
  discountFromCoupon: Number = 0 # total discount for all products 
  scheduleId: Optional[int] = None
  isPreOrder: bool = False
#   rowTotal: Number
  @property
  def rowTotal(self)->Number:
    return self.price * self.quantity
  @rowTotal.setter
  def rowTotal(self, value):
    pass
  

# # discount
@dataclass_json
@dataclass
class Discount(JsonSchemaMixin):
  couponId: str
  couponName: str
  discount: Number
  eligibleProducts: List[int]
    
    
    
#main output
@dataclass_json
@dataclass
class GetCostOutput(JsonSchemaMixin):
  productList:List[OutputProduct]
  deliveryFee:Number
#   subTotal:Number
#   bogoDiscount: Number = 0
#   grandTotal:Number
  voucherId: List[int] = field(default_factory=list)
  ownerId:Optional[str] = None
  shipping: Optional[Shipping] = None
  cartDiscount:Number = 0
  cartDiscountInfo:List[Any] = field(default_factory = list)
  couponCodeList:List['str'] = field(default_factory=list)
  branchId:str = '1000'
    
    
  @property
  def totalExcludeControlledProducts(self)-> Number:
    sumControlledProducts = 0
    return self.grandTotal - sumControlledProducts
  
  @property
  def bogoDiscount(self) -> Number:
    return float(sum(product.discountFromCoupon for product in self.productList))
  
  @property
  def voucherDiscount(self)-> Number:
    return 0
  
  @property
  def subTotal(self) -> Number:
    return float(sum(product.rowTotal for product in self.productList))
  @subTotal.setter
  def subTotal(self, v:str)-> None:
    pass
  
  @property
  def grandTotal(self) -> Number:
    return self.subTotal + self.deliveryFee - self.cartDiscount - self.bogoDiscount
    
  def toDict(self):
    newDict:dict = json.loads(self.to_json())
    newDict['subTotal'] = self.subTotal
    newDict['grandTotal'] = self.grandTotal
    newDict['bogoDiscount'] = self.bogoDiscount
    newDict['totalExcludeControlledProducts'] = self.totalExcludeControlledProducts
    newDict['voucherDiscount'] = self.voucherDiscount
    return newDict