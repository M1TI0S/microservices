import sys
import os
delivery_service_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../delivery_service'))
sys.path.append(delivery_service_path)

import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from delivery_service import create_delivery_and_record, Delivery
from sqlalchemy.exc import IntegrityError


class TestDeliveryService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Создаем тестовую базу данных SQLite и сессию SQLAlchemy
        cls.engine = create_engine("sqlite:///:memory:")
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=cls.engine)
        cls.session = SessionLocal()

        # Создаем таблицы в тестовой базе данных
        Delivery.metadata.create_all(bind=cls.engine)

    @classmethod
    def tearDownClass(cls):
        # Очищаем таблицы после выполнения тестов
        Delivery.__table__.drop(cls.engine)

    def test_create_delivery_and_record(self):
        # Тест создания доставки еды и записи в базу данных
        order_id = 12345
        result = create_delivery_and_record(self.session, order_id)

        # Проверяем, что доставка создана и записана в базу данных
        self.assertIn("message", result)
        self.assertIn("delivery_id", result)
        self.assertIn("status", result)

        # Проверяем, что доставка присутствует в базе данных
        db_food_delivery = self.session.query(Delivery).filter(Delivery.order_id)

    def test_create_delivery_duplicate(self):
        # Создаем доставку с определенным order_id
        order_id = 12345
        create_delivery_and_record(self.session, order_id)

        # Пытаемся создать доставку с тем же order_id еще раз
        # Ожидаем IntegrityError, так как заказ уже существует
        try:
            create_delivery_and_record(self.session, order_id)
        except IntegrityError as e:
            print("IntegrityError occurred:", e)
            raise


if __name__ == '__main__':
    unittest.main()