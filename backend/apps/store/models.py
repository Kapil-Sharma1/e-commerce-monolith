from django.db import models
from django.db.models import Sum, F
from django.core.validators import(
    MaxValueValidator,
    MinValueValidator
)

from apps.util.models import AbstractBaseModel
from apps.users.models import User, Address


def product_image(instance, filename):
    return f'product/image/{instance.uid}/{filename}'

def product_review_image(instance, filename):
    return f'product/review/image/{instance.uid}/{filename}'


class Category(AbstractBaseModel):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Product(AbstractBaseModel):
    title = models.TextField()
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(max_length=500, upload_to=product_image, 
                            null=True, blank=True)
    category = models.ForeignKey(
        to=Category,
        related_name='products',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title
    
    def __repr__(self):
        return self.title


class ProductVariant(AbstractBaseModel):
    SIZE_CHOICES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    )
    COLOR_CHOICES = (
        ('R', 'Red'),
        ('G', 'Green'),
        ('B', 'Blue'),
        ('BL', 'Black'),
        ('W', 'White'),
    )
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name='product_variants'
    )
    quantity = models.IntegerField(default=0)
    size = models.CharField(max_length=2, choices=SIZE_CHOICES)
    color = models.CharField(max_length=2, choices=COLOR_CHOICES)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
    def __repr__(self):
        return self.title


class Cart(AbstractBaseModel):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name='cart'
    )
    total_amount = models.PositiveIntegerField(null=True, blank=True)

    @property
    def total_cost(self):
        total = self.cart_items.aggregate(
            total_cost=Sum(F('quantity') * F('product__product_price'))
            )['total_cost']
        return total or 0 

    def __str__(self):
        return f'{self.user.full_name} : {self.total_cost}'

    def __repr__(self):
        return f'{self.user.full_name} : {self.total_cost}' 
    

class CartItem(AbstractBaseModel):
    cart = models.ForeignKey(
        to=Cart,
        on_delete=models.CASCADE,
        related_name='cart_items'
    )
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name='cart_items'
    )
    quantity = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.product.title} : {self.quantity}' 

    def __repr__(self):
        return f'{self.product.title} : {self.quantity}' 


class WishList(AbstractBaseModel):
    products = models.ManyToManyField(
        to=Product,
        related_name='wish_lists'
    )
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name='wishlist'
    )

    def __str__(self):
        return self.user.full_name

    def __repr__(self):
        return self.user.full_name


class Order(AbstractBaseModel):
    products = models.ManyToManyField(
        to=Product,
        related_name='orders',
        null=True,
        blank=True
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    transaction_id = models.CharField(max_length=64, blank=True)
    billing_address = models.ForeignKey(
        to=Address,
        on_delete=models.CASCADE,
        related_name='billing_orders',
        null=True,
        blank=True
    )
    delivery_address = models.ForeignKey(
        to=Address,
        on_delete=models.CASCADE,
        related_name='delivery_orders',
        null=True,
        blank=True
    )
    order_id = models.CharField(max_length=24, blank=True)
    order_status = models.CharField(max_length=32, blank=True)
    delivered_on = models.DateField(null=True, blank=True)
    is_payment_completed = models.BooleanField(default=False)
    total_amount = models.PositiveIntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.user.full_name

    def __repr__(self):
        return self.user.full_name


class ProductReview(AbstractBaseModel):
    order = models.ForeignKey(
        to=Order,
        on_delete=models.CASCADE,
        related_name='product_reviews'
    )
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name='product_reviews'
    )
    review = models.CharField(max_length=2048, null=True, blank=True)
    rating = models.IntegerField(default=1, help_text='value should be 1 to 5', 
                                validators=[MaxValueValidator(5),
                                            MinValueValidator(1)])

    def __str__(self):
        return f'{self.order.user.full_name} : {self.product.title} : {self.rating}' 

    def __repr__(self):
        return f'{self.order.user.full_name} : {self.product.title} : {self.rating}' 


class ProductReviewImageFiles(AbstractBaseModel):
    files = models.FileField(null=True, blank=True, upload_to=product_review_image)
    product_review = models.ForeignKey(
        to=ProductReview,
        on_delete=models.CASCADE,
        related_name='product_review_image_files'
    )

    class Meta:
        verbose_name = "Product Review Image File"
        verbose_name_plural = "Product Review Image Files"
