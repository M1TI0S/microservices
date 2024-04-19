import unittest
from unittest import mock
import requests

class TestDelivery(unittest.TestCase):
    @mock.patch('requests.post')
    def test_create_delivery(self, mock_post):
        # Настройка имитации ответа от сервера
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        # Вызов метода, который мы тестируем
        response = requests.post("http://localhost:8080/delivery/")

        # Проверка результатов
        self.assertEqual(response.status_code, 200)
        mock_post.assert_called_once_with("http://localhost:8080/delivery/")

if __name__ == '__main__':
    unittest.main()