from sqlalchemy import event
from sqlalchemy.orm import Session

from app.models.product import Product
from app.models.seller import Seller
from app.models.comment import Comment
from app.services.elasticsearch import (
    index_product,
    index_seller,
    index_comment,
    delete_product,
    delete_seller,
    delete_comment
)

def setup_elasticsearch_sync(session: Session):
    """Setup SQLAlchemy event listeners for Elasticsearch synchronization"""
    
    # Product events
    @event.listens_for(Product, 'after_insert')
    @event.listens_for(Product, 'after_update')
    def index_product_listener(mapper, connection, target):
        index_product({
            'id': target.id,
            'name': target.name,
            'description': target.description,
            'price': str(target.price),
            'category': target.category,
            'stock': target.stock,
            'image_url': target.image_url,
            'seller_id': target.seller_id
        })

    @event.listens_for(Product, 'after_delete')
    def delete_product_listener(mapper, connection, target):
        delete_product(target.id)

    # Seller events
    @event.listens_for(Seller, 'after_insert')
    @event.listens_for(Seller, 'after_update')
    def index_seller_listener(mapper, connection, target):
        index_seller({
            'id': target.id,
            'name': target.name,
            'description': target.description,
            'rating': target.rating
        })

    @event.listens_for(Seller, 'after_delete')
    def delete_seller_listener(mapper, connection, target):
        delete_seller(target.id)

    # Comment events
    @event.listens_for(Comment, 'after_insert')
    @event.listens_for(Comment, 'after_update')
    def index_comment_listener(mapper, connection, target):
        index_comment({
            'id': target.id,
            'text': target.text,
            'rating': target.rating,
            'user_id': target.user_id,
            'product_id': target.product_id,
            'created_at': target.created_at
        })

    @event.listens_for(Comment, 'after_delete')
    def delete_comment_listener(mapper, connection, target):
        delete_comment(target.id)

def sync_existing_data(session: Session):
    """Synchronize existing database data with Elasticsearch"""
    # Sync products
    products = session.query(Product).all()
    for product in products:
        index_product({
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': str(product.price),
            'category': product.category,
            'stock': product.stock,
            'image_url': product.image_url,
            'seller_id': product.seller_id
        })

    # Sync sellers
    sellers = session.query(Seller).all()
    for seller in sellers:
        index_seller({
            'id': seller.id,
            'name': seller.name,
            'description': seller.description,
            'rating': seller.rating
        })

    # Sync comments
    comments = session.query(Comment).all()
    for comment in comments:
        index_comment({
            'id': comment.id,
            'text': comment.text,
            'rating': comment.rating,
            'user_id': comment.user_id,
            'product_id': comment.product_id,
            'created_at': comment.created_at
        }) 