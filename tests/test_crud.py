import datetime

import pytest
from sqlalchemy import func

from app import create_app
from database import db
from models.userModel import User, Sample, Supplie, Order, Delivery, \
    OrderItem, Magacin, \
    Category, Status, ProductSales


@pytest.fixture
def app():
    app = create_app()
    with app.app_context():
        product_sales_data = [
            ProductSales(product_id=1, product_name='Laptop', quantity=2,
                         price=1200.00,
                         sale_date=datetime.datetime(2024, 4, 1),
                         customer_id=101, customer_name='John Doe',
                         region='North America'),
            ProductSales(product_id=2, product_name='Smartphone', quantity=1,
                         price=800.00, sale_date=datetime.datetime(2024, 4, 1),
                         customer_id=102, customer_name='Jane Smith',
                         region='Europe'),
            ProductSales(product_id=3, product_name='Tablet', quantity=3,
                         price=450.00, sale_date=datetime.datetime(2024, 4, 2),
                         customer_id=103, customer_name='Alice Johnson',
                         region='Asia'),
            ProductSales(product_id=4, product_name='Printer', quantity=1,
                         price=150.00, sale_date=datetime.datetime(2024, 4, 2),
                         customer_id=104, customer_name='Chris Lee',
                         region='North America'),
            ProductSales(product_id=5, product_name='Camera', quantity=2,
                         price=700.00, sale_date=datetime.datetime(2024, 4, 3),
                         customer_id=105, customer_name='Debbie Martin',
                         region='Europe'),
            ProductSales(product_id=6, product_name='Mouse', quantity=10,
                         price=25.00, sale_date=datetime.datetime(2024, 4, 3),
                         customer_id=106, customer_name='Frank Wright',
                         region='Asia'),
            ProductSales(product_id=7, product_name='Keyboard', quantity=5,
                         price=75.00, sale_date=datetime.datetime(2024, 4, 4),
                         customer_id=107, customer_name='Grace Hall',
                         region='North America'),
            ProductSales(product_id=8, product_name='Monitor', quantity=2,
                         price=300.00, sale_date=datetime.datetime(2024, 4, 4),
                         customer_id=108, customer_name='Bruce Adams',
                         region='Europe'),
            ProductSales(product_id=9, product_name='Desk', quantity=1,
                         price=250.00, sale_date=datetime.datetime(2024, 4, 5),
                         customer_id=109, customer_name='Nancy Clark',
                         region='Asia'),
            ProductSales(product_id=10, product_name='Chair', quantity=4,
                         price=125.00, sale_date=datetime.datetime(2024, 4, 5),
                         customer_id=110, customer_name='Jean Allen',
                         region='North America'),
            ProductSales(product_id=11, product_name='Notebook', quantity=20,
                         price=3.00, sale_date=datetime.datetime(2024, 4, 6),
                         customer_id=111, customer_name='Walter Harris',
                         region='Europe'),
            ProductSales(product_id=12, product_name='Pen', quantity=50,
                         price=1.50, sale_date=datetime.datetime(2024, 4, 6),
                         customer_id=112, customer_name='Tammy King',
                         region='Asia'),
            ProductSales(product_id=13, product_name='Backpack', quantity=3,
                         price=60.00, sale_date=datetime.datetime(2024, 4, 7),
                         customer_id=113, customer_name='Jerry Moore',
                         region='North America'),
            ProductSales(product_id=14, product_name='Watch', quantity=1,
                         price=250.00, sale_date=datetime.datetime(2024, 4, 7),
                         customer_id=114, customer_name='Gloria Young',
                         region='Europe'),
            ProductSales(product_id=15, product_name='Speaker', quantity=4,
                         price=150.00, sale_date=datetime.datetime(2024, 4, 8),
                         customer_id=115, customer_name='Howard Lopez',
                         region='Asia'),
            ProductSales(product_id=16, product_name='Headphones', quantity=6,
                         price=130.00, sale_date=datetime.datetime(2024, 4, 8),
                         customer_id=116, customer_name='Diane Hernandez',
                         region='North America'),
            ProductSales(product_id=17, product_name='Projector', quantity=1,
                         price=400.00, sale_date=datetime.datetime(2024, 4, 9),
                         customer_id=117, customer_name='Matthew Garcia',
                         region='Europe'),
        ]

        db.create_all()
        db.session.add_all(product_sales_data)
        db.session.commit()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


def test_user(app):
    with app.app_context():
        user = User(email="pera.cane@gmail.com", username="pera123",
                    password="123")

        db.session.add(user)
        db.session.commit()

        user_get = User.query.get(1)

        assert user_get.email == user.email

        users = User.query.all()

        assert len(users) == 1

        user_get.email = "abrakadaba@gmail.com"

        db.session.commit()
        user_get1 = User.query.get(1)
        assert user_get.email == user_get1.email


