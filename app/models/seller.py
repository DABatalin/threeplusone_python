from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Seller(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String)
    rating = Column(Float, default=0.0)
    
    products = relationship("Product", back_populates="seller") 