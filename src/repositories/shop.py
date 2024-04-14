from db import PostgresDB
from dto.shop import ShopDTO
from models import Shop, Offer


class ShopRepository:
    def __init__(self, db: PostgresDB):
        self._db = db

    def get_shops(self, category_id: int) -> list[ShopDTO]:
        with self._db.session_scope() as session:
            query = session.query(Shop.id, Shop.name).distinct(Shop.id)
            query = query.join(Offer, Offer.shop_id == Shop.id)
            query = query.filter_by(category_id=category_id)

            shops = query.all()

        return [ShopDTO(*shop) for shop in shops]
