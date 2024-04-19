import unittest
import requests


class TestDelivery(unittest.TestCase):
    def test_create_delivery(self):
        # Отправляем POST-запрос на /delivery/{order_id}
        order_id = 123
        response = requests.post(f"http://localhost:80/delivery/{order_id}")

        # Проверяем, что сервер возвращает код статуса
        self.assertEqual(response.status_code, 200)  # Изменено на 200, так как это успешный запрос

    def test_read_delivery(self):
        # Отправляем GET-запрос на /delivery/{order_id}
        order_id = 123
        response = requests.get(f"http://localhost:80/delivery/{order_id}")

        # Проверяем, что сервер возвращает код статуса
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()