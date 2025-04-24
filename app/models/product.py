from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Product(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    category = Column(String, index=True)
    stock = Column(Integer, default=0)
    image_url = Column(String)  # S3 URL
    seller_id = Column(Integer, ForeignKey("seller.id"), nullable=False)
    
    # Relationships
    seller = relationship("Seller", back_populates="products")
    cart_items = relationship("CartItem", back_populates="product")
    purchase_items = relationship("PurchaseItem", back_populates="product")
    comments = relationship("Comment", back_populates="product") 