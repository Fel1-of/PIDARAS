import os
from datetime import date
from contextlib import contextmanager

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData
from db.tables import Base
from db.tables import Client, Category, Expense, ClientSettings

PSQL_PASSWORD = os.environ['PASSWORDPSQL']
DATABASE_NAME = 'goodbottest'
engine = create_engine(f'postgresql+psycopg2://postgres:{PSQL_PASSWORD}@localhost/{DATABASE_NAME}', echo=False)
Session = sessionmaker(bind=engine)
current_session = Session()


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def _init_db_():
    meta = MetaData()
    meta.reflect(bind=engine)
    meta.drop_all(bind=engine)

    Base.metadata.create_all(engine)

    me = Client(telegram_id=285942176, is_pro_account=False)
    with session_scope() as session:
        session.add(me)
        session.add_all([
            Category(name='продукты', icon='🍴', client_telegram_id=285942176),
            Category(name='кофе', icon='☕', client_telegram_id=285942176),
            Category(name='пиво', icon='🍻', client_telegram_id=285942176),
            Category(name='общественный транспорт', icon='🚌', client_telegram_id=285942176),
            Category(name='такси', icon='🚕', client_telegram_id=285942176)
        ])


# _init_db_()


async def add_expense(telegram_user_id: int, amount: float, category_name: str, created_date: date,
                      label: str = None, place: str = None, description: str = None):
    with session_scope() as session:
        categories = session.query(Category).filter(Category.client_telegram_id == telegram_user_id)
        category = categories.filter(Category.name == category_name).first()
        expense = Expense(client_telegram_id=telegram_user_id, amount=amount, category_id=category.id,
                          label=label, date=created_date, place=place, description=description)
        session.add(expense)


async def get_client_settings(telegram_user_id: id) -> ClientSettings:
    client_settings = current_session.query(ClientSettings).filter(ClientSettings.telegram_id == telegram_user_id)
    return client_settings.first()
    # with session_scope() as session:
    #     client_settings = session.query(ClientSettings).filter(ClientSettings.telegram_id == telegram_user_id).first()
    #     return client_settings

# meta = MetaData()

# meta.reflect(bind=engine)
# meta.drop_all(bind=engine)

# for table in reversed(meta.sorted_tables):
#     print(table)
#     engine.execute(table.drop(engine))
