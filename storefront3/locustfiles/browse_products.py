from locust import HttpUser,task,between
from random import randint
import requests
class WebsiteUser(HttpUser):
    wait_time=between(1,5)
    #viewing products
    @task(2)
    def view_products(self):
        print('view products')
        collection_id=randint(2,6)
        self.client.get(
            f'/store/products/?collection_id={collection_id}',
            name='/store/products')
    #viewing product details
    @task(4)
    def view_product(self):
        print('view product details')
        product_id=randint(1,1000)
        self.client.get(
            f'/store/products/{product_id}',
            name='store/products/:1d')
    
    # add product to cart
    # @task(1)
    # def add_to_cart(self):
    #     print('add to cart')
    #     product_id=randint(1, 10)
    #     self.client.post(
    #         f'/store/carts/{self.cart_id}/items/',
    #         name='store/carts/items',
    #         json={'product_id':product_id,'quantity':1})
    # def on_start(self):
    #     response=self.client.post('/store/carts/')
    #     result=response.json()
    #     self.cart_id=result['id']
    # def on_start(self):
    #     response = self.client.post('/store/carts/')
    #     if response.status_code == 200:
    #         result = response.json()
    #         self.cart_id = result['id']
    #     else:
    #         print(f"Error creating cart: Status code {response.status_code}")
    #         return  # Or perform alternative action
    def on_start(self):
        response = self.client.post('/store/carts/')
        try:
            result = response.json()
        except requests.exceptions.JSONDecodeError:
            print(f"Error: Could not parse cart creation response as JSON. ({response.status_code})")
            return
        self.cart_id = result['id']

        # Add product to cart after retrieving cart ID
        product_id = randint(1, 10)
        self.client.post(
            f'/store/carts/{self.cart_id}/items/',
            name='store/carts/items',
            json={'product_id': product_id, 'quantity': 1})