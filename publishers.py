import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import create_tables, Publisher, Book, Shop, Stock, Sale

driver = "postgresql"  # input()
host = "localhost"  # input()
login = "postgres"  # input()
password = "456egor4ik456"  # input()
port = "5432"  # input()
db = "Publishers"  # input()

DSN = f"{driver}://{login}:{password}@{host}:{port}/{db}"
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

# with open('C:/Users/Admin/PycharmProjects/pythonProject1/tests_data.json', 'r') as fd:
#     data = json.load(fd)
#
# for record in data:
#     model = {
#         'publisher': Publisher,
#         'shop': Shop,
#         'book': Book,
#         'stock': Stock,
#         'sale': Sale,
#     }[record.get('model')]
#     session.add(model(id=record.get('pk'), **record.get('fields')))
# session.commit()


def shops(name):
    Pub = session.query(Publisher).filter(Publisher.name.like(name)).subquery()
    Bk = session.query(Book).join(Pub, Book.id_publisher == Pub.c.id).subquery()
    Stck = session.query(Stock).join(Bk, Stock.id_book == Bk.c.id).subquery()
    for sh in session.query(Shop).join(Stck, Shop.id == Stck.c.id_shop).all():
        print(sh)


print(shops("O’Reilly"))
print()


def book_sales(name_p=None, id_pub=None):
    if name_p:
        for b in session.query(Book.title).join(Publisher).join(
                         Stock).join(Shop).join(Sale).filter(Publisher.name == name_p):
            for sh in session.query(Shop.name).join(Stock).join(
                            Book).join(Sale).join(Publisher).filter(Publisher.name == name_p):
                for pr in session.query(Sale.price * Sale.count).join(
                        Stock).join(Book).join(Shop).join(Publisher).filter(Publisher.name == name_p):
                    for d in session.query(Sale.date_sale).join(
                            Stock).join(Book).join(Shop).join(Publisher).filter(Publisher.name == name_p):
                        print(b[0], sh[0], pr[0], d[0], sep=' | ')
    else:
        for b in session.query(Book.title).join(Publisher).join(
                Stock).join(Shop).join(Sale).filter(Publisher.id == id_pub):
            for sh in session.query(Shop.name).join(Stock).join(
                    Book).join(Sale).join(Publisher).filter(Publisher.id == id_pub):
                for pr in session.query(Sale.price * Sale.count).join(
                        Stock).join(Book).join(Shop).join(Publisher).filter(Publisher.id == id_pub):
                    for d in session.query(Sale.date_sale).join(
                            Stock).join(Book).join(Shop).join(Publisher).filter(Publisher.id == id_pub):
                        print(b[0], sh[0], pr[0], d[0], sep=' | ')


print(book_sales(name_p='Microsoft Press'))
