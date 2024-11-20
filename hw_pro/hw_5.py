import logging
import datetime
from functools import total_ordering
from itertools import product

logger = logging.getLogger('main_cart')  # Створюємо логер
logger.setLevel(logging.DEBUG)  # Встановлюємо рівень логування
formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-(message)s')  # Формат виводу

file_handler = logging.FileHandler('main_cart.log')  # Файл для запису логів
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()  # Вивід на консоль
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)  # Додаємо обробники до логера
logger.addHandler(stream_handler)


########################################################################################################################
class PriceError(Exception):
    def __init__(self, message):
        super().__init__(message)
#########################################################################################################################

class CartIterator:
    def __init__(self, products,):
        self.products=products
        self.index=0

        self.__keys = list(self.products.keys())
        self.__values = list(self.products.values())

    def __next__(self):
            if self.index >= len(self.products):
                raise StopIteration
            self.index += 1
            return self.__keys[self.index - 1], self.__values[self.index - 1]

class Product:
    """
    Describes a product with a name and a price.
    """

    def __init__(self, name: str, price: float | int):
        """
        Initializes a product with a name and a price.

        :param name: name of the product
        :param price: price of the product
        """
        if not isinstance(price, int | float):
            logger.debug("Price must be a number")
            raise TypeError("Price must be a number")

        if price <= 0:
            logger.debug("Price must be positive")
            raise PriceError("Price must be positive")

        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.name}: {self.price}"


#################################################################################################

class Cart:
    """
    Describes a cart with products.
    """

    def __init__(self, cart_name:str):
        self.cart_name=cart_name

        self.__products = {}

    def __iter__(self):
        return CartIterator(self.__products)

    def add_product(self, product: Product, quantity: int | float = 1):
        """
        Adds a product to the cart.
        :param product: instance of the Product class
        :param quantity: quantity of the product
        :return: None
        """
        if not isinstance(quantity, int | float):
            logger.debug("Quantity must be a number")
            raise TypeError("Quantity must be a number")

        if quantity <= 0:
            logger.debug("Quantity must be positive")
            raise ValueError("Quantity must be positive")
        if not isinstance(product, Product):
            logger.debug("Product is not instance of the Product class")
            raise TypeError("Product must be an instance of the Product class")

        self.__products[product] = self.__products.get(product, 0) + quantity



    def __iadd__(self, other):
        """
         += operator for combining carts.
        """
        if isinstance(other, Cart):
            for product, quantity in other._Cart__products.items():
                self.add_product(product, quantity)
        else:
            raise TypeError("Can only add another Cart instance")
        return self


    def remove_product(self, product: Product, quantity: int | float = 1):
        """
        Removes a product from the cart.
        :param product: instance of the Product class
        :param quantity: quantity of the product
        :return: None
        """
        if not isinstance(quantity, int | float):
            logger.debug("Quantity must be a number")
            raise TypeError("Quantity must be a number")
        if quantity <= 0:
            logger.debug("Quantity must be positive")
            raise ValueError("Quantity must be positive")
        if not isinstance(product, Product):
            raise TypeError("Product must be an instance of the Product class")

        if product in self.__products:
            self.__products[product] -= quantity
            if self.__products[product] <= 0:
                del self.__products[product]

    def total(self):
        """
        Calculates the total price of the products in the cart.
        :return: total price of the products in the cart
        """
        return sum(product.price * quantity for product, quantity in self.__products.items())

    def __str__(self):
        res = '\n'.join(f"{product.name}: {quantity} x {product.price} UAH = {quantity * product.price} UAH"
                        for product, quantity in self.__products.items())
        return f"{self.cart_name}:\n{res}\nTotal {self.cart_name}: {self.total()} UAH"



##################################################################################################################
class PaymentProcessor:
    def __init__(self, cart: Cart):
        self.cart = cart

    def pay(self):
        print(f"Payment for {self.cart.total()} UAH is in progress...")


class DebitCardProcessor(PaymentProcessor):

    def pay(self):
        logger.info(f"Payment for {self.cart.total()} UAH by  debit card is in progress...")
        print(f"Payment for {self.cart.total()} UAH by debit card is in progress...")


class CreditCardProcessor(PaymentProcessor):

    def pay(self):
        logger.info(f"Payment for {self.cart.total()} UAH by credit card is in progress...")
        print(f"Payment for {self.cart.total()} UAH by credit card is in progress...")


class GooglePayProcessor(PaymentProcessor):

    def pay(self):
        logger.info(f"Payment for {self.cart.total()} UAH by GooglePay is in progress...")
        print(f"Payment for {self.cart.total()} UAH by GooglePay is in progress...")


##################################################################################################################
from datetime import datetime
class ProductMit_Milk(Product):
    def __init__(self, name: str, price: float | int, exp_date: str):
        super().__init__(name, price)
        self.exp_date = datetime.strptime(exp_date, "%d.%m.%Y").date()

    def __str__(self):
        return f"{super().__str__()} (expires on {self.exp_date})"

# для продуктів з терміном придатності
class CartProductMit_Milk(Cart):
    def __init__(self, cart_name: str):
        super().__init__(cart_name)

    def __iter__(self):
        return CartIterator(self._Cart__products)

# знижка
#     def apply_discounts(self):
#         today = datetime.now().date()
#         for product in self._Cart__products:
#             if isinstance(product, ProductMit_Milk):
#                 days_remaining = (product.exp_date - today).days
#                 if days_remaining <= 3:
#                     logger.info(f"50% discount to {product.name} (expiring soon)")
#                     product.price *= 0.5

##################################################################################################################
try:
    pr1 = Product("Fanta", 10)
    pr2 = Product("Solt", 5)
    pr3 = ProductMit_Milk("Butter", 20, '14.11.2024')
    pr4 = ProductMit_Milk("Milk", 15, '14.11.2024')

except PriceError as e:
    print(e)
except TypeError as e:
    print(e)
except Exception as e:
    print(e)

cart1 = Cart("CART1+2")
cartMit_Milk = CartProductMit_Milk('CART2')

try:
    cart1.add_product(pr1, 2)
    cart1.add_product(pr2, 3)
    cartMit_Milk.add_product(pr3, 3)
    cartMit_Milk.add_product(pr4, 4)

    cart1 += cartMit_Milk

except TypeError as e:
    print(e)
except ValueError as e:
    print(e)
except Exception as e:
    print(e)

ans = input('Debit / credit card or GooglePay?\n')
if ans == 'Debit':
    processor = DebitCardProcessor(cart1)
elif ans == 'credit':
    processor = CreditCardProcessor(cart1)
else:
    processor = GooglePayProcessor(cart1)

if cart1.total() > 0:
    print(cart1)
    print(cartMit_Milk)

    processor.pay()
for product, quantity in cart1:
    print(f"{product} x {quantity} = {product.price * quantity} UAH.")