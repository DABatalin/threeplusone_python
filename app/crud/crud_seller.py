from app.crud.base import CRUDBase
from app.models.seller import Seller
from app.schemas.seller import SellerCreate, SellerUpdate


class CRUDSeller(CRUDBase[Seller, SellerCreate, SellerUpdate]):
    pass


seller = CRUDSeller(Seller) 