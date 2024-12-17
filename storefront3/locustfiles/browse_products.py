from locust import HttpUser,task,between
from random import randit
class WebsiteUser(HttpUser):
    wait_time=between(1,5)
    #viewing products
    @task(2)
    def view_products(self):
        collection_id=randit(2,6)
        self.client.get(
            f'/store/products/?collection_id={collection_id}',
            name='/store/products')
    #viewing product details
    @task(4)
    def view_product(self):
        product_id=randit(1,1000)
        self.client.get(
            f'/store/products/{product_id}',
            name='store/products/:1d')
    
    # add product to cart
    @task(1)
    def add_to_cart(self):
        product_id=randit(1, 10)
        self.client.post(
            f'/store/carts/{self.cart_id}/items/',
            name='store/carts/items',
            json={'product_id':product_id,'quantity':1})
    def on_start(self):
        response=self.client.post('/start/carts/')
        result=response.json()
        self.cart_id=result['id']