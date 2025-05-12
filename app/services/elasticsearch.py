from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
from elasticsearch_dsl import Search, Index, Document, Text, Keyword, Float, Integer, Date
from typing import List, Optional, Any, Dict

from app.core.config import settings

# Initialize Elasticsearch client
es_client = Elasticsearch(
    [{'host': settings.ELASTICSEARCH_HOST, 'port': settings.ELASTICSEARCH_PORT}],
    http_auth=(settings.ELASTICSEARCH_USERNAME, settings.ELASTICSEARCH_PASSWORD) if settings.ELASTICSEARCH_USERNAME else None
)

class ProductDocument(Document):
    name = Text(fields={'keyword': Keyword()})
    description = Text()
    price = Float()
    category = Keyword()
    stock = Integer()
    image_url = Keyword()
    seller_id = Integer()

    class Index:
        name = 'products'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

class SellerDocument(Document):
    name = Text(fields={'keyword': Keyword()})
    description = Text()
    rating = Float()

    class Index:
        name = 'sellers'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

class CommentDocument(Document):
    text = Text()
    rating = Integer()
    user_id = Integer()
    product_id = Integer()
    created_at = Date()

    class Index:
        name = 'comments'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

def setup_elasticsearch():
    """Create indices if they don't exist"""
    ProductDocument.init()
    SellerDocument.init()
    CommentDocument.init()

def index_product(product: Dict[str, Any]):
    """Index a product in Elasticsearch"""
    doc = ProductDocument(
        meta={'id': product['id']},
        name=product['name'],
        description=product['description'],
        price=float(product['price']),
        category=product['category'],
        stock=product['stock'],
        image_url=product['image_url'],
        seller_id=product['seller_id']
    )
    doc.save()

def index_seller(seller: Dict[str, Any]):
    """Index a seller in Elasticsearch"""
    doc = SellerDocument(
        meta={'id': seller['id']},
        name=seller['name'],
        description=seller['description'],
        rating=seller['rating']
    )
    doc.save()

def index_comment(comment: Dict[str, Any]):
    """Index a comment in Elasticsearch"""
    doc = CommentDocument(
        meta={'id': comment['id']},
        text=comment['text'],
        rating=comment['rating'],
        user_id=comment['user_id'],
        product_id=comment['product_id'],
        created_at=comment['created_at']
    )
    doc.save()

def search_products(query: str, category: Optional[str] = None) -> List[Dict[str, Any]]:
    """Search products by name, description or category"""
    s = Search(using=es_client, index='products')
    if category:
        s = s.filter('term', category=category)
    s = s.query('multi_match', query=query, fields=['name^3', 'description'])
    response = s.execute()
    return [hit.to_dict() for hit in response]

def search_sellers(query: str) -> List[Dict[str, Any]]:
    """Search sellers by name or description"""
    s = Search(using=es_client, index='sellers')
    s = s.query('multi_match', query=query, fields=['name^3', 'description'])
    response = s.execute()
    return [hit.to_dict() for hit in response]

def search_comments(product_id: int) -> List[Dict[str, Any]]:
    """Search comments for a specific product"""
    s = Search(using=es_client, index='comments')
    s = s.filter('term', product_id=product_id)
    s = s.sort('-created_at')
    response = s.execute()
    return [hit.to_dict() for hit in response]

def delete_product(product_id: int):
    """Delete a product from Elasticsearch"""
    try:
        ProductDocument.get(id=product_id).delete()
    except NotFoundError:
        pass

def delete_seller(seller_id: int):
    """Delete a seller from Elasticsearch"""
    try:
        SellerDocument.get(id=seller_id).delete()
    except NotFoundError:
        pass

def delete_comment(comment_id: int):
    """Delete a comment from Elasticsearch"""
    try:
        CommentDocument.get(id=comment_id).delete()
    except NotFoundError:
        pass 