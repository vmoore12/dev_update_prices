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
                if product['type'] != 'simple':
                    s_name = product['name'] + ',' + product['type']
                    self.skipped_items.append(s_name)
                    continue

                reg_price = product['regular_price']
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





# woo_api = API(
#     url=url,
#     consumer_key=key,
#     consumer_secret=secret,
#     wp_api=True,
#     version='wc/v3'

# )

# per_page = 100
# current_page = 1
# count = 0
# skipped_items =[]
# # orig_price = []
# updated_price = []
# while True:
#         payload = {
#             "per_page": per_page,
#             "page": current_page, #Note: this show the specific page you want to see now
#         }

#         all_products = woo_api.get('products', params=payload).json()
#         if not all_products:
#                 break 
        
#         for product in all_products:
#             if product['type'] != 'simple':
#                 s_name = product['name'] +',' + product['type']
#                 skipped_items.append(s_name)
#                 continue
    
#             reg_price =  product['regular_price']
#             upd_price = round(float(reg_price) * 0.10, 2) + float(reg_price)
#             updated_price.append({'id': product['id'], 'old_price':{reg_price}, 'updated_price': {upd_price}})

#         current_page += 1

# with open('up10.csv', 'w', newline='') as f:
#       writer = csv.writer(f)
#       for i in updated_price:
#             row = f'product id = {i['id']}: old price - {i['old_price']}, new price -  {i['updated_price']}'
#             writer.writerow([row])
# print(updated_price)

