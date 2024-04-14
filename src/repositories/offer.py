from sqlalchemy import or_

from db import PostgresDB
from dto import OfferDTO
from models import Offer, Bank, Category, Shop


class OfferRepository:
    def __init__(self, db: PostgresDB):
        self._db = db

    def get_offers(self, word: str) -> list[OfferDTO]:
        with self._db.session_scope() as session:
            query = session.query(Offer.id, Category.name, Shop.name, Bank.name, Offer.bonus, Offer.updated_at)
            query = query.join(Bank, Offer.bank_id == Bank.id)
            query = query.join(Category, Offer.category_id == Category.id)
            query = query.join(Shop, Offer.shop_id == Shop.id)

            condition = or_(
                Shop.name.ilike(f'{word}%'),
                Category.name.ilike(f'{word}%')
            )
            offers = query.filter(condition).all()

            condition = or_(
                Shop.name.ilike(f'%{word}%'),
                Category.name.ilike(f'%{word}%')
            )
            offers.extend(query.filter(condition).all())

            condition = or_(
                Shop.name.ilike(f'%{word}'),
                Category.name.ilike(f'%{word}')
            )
            offers.extend(query.filter(condition).all())

        # https://stackoverflow.com/questions/480214/how-do-i-remove-duplicates-from-a-list-while-preserving-order
        storage = set()
        add_storage = storage.add
        offers = [OfferDTO(*offer[1:]) for offer in offers if not (offer[0] in storage or add_storage(offer[0]))]

        return offers

    def get_offers_by_shop_id(self, shop_id: int) -> list[OfferDTO]:
        with self._db.session_scope() as session:
            query = session.query(Offer.id, Category.name, Shop.name, Bank.name, Offer.bonus, Offer.updated_at)
            query = query.join(Bank, Offer.bank_id == Bank.id)
            query = query.join(Category, Offer.category_id == Category.id)
            query = query.join(Shop, Offer.shop_id == Shop.id)
            query = query.filter(Offer.shop_id == shop_id)

            offers = query.all()

        return [OfferDTO(*offer[1:]) for offer in offers]
