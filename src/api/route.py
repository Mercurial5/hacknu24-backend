from sanic import Request
from sanic.response import JSONResponse

from repositories import OfferRepository, CategoryRepository, ShopRepository


def search(offer_repository: OfferRepository, request: Request) -> JSONResponse:
    query = request.args.get('query')
    if not query:
        return JSONResponse(dict(detail='Empty query'), 400)

    offers = offer_repository.get_offers(query)
    offers = [offer.dict() for offer in offers]
    return JSONResponse(offers, 200)


def categories_route(category_repository: CategoryRepository, _: Request) -> JSONResponse:
    categories = category_repository.get_categories()
    categories = [category.dict() for category in categories]

    return JSONResponse(categories, 200)


def shops_route(shop_repository: ShopRepository, _: Request, category_id: int) -> JSONResponse:
    shops = shop_repository.get_shops(category_id)
    shops = [shop.dict() for shop in shops]

    return JSONResponse(shops, 200)


def offers_route(offers_repository: OfferRepository, _: Request, shop_id: int) -> JSONResponse:
    offers = offers_repository.get_offers_by_shop_id(shop_id)
    offers = [offer.dict() for offer in offers]

    return JSONResponse(offers, 200)