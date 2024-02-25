from django.contrib import admin

from apps.util.admin import BaseModelAdmin
from apps.store.models import(
    Category,
    Product,
    ProductReview,
    ProductReviewImageFiles,
    ProductVariant,
    Order,
    Cart,
    CartItem,
    WishList
)


class ProductModelAdmin(BaseModelAdmin):
    list_display = ('id', 'title', 'category')
    search_fields = ['title', 'uid']


class ProductVariantModelAdmin(BaseModelAdmin):
    list_display = ('id', 'product', 'quantity', 
                    'size', 'color', 'price')


class CartModelAdmin(BaseModelAdmin):
    list_display = ('id', 'user', 'total_amount')


class CartItemModelAdmin(BaseModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity')


class WishlistModelAdmin(BaseModelAdmin):
    list_display = ('id', 'user')


class OrderModelAdmin(BaseModelAdmin):
    list_display = ('id', 'user', 'order_id', 'order_status')


class ProductReviewModelAdmin(BaseModelAdmin):
    list_display = ('id', 'order', 'product', 'review', 'rating')


admin.site.register(Category)
admin.site.register(Product, ProductModelAdmin)
admin.site.register(ProductVariant, ProductVariantModelAdmin)
admin.site.register(Cart, CartModelAdmin)
admin.site.register(CartItem, CartItemModelAdmin)
admin.site.register(Order, OrderModelAdmin)
admin.site.register(WishList, WishlistModelAdmin)
admin.site.register(ProductReview, ProductReviewModelAdmin)
admin.site.register(ProductReviewImageFiles)
