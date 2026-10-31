from django.db import models                       # gives us tools to define database tables
from django.contrib.auth.models import User        # Django's ready-made User table (handles users and passwords)


class Product(models.Model):                       # a class = a table. Product table.
    name = models.CharField(max_length=100)        # short text, max 100 characters
    description = models.TextField()               # long text, no limit
    price = models.DecimalField(max_digits=8, decimal_places=2)   # numbers like 499.99 (use Decimal for money, not float)
    image_url = models.URLField(blank=True)        # link to an image; blank=True means it's optional

    def __str__(self):                             # how this object appears in the admin panel
        return self.name                           # show the product name instead of "Product object (1)"


class Order(models.Model):                         # one row = one order placed by one customer
    user = models.ForeignKey(User, on_delete=models.CASCADE)   # which user placed it
    address = models.TextField()                   # delivery address
    total = models.DecimalField(max_digits=10, decimal_places=2)   # total bill
    created_at = models.DateTimeField(auto_now_add=True)   # date/time filled automatically when created

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


class OrderItem(models.Model):                     # one row = one product inside an order
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()       # whole number, 0 or more
    price = models.DecimalField(max_digits=8, decimal_places=2)   # price at the time of purchase

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"