def test_sample(app):
    with app.app_context():
        # Craeate Category
        status = Category(name="Hemija",
                          description="Ciscenje osvezavanje prostora")
        status1 = Category(name="Hrana", description="Lagano osvezenje")
        status2 = Category(name="Grickalice", description="Lagano cascavanje")

        db.session.add_all([status, status1, status2])
        db.session.commit()

        categories = Category.query.all()
        assert 3 == len(categories)

        sample = Sample(name="Feri", price=123, description="Za sudove",
                        categories=[categories[0]])
        sample1 = Sample(name="Brownie", price=80, description="Za has",
                         categories=categories[1:])

        db.session.add_all([sample, sample1])
        db.session.commit()
        samples = Sample.query.all()
        assert 2 == len(samples)

        # Proveravamo uvezivanje
        category = Category.query.get(1)
        category2 = Category.query.get(2)
        category3 = Category.query.get(3)
        assert category.sample_id == 1
        assert category2.sample_id == 2
        assert category3.sample_id == 2

        magacin1 = Magacin(sample_id=1, amount=100)
        magacin2 = Magacin(sample_id=1, amount=200)
        magacin3 = Magacin(sample_id=2, amount=50)

        supplie = Supplie(name="Magacin NS", description="Magacnin u NS",
                          location="NS", magacin_id=1)
        supplie1 = Supplie(name="Magacin NBG", description="Magacnin u NBS",
                           location="NBG", magacin_id=2)
        supplie2 = Supplie(name="Magacin BG", description="Magacnin u BG",
                           location="BG", magacin_id=3)

        db.session.add_all(
            [magacin1, magacin2, magacin3, supplie, supplie1, supplie2])

        sample = Sample.query.get(1)

        assert sample.magacines == [magacin1, magacin2]
        supplies = Supplie.query.all()

        assert len(supplies) == 3

        magacin1 = Magacin.query.get(1)
        magacin1.amount = 10
        db.session.commit()
        mag1 = Magacin.query.get(1)
        assert magacin1.amount == mag1.amount
        db.session.delete(mag1)
        db.session.commit()
        mags = Magacin.query.all()
        assert 2 == len(mags)

        # ORDERS
        user = User(email="pera.cane@gmail.com", username="pera123",
                    password="123")

        db.session.add(user)
        db.session.commit()
        status = Status(name="Stize")
        status1 = Status(name="Krece")
        status2 = Status(name="Stiglo")
        order = Order(user_id=1, status_id=2)
        order1 = Order(user_id=1, status_id=3)
        db.session.add_all([status, status1, status2, order, order1])
        db.session.commit()

        orderItem = OrderItem(order_id=1, sample_id=1, amount=2)
        orderItem1 = OrderItem(order_id=1, sample_id=2, amount=2)
        orderItem2 = OrderItem(order_id=2, sample_id=2, amount=10)
        orderItem3 = OrderItem(order_id=2, sample_id=1, amount=30)

        db.session.add_all([orderItem, orderItem1, orderItem2, orderItem3])
        db.session.commit()

        ord1 = Order.query.get(1)

        assert ord1.items == [orderItem, orderItem1]

        date = datetime.datetime.now()
        delivery = Delivery(order=order, expected_del=date,
                            real_delivery=date - datetime.timedelta(
                                minutes=10))
        delivery1 = Delivery(order=order1, expected_del=date,
                             real_delivery=date + datetime.timedelta(
                                 minutes=10))

        db.session.add_all([delivery, delivery1])
        db.session.commit()

        # Ovde cemo da vidimo malo fje agregacije i pitanja!!
        # Izlistavaju narudžbine koje su kasnile u isporuci.

        delivery = Delivery.query.filter(
            (Delivery.real_delivery > Delivery.expected_del)).first()

        assert delivery == delivery1

        late_orders = (db.session.query(Order, Delivery.expected_del,
                                        Delivery.real_delivery)
                       .join(Delivery, Order.delivery_id == Delivery.id)
                       .filter(Delivery.real_delivery > Delivery.expected_del)
                       .all())

        # Ispis narudžbina koje su kasnile
        for order, expected, delivered in late_orders:
            print(
                f"Order ID: {order.id}, Expected Delivery: {expected}, Actual Delivery: {delivered}")


def test_product_sales(app):
    with app.app_context():
        pay = db.session.query(func.sum(ProductSales.price)).all()
        max_price = db.session.query(func.max(ProductSales.price)).first()
        group_by_date = db.session.query(
            func.sum(ProductSales.quantity)).group_by(ProductSales.sale_date)
        assert max_price[0] == 1200
        db_len = len(db.session.query(ProductSales).all())
        assert sorted(list(group_by_date)) == sorted(
            [(3,), (4,), (12,), (7,), (5,), (70,), (4,), (10,), (1,)])
        assert db_len == 17

        distinct = db.session.query(ProductSales.sale_date).distinct().all()
        assert len(distinct) == 9


