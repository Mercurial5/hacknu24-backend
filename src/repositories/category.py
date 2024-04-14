from db import PostgresDB
from dto import CategoryDTO
from models import Category


class CategoryRepository:

    def __init__(self, db: PostgresDB):
        self._db = db

    def get_categories(self) -> list[CategoryDTO]:
        with self._db.session_scope() as session:
            categories = session.query(Category.id, Category.name).all()

        return [CategoryDTO(*category) for category in categories]
