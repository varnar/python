import unittest
from unittest.mock import patch
from currency_converter_online import get_exchange_rate, convert_currency

class TestCurrencyConverter(unittest.TestCase):

    @patch('currency_converter_online.requests.get')
    def test_get_exchange_rate(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'conversion_rates': {
                'EUR': 0.85
            }
        }

        api_key = '08906ffe6c7ad809aa8deef6'
        base_currency = 'USD'
        target_currency = 'EUR'
        exchange_rate = get_exchange_rate(api_key, base_currency, target_currency)
        self.assertEqual(exchange_rate, 0.85)

    @patch('currency_converter_online.get_exchange_rate')
    def test_convert_currency(self, mock_get_exchange_rate):
        mock_get_exchange_rate.return_value = 0.85

        amount = 100
        base_currency = 'USD'
        target_currency = 'EUR'
        converted_amount = convert_currency(amount, base_currency, target_currency)
        self.assertEqual(converted_amount, 85.0)

if __name__ == '__main__':
    unittest.main()