def test_product_sales_get(app):
    with app.app_context():
        sales1 = db.session.query(ProductSales).get(10)

        assert sales1.product_name == "Chair"

        # LEts group sales per region and count them
        sales = db.session.query(func.count(ProductSales.id)).group_by(
            ProductSales.region).all()
        sales_count = ProductSales.query.filter_by(region="Asia").count()
        assert sales_count == 5
        assert sorted(sales) == sorted([(6,), (6,), (5,)])

        # kada radimo sa db.session.query(u zagradi bukvalno mozemo da stavimo sta zelimo
        # kao da pisemo from pa navodimo imena koja zelimo da izbacimo !!!

        # dobijanje ukupnih prihoda po proizvodu
        # Nece radi ako ne stavimo kao label product name
        # jer groupby zahteva da se ta labela nalazi u selest statement u SQL
        sales = db.session.query(ProductSales.product_name,
                                 func.sum(
                                     ProductSales.price * ProductSales.quantity)).group_by(
            ProductSales.product_name)
        sales = [sale[1] for sale in sales]
        assert sorted(
            [60, 75.0, 150.0, 180.0, 250.0, 250.0, 250.0, 375.0, 400.0, 500.0,
             600.0, 600.0, 780.0, 800.0, 1350.0, 1400.0, 2400.0]) == sorted(
            sales)

        # Prosecna cena po regionu
        average_sale = db.session.query(ProductSales.region,
                                        func.avg(ProductSales.price)).group_by(
            ProductSales.region).all()
        assert average_sale == [('Asia', 175.3), ('North America', 290.0),
                                ('Europe', 408.8333333333333)]

        date = datetime.datetime.now() - datetime.timedelta(days=50)
        # Pronalaženje prodaja iznad određene cene u poslednjih mesec dana
        sales = db.session.query(ProductSales.product_name).filter(
            ProductSales.price > 250, ProductSales.sale_date > date).all()

        assert [('Laptop',), ('Smartphone',), ('Tablet',), ('Camera',),
                ('Monitor',), ('Projector',)] == sales

        sum_region = db.session.query(ProductSales.region, func.sum(
            ProductSales.quantity * ProductSales.price)).group_by(
            ProductSales.region).all()

        assert sum_region == [('Asia', 2525.0), ('North America', 4385.0),
                              ('Europe', 3510.0)]

        # Having je jedna vrsta sorta kada odradimo group by
        # Having mora da ide neka labela iz modela ili ovako fja!
        sort_group = db.session.query(ProductSales.region,
                                      func.avg(ProductSales.quantity * ProductSales.price).label("suma")).group_by(
            ProductSales.region).having(func.avg(ProductSales.quantity * ProductSales.price) > 510).all()

        assert  sort_group == [('North America', 730.8333333333334), ('Europe', 585.0)]

        product_name = db.session.query(ProductSales.product_name).filter(ProductSales.product_name.contains("Pe")).first()
        assert product_name.product_name == "Pen"

        quantity = db.session.query(ProductSales.product_name,ProductSales.quantity).filter(ProductSales.quantity > 5, ProductSales.price>100).all()

        assert  quantity == [('Headphones', 6)]


        #Koliko sam video postoji caka vezivanja tabela tj neko nasledjivanje tabela
        # neka hijararhija da se napravi !!!
        # Mogucnost kreiranja nekih metoda koja mogu kasnije da sluze
        # Mogucnost kreiranja nekih logova!!
        #Alembic i migrate to smo vec odradili!!!
# Kreirajte ER dijagram koji prikazuje sve entitete i njihove veze.
# Definišite ključeve, strane ključeve, i ograničenja integriteta.
# Implementacija baze podataka
# Implementirajte bazu podataka koristeći sistem po vašem izboru (npr., MySQL, PostgreSQL, Microsoft SQL Server).
# Kreirajte tabele i veze među njima.
# Operacije i upiti
# Napišite SQL upite za dodavanje, ažuriranje, i brisanje podataka za svaki entitet.
# Napišite složene upite koji:
# Izračunavaju ukupnu vrednost svake narudžbine.
# Pronalaze top 5 najprodavanijih proizvoda.
# Izlistavaju narudžbine koje su kasnile u isporuci.
# Transakcije i sigurnost
# Definišite transakcije koje osiguravaju konzistentnost podataka prilikom izrade narudžbina i ažuriranja zaliha.
# Implementirajte mehanizme za kontrolu pristupa i sigurnost na nivou baze podataka.
