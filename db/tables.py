from sqlalchemy import Column, ForeignKey, Integer, String, Float, Text, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Client(Base):
    __tablename__ = 'clients'

    telegram_id = Column(Integer, primary_key=True)
    is_pro_account = Column(Boolean, nullable=False, default=False)
    expenses = relationship('Expense')
    categories = relationship('Category')
    settings = relationship('ClientSettings', back_populates='client', uselist=False)

    def __repr__(self):
        return f'Client(telegram_id={self.telegram_id} is_pro_account={self.is_pro_account})'


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    client_telegram_id = Column(Integer, ForeignKey(Client.telegram_id))
    name = Column(String(128), nullable=False, unique=True)
    icon = Column(String(32), nullable=False)
    expenses = relationship('Expense')

    def __repr__(self):
        return f'Expense(name={self.name})'


class Expense(Base):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True)
    client_telegram_id = Column(Integer, ForeignKey(Client.telegram_id))
    amount = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey(Category.id))
    label = Column(String(64))
    date = Column(Date)
    place = Column(Text)
    description = Column(Text)

    def __repr__(self):
        return f'Expense(amount={self.amount})'


class ClientSettings(Base):
    __tablename__ = 'clientsSettings'

    telegram_id = Column(Integer, ForeignKey(Client.telegram_id), primary_key=True)
    client = relationship('Client', back_populates='settings')
    asking_label = Column(Boolean, nullable=False, default=True)
    asking_place = Column(Boolean, nullable=False, default=True)
    asking_description = Column(Boolean, nullable=False, default=True)

    def __repr__(self):
        return f'ClientSettings(asking_label={self.asking_label} ' \
               f'asking_place={self.asking_place} asking_description={self.asking_description})'
