"""
Database models
"""

from django.conf import settings

from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Managers for users"""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Create a new superuser and return superuser."""
        user = self.create_user(email=email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Category(models.Model):
    """Category Database model."""
    name = models.CharField(max_length=100)
    # tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.name


class Discount(models.Model):
    """Models for Discount."""
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    percentage = models.IntegerField()

    def __str__(self):
        return f"{self.name}"


class Tag(models.Model):
    """Tag model."""
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title


class Product(models.Model):
    """Our Product Database Model."""
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True)
    image = models.ImageField(upload_to='product/', blank=True, null=True)
    stock = models.IntegerField(default=0)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    discounted_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    created = models.DateTimeField(auto_now_add=True)
    # tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f"{self.name}"

    def calculate_discount(self):
        """Calculate discount based on category."""
        try:
            discount_obj = Discount.objects.get(category=self.category)
            discount_amount = (self.price * discount_obj.percentage)/100
        except Discount.DoesNotExist:
            discount_amount = 0

        self.discount = discount_amount
        self.discounted_price = self.price-self.discount


class ProductTagConnector(models.Model):
    """Product Tag connector Model."""
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tag.title} {self.product.name}"


class Customer(models.Model):
    """Model for Customer."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    """Our Order Model."""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    cart_total = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    paid_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0)

    choice = (
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered')
    )

    order_status = models.CharField(
        choices=choice, default='Pending', max_length=20)

    def __str__(self):
        return f"{self.id}"

    def get_cart_total(self):
        """Calculate total order price"""
        # orderitems = self.orderitem_set.all()
        orderitems = self.order_items.all()
        total = sum([item.get_total() for item in orderitems])
        self.cart_total = total
        return total


class OrderItem(models.Model):
    """Model for storing order Items."""
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='order_items')
    # order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    item_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.id}'

    def get_total(self):
        """Calculate and return total price."""
        if self.product.discounted_price < 1:
            return self.product.price * self.quantity
        return self.product.discounted_price * self.quantity
