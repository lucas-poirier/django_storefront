from django.test import TestCase
from django.contrib.auth.models import User
from shop.models import Product, Cart, CartItem
from django.urls import reverse

class BaseTestCase(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")

        # Create some product instances for testing
        self.djan = Product.objects.create(
            name="Djan",
            description="Good Djan",
            price=9.99,
            stock=100,
        )
        self.djan_pro = Product.objects.create(
            name="Djan Pro",
            description="Best Djan",
            price=19.99,
            stock=100,
        )
        self.go = Product.objects.create(
            name="Go",
            description="Good Go",
            price=24.99,
            stock=100,
        )
        self.go_pro = Product.objects.create(
            name="Go Pro",
            description="Best Go",
            price=29.99,
            stock=100,
        )
        # Create a cart instance for testing
        self.cart = Cart.objects.create(user=self.user)

        # Create cart items for testing
        # self.cart_item1 = CartItem.objects.create(cart=self.cart, product=self.djan, quantity=2)
        # self.cart_item2 = CartItem.objects.create(cart=self.cart, product=self.djan_pro, quantity=3)
        # self.cart_item3 = CartItem.objects.create(cart=self.cart, product=self.go, quantity=1)
        # self.cart_item4 = CartItem.objects.create(cart=self.cart, product=self.go_pro, quantity=4)
    
    def tearDown(self):
        # Clean up after tests
        self.user.delete()

class ProductTestCase(BaseTestCase):

    def test_product_creation(self):
        # Test if the product was created successfully
        self.assertEqual(self.djan.name, "Djan")
        self.assertEqual(self.djan.description, "Good Djan")
        self.assertEqual(self.djan.price, 9.99)
        self.assertEqual(self.djan.stock, 100)
    
    def test_product_stock_update(self):    
        # Test if the stock can be updated correctly
        self.djan.stock = 50
        self.djan.save()
        self.assertEqual(self.djan.stock, 50)
        self.djan.stock = 100

class CartTestCase(BaseTestCase):
    
    def test_cart_creation(self):
        # Test if the cart was created successfully
        self.assertEqual(self.cart.user, self.user)
        self.assertEqual(self.cart.items.count(), 0)
    
    def test_cart_total_price(self):
        # Test if the total price is calculated correctly
        cart_item1 = CartItem.objects.create(cart=self.cart, product=self.djan, quantity=2)
        cart_item2 = CartItem.objects.create(cart=self.cart, product=self.djan_pro, quantity=3)

        self.assertEqual(float(self.cart.total_price), (cart_item1.total_price() + cart_item2.total_price()))
    
    def test_cart_item_creation(self):
        # Test if the cart item was created successfully
        cart_item = CartItem.objects.create(cart=self.cart, product=self.djan, quantity=2)
        self.assertEqual(cart_item.cart, self.cart)
        self.assertEqual(cart_item.product, self.djan)
        self.assertEqual(cart_item.quantity, 2)
    
    def test_cart_item_total_price(self):
        # Test if the total price of a cart item is calculated correctly
        cart_item = CartItem.objects.create(cart=self.cart, product=self.djan, quantity=3)
        self.assertEqual(cart_item.total_price(), self.djan.price * cart_item.quantity)
    
    def test_cart_item_quantity_update(self):
        # Test if the quantity of a cart item can be updated correctly
        cart_item = CartItem.objects.create(cart=self.cart, product=self.djan, quantity=2)
        cart_item.quantity = 5
        cart_item.save()
        self.assertEqual(cart_item.quantity, 5)
    
    def test_cart_item_deletion(self):
        # Test if a cart item can be deleted
        cart_item = CartItem.objects.create(cart=self.cart, product=self.djan, quantity=2)
        cart_item.delete()
        self.assertEqual(self.cart.items.count(), 0)
    
    def test_cart_item_stock_update(self):
        # Test if the stock of a product is updated correctly when added to the cart
        cart_item = CartItem.objects.create(cart=self.cart, product=self.djan, quantity=2)
        self.djan.stock -= cart_item.quantity
        self.djan.save()
        self.assertEqual(self.djan.stock, 98)
    
    def test_cart_item_stock_check(self):
        # Test if the stock is checked correctly when adding to the cart
        cart_item = CartItem.objects.create(cart=self.cart, product=self.djan, quantity=2)
        self.assertTrue(cart_item.product.stock >= cart_item.quantity)

