
""" Python script that will update all prices on the dev site by 10%."""

from cred import url,key,secret
from woocommerce import API
import random
import time
import string
import csv



class WooCommerceUpdater:
    def __init__(self):
        self.woo_api = API(
            url=url,
            consumer_key=key,
            consumer_secret=secret,
            wp_api=True,
            version='wc/v3'
        )
        self.per_page = 100
        self.current_page = 1
        self.count = 0
        self.skipped_items = []
        self.updated_price = []

    def update_prices(self):
        while True:
            payload = {
                "per_page": self.per_page,
                "page": self.current_page,
            }

            all_products = self.woo_api.get('products', params=payload).json()
            if not all_products:
                break

            for product in all_products:
                reg_price = product['regular_price']
                if reg_price == '':
                   no_price_id =  product['id']
                   no_price_name = product['sku']
                   print(f'Product id #{no_price_id} named {no_price_name} has no price to update')
                   continue
                upd_price = round(float(reg_price) * 0.10, 2) + float(reg_price)
                self.updated_price.append({'id': product['id'], 'old_price': reg_price, 'updated_price': upd_price})

            self.current_page += 1

    def write_to_csv(self):
        with open('up10.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            for i in self.updated_price:
                row = f"product id = {i['id']}: old price - {i['old_price']}, new price - {i['updated_price']}"
                writer.writerow([row])


updater = WooCommerceUpdater()

updater.update_prices()
updater.write_to_csv()
print(updater.skipped_items)
print(updater.updated_price)





