"""Работа с категориями расходов"""
from typing import List
from dataclasses import dataclass
from db import db


@dataclass
class Category:
    """Структура категории"""
    id: int
    name: str
    icon: str
    client_telegram_id: int


class Categories:
    def __init__(self, telegram_id: int):
        self.telegram_id = telegram_id
        self._categories = self._load_categories()

    def _load_categories(self) -> List[Category]:
        """Возвращает справочник категорий расходов из БД"""
        categories = db.fetchall(
            'category', 'id name icon client_telegram_id'.split(), self.telegram_id
        )
        categories = [Category(id=category['id'],
                               name=category['name'],
                               icon=category['icon'],
                               client_telegram_id=category['client_telegram_id'])
                      for category in categories]
        return categories

    def get_all_categories(self) -> List[Category]:
        """Возвращает справочник категорий."""
        return self._categories

    def get_category(self, category_name: str) -> Category:
        """Возвращает категорию по одному из её алиасов."""
        found = None
        other_category = None
        for category in self._categories:
            if category.codename == "other":
                other_category = category
            for alias in category.aliases:
                if category_name in alias:
                    found = category
        if not found:
            found = other_category
        return found
