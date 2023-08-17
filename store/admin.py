from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea, CharField
from django import forms
from django.db import models


class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ('email', 'username', 'name',)
    list_filter = ('email', 'username', 'name', 'is_active', 'is_staff')
    ordering = ('-start_date',)
    list_display = ('email', 'username', 'name',
                    'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'name',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 60})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'name', 'password1', 'password2', 'is_active', 'is_staff')}
         ),
    )

admin.site.register(Types)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Settings)
admin.site.register(Categories)
admin.site.register(CategoryPivot)
admin.site.register(TypeSettings)
admin.site.register(BannerImage)
admin.site.register(Banners)
admin.site.register(PromotionalSliders)
admin.site.register(ProductImage)
admin.site.register(ProductGallery)
admin.site.register(Shop)
admin.site.register(ShopImage)
admin.site.register(ShopLocation)
admin.site.register(Address)
admin.site.register(ShopSettings)
admin.site.register(Logo)
admin.site.register(Socials)
admin.site.register(Location)
admin.site.register(Options)
admin.site.register(ContactDetails)
admin.site.register(DeliveryTime)
admin.site.register(Seo)
admin.site.register(ShopOwner)
admin.site.register(Profile)
admin.site.register(UserAddress)
admin.site.register(User, UserAdminConfig)
admin.site.register(Token)
admin.site.register(Permissions)
admin.site.register(AuthResponse)
admin.site.register(Me)
admin.site.register(OrderStatus)
admin.site.register(SocialLoginToken)
admin.site.register(Tag)
admin.site.register(Author)
admin.site.register(Manufacturer)
admin.site.register(Coupon)
admin.site.register(VerifiedCheckoutData)
admin.site.register(Attachment)
admin.site.register(ConnectProductOrderPivot)
admin.site.register(OrderProductPivot)