import asyncio
from typing import Optional
from elasticsearch import AsyncElasticsearch
from elastic_transport import ConnectionError
from app.core.config import settings

class ElasticsearchService:
    def __init__(self):
        self.es: Optional[AsyncElasticsearch] = None
        self.product_index = 'products'
        self.comment_index = 'comments'

    async def connect(self, retries: int = 5, delay: int = 5) -> None:
        """Connect to Elasticsearch with retries"""
        for attempt in range(retries):
            try:
                self.es = AsyncElasticsearch([f'http://{settings.ELASTICSEARCH_HOST}:{settings.ELASTICSEARCH_PORT}'])
                # Test the connection
                await self.es.info()
                print(f"Successfully connected to Elasticsearch on attempt {attempt + 1}")
                break
            except ConnectionError as e:
                if attempt == retries - 1:  # Last attempt
                    print(f"Could not connect to Elasticsearch after {retries} attempts")
                    raise e
                print(f"Connection attempt {attempt + 1} failed, retrying in {delay} seconds...")
                await asyncio.sleep(delay)

    async def init_indices(self):
        """Initialize Elasticsearch indices"""
        if not self.es:
            await self.connect()

        if not await self.es.indices.exists(index=self.product_index):
            await self.es.indices.create(
                index=self.product_index,
                body={
                    'mappings': {
                        'properties': {
                            'id': {'type': 'integer'},
                            'name': {'type': 'text'},
                            'description': {'type': 'text'},
                            'category': {'type': 'keyword'},
                            'seller_id': {'type': 'integer'},
                            'comments': {
                                'type': 'nested',
                                'properties': {
                                    'id': {'type': 'integer'},
                                    'text': {'type': 'text'},
                                    'rating': {'type': 'integer'},
                                    'user_id': {'type': 'integer'}
                                }
                            }
                        }
                    }
                }
            )

    async def index_product(self, product_data: dict):
        if not self.es:
            await self.connect()
        await self.es.index(
            index=self.product_index,
            id=product_data['id'],
            body=product_data
        )

    async def update_product(self, product_id: int, product_data: dict):
        if not self.es:
            await self.connect()
        await self.es.update(
            index=self.product_index,
            id=product_id,
            body={'doc': product_data}
        )

    async def delete_product(self, product_id: int):
        if not self.es:
            await self.connect()
        await self.es.delete(
            index=self.product_index,
            id=product_id
        )

    async def search_products(self, query: str, category: str = None):
        if not self.es:
            await self.connect()
        search_query = {
            'query': {
                'bool': {
                    'must': [
                        {
                            'multi_match': {
                                'query': query,
                                'fields': ['name^3', 'description', 'comments.text']
                            }
                        }
                    ]
                }
            }
        }

        if category:
            search_query['query']['bool']['filter'] = [{'term': {'category': category}}]

        result = await self.es.search(
            index=self.product_index,
            body=search_query
        )
        return result['hits']['hits']

    async def close(self):
        if self.es:
            await self.es.close()

elasticsearch_service = ElasticsearchService() 