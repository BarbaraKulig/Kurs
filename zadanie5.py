import aiohttp
import asyncio
from datetime import datetime, timedelta
import argparse
import json

class PrivatBankApiClient:
    def __init__(self):
        self.base_url = 'https://api.privatbank.ua/#p24/exchangeArchive'
        self.session = aiohttp.ClientSession()

    async def get_exchange_rates(self, currency, days):
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days-1)
        url = f'{self.base_url}exchange_rates?json&date={start_date.strftime("%d.%m.%Y")}&date_to={end_date.strftime("%d.%m.%Y")}'

        try:
            async with self.session.get(url) as response:
                if response.status != 200:
                    print(f'Error: {response.status}')
                    return None
                data = await response.json()
                rates = data['exchangeRate']
                filtered_rates = [rate for rate in rates if rate['currency'] == currency]
                return filtered_rates
        except aiohttp.ClientError as e:
            print(f'Network error: {e}')
            return None

async def main(days):
    api_client = PrivatBankApiClient()

    currencies = ['USD', 'EUR']
    results = []

    for currency in currencies:
        exchange_rates = await api_client.get_exchange_rates(currency, days)
        if exchange_rates:
            rate_data = {
                currency: {
                    'sale': exchange_rates[0]['saleRate'],
                    'purchase': exchange_rates[0]['purchaseRate']
                }
            }
            results.append(rate_data)

    formatted_results = [{datetime.now().strftime("%d.%m.%Y"): result} for result in results]
    print(json.dumps(formatted_results, indent=2))

    await api_client.session.close()  # Close the session after all requests are done

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Retrieve exchange rates from PrivatBank API.')
    parser.add_argument('days', type=int, help='Number of days to retrieve exchange rates for (up to 10 days).')
    args = parser.parse_args()
    if args.days > 10:
        print("Error: Number of days cannot exceed 10.")
    else:
        asyncio.run(main(args.days))
