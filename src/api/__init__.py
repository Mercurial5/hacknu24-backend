import functools

from sanic import Sanic
from sanic_cors import CORS

from api.cors import add_cors_headers
from api.options import setup_options
from api.route import search, categories_route, shops_route, offers_route
from db import PostgresConfigs, PostgresDB
from repositories import OfferRepository, ShopRepository
from repositories.category import CategoryRepository


def create_app() -> Sanic:
    app = Sanic(__name__)
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)
    # app.register_listener(setup_options, "before_server_start")
    app.register_middleware(add_cors_headers, "response")

    postgres_configs = PostgresConfigs.from_environ()
    db = PostgresDB(postgres_configs)
    offer_repository = OfferRepository(db)

    twisted_search = functools.partial(search, offer_repository)
    twisted_search.__name__ = 'search'
    app.add_route(twisted_search, uri='/search', methods=['GET'])

    category_repository = CategoryRepository(db)
    twisted_categories = functools.partial(categories_route, category_repository)
    twisted_categories.__name__ = 'categories'
    app.add_route(twisted_categories, uri='/categories', methods=['GET'])

    shop_repository = ShopRepository(db)
    twisted_shops = functools.partial(shops_route, shop_repository)
    twisted_shops.__name__ = 'shops'
    app.add_route(twisted_shops, uri='/categories/<category_id>', methods=['GET'])

    twisted_offers = functools.partial(offers_route, offer_repository)
    twisted_offers.__name__ = 'offers'
    app.add_route(twisted_offers, uri='/offers/<shop_id>', methods=['GET'])

    return app
