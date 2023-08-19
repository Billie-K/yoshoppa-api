from email.policy import default
from pkg_resources import require
from rest_framework import serializers, viewsets
from .models import *
from drf_writable_nested.serializers import WritableNestedModelSerializer


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class TypeSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeSettings
        fields = ('isHome', 'layoutType', 'productCard')

class PromotionalSlidersSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionalSliders
        fields = ('id', 'original', 'thumbnail')

class BannerImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BannerImage
        fields = ('id', 'name', 'original', 'thumbnail')


class BannersSerializer(serializers.ModelSerializer):
    image = BannerImageSerializer(many=False)

    class Meta:
        model = Banners
        fields = ('id', 'type_id', 'title', 'description', 'image', 'created_at', 'updated_at')


class TypesSerializer(serializers.HyperlinkedModelSerializer):
    settings = TypeSettingsSerializer(many=False)
    promotional_sliders = PromotionalSlidersSerializer(many=True)
    banners = BannersSerializer(many=True)
    
    class Meta:
        model = Types
        fields = ('id', 'name', 'settings', 'slug', 'icon', 'promotional_sliders', 
        'created_at', 'updated_at', 'banners')
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class ShopImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopImage
        fields = ('id', 'original', 'thumbnail')


class LogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logo
        fields = ('id', 'original', 'thumbnail')


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'zip', 'city', 'state', 'country', 'street_address')


class SocialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Socials
        fields = ('url', 'icon')


class ShopLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopLocation
        fields = ('lat', 'lng', 'city', 'state', 'country', 'formattedAddress')

class ShopSettingsSerializer(serializers.ModelSerializer):
    socials = SocialsSerializer(many=True)
    location = ShopLocationSerializer(many=False)

    class Meta:
        model = ShopSettings
        fields = ('contact', 'socials', 'website', 'location')


class ShopSerializer(serializers.ModelSerializer):
    cover_image = ShopImageSerializer(many=False)
    logo = LogoSerializer(many=False)
    address = AddressSerializer(many=False)
    settings = ShopSettingsSerializer(many=False)

    class Meta:
        model = Shop
        fields = ('id', 'owner_id', 'name', 'slug', 'description', 'cover_image', 'logo',
        'is_active', 'address', 'settings', 'created_at', 'updated_at')
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'original', 'thumbnail')


class ProductGallerySerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)

    class Meta:
        model = ProductGallery
        fields = ('name', 'images')

class CategoryPivotSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryPivot
        fields = ('product_id', 'category_id')


class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('id', 'name', 'slug', 'icon', 'image', 'details', 'parent', 
        'typeId', 'created_at', 'updated_at', 'deleted_at')


class ChildrenSerializer(serializers.ModelSerializer):
    parent = ParentSerializer(many=False)

    class Meta:
        model = Categories
        fields = ('id', 'name', 'slug', 'icon', 'image', 'details', 'parent', 
        'typeId', 'created_at', 'updated_at', 'deleted_at','products_count')

class CategoriesSerializer(serializers.ModelSerializer):
    image = ProductImageSerializer(many=True)
    parent = ChildrenSerializer(many=False)
    children = ChildrenSerializer(many=True)
    type = TypesSerializer(many=False)

    class Meta:
        model = Categories
        fields = ('id', 'name', 'slug', 'icon', 'image', 'details', 'parent', 'created_at', 
        'updated_at', 'deleted_at', 'type', 'children')


class OrderProductPivotSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProductPivot
        fields = '__all__'

class RelatedProductSerializer(serializers.ModelSerializer):
    image = ProductImageSerializer(many=False)
    # gallery = ProductGallerySerializer(many=False)
    # type = TypesSerializer(many=False)
    # shop = ShopSerializer(many=False)
    # categories = CategoriesSerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'image')

class ProductSerializer(DynamicFieldsModelSerializer):
    image = ProductImageSerializer(many=False)
    gallery = ProductGallerySerializer(many=False)
    type = TypesSerializer(many=False)
    shop = ShopSerializer(many=False)
    categories = CategoriesSerializer(many=True)
    pivot = OrderProductPivotSerializer(many=False)

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'description', 'price', 'sales_price', 'sku', 'quantity', 'in_stock', 
        'is_taxable', 'is_digital', 'shipping_class_id', 'status', 'product_type', 'unit', 'height', 'width', 'length', 
        'image', 'gallery', 'created_at', 'updated_at', 'max_price', 'min_price', 'type', 'product_type',
        'shop', 'categories', 'pivot')
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }

# class ProductWithRelatedSerializer(ProductSerializer):
#     related_products = serializers.SerializerMethodField(read_only=True)

#     def get_related_products(self, obj):
#         related = Product.objects.filter(shop_id=obj.shop_id).exclude(id=obj.pk)[:4]
#         product = RelatedProductSerializer(related, many=True)
#         return product.data

#     class Meta:
#         model = Product
#         fields = ('id', 'name', 'slug', 'description', 'price', 'sales_price', 'sku', 'quantity', 'in_stock', 
#         'is_taxable', 'shipping_class_id', 'status', 'product_type', 'unit', 'height', 'width', 'length', 
#         'image', 'gallery', 'created_at', 'updated_at', 'max_price', 'min_price', 'type', 'product_type',
#         'shop', 'categories', 'pivot', 'related_products')
        

class SeoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seo
        fields = ('ogImage', 'ogTitle', 'metaTags', 'metaTitle', 'canonicalUrl', 'ogDescription', 'twitterHandle',
        'metaDescription', 'twitterCardType')


class DeliveryTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryTime
        fields = ('title', 'description')


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('lat', 'lng', 'city', 'state', 'country', 'formattedAddress')


class ContactDetailsSerializer(serializers.ModelSerializer):
    socials = SocialsSerializer(many=True)
    location = LocationSerializer(many=False)

    class Meta:
        model = ContactDetails
        fields = ('contact', 'socials', 'website', 'location')

class OptionsSerializer(serializers.ModelSerializer):
    seo = SeoSerializer(many=False)
    logo = LogoSerializer(many=False)
    deliveryTime = DeliveryTimeSerializer(many=True)
    contactDetails = ContactDetailsSerializer(many=False)

    class Meta:
        model = Options
        fields = ('seo', 'logo', 'useOtp', 'currency', 'taxClass', 'siteTitle', 'deliveryTime', 'siteSubtitle', 
        'shippingClass', 'contactDetails', 'minimumOrderAmount')


class SettingsSerializer(serializers.ModelSerializer):
    options = OptionsSerializer(many=False)

    class Meta:
        model = Settings
        fields = ('id', 'options', 'created_at', 'updated_at')


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('email', 'password')

class ProfileSerializer(serializers.ModelSerializer):
    avatar = ShopImageSerializer(many=False, required=False)
    socials = SocialsSerializer(many=False, required=False)

    class Meta:
        model = Profile
        fields = ('avatar', 'bio', 'socials', 'contact', 'customer_id', 'created_at', 'updated_at')


class UserAddressSerializer(WritableNestedModelSerializer):
    address = AddressSerializer(many=False)    

    class Meta:
        model = UserAddress
        fields = ('title', 'type', 'default','user', 'address', 'customer_id', 'created_at', 'updated_at')



class PermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permissions
        fields = ('id', 'name', 'guard_name', 'created_at', 'updated_at')

class UserSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    address = UserAddressSerializer(many=True, required=False)
    permissions = PermissionsSerializer(many=True, required=False)
    profile = ProfileSerializer(many=False, required=False)
    password = serializers.CharField(required=False, min_length=8, write_only=True)

    def validate_email(self, email):
        User = self.Meta.model
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email already registered to a user.')
        return email

    def validate_username(self, username):
        User = self.Meta.model
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Username already taken. Try another one.')
        return username

    class Meta:
        model =  User
        fields = ('address', 'created_at', 'email', 'email_verified_at','id','is_active','name','permissions',
        'profile','shop_id','updated_at','username','password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        # as long as the fields are the same, we can just use this
        user = self.Meta.model.objects.create(**validated_data)
        if password is not None:
            user.set_password(password)
        user.save()
        return user


class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class CardInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardInput
        fields = '__all__'

class ConnectProductOrderPivotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectProductOrderPivot
        fields = '__all__'

class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = ('id', 'name', 'serial', 'color', 'created_at', 'updated_at')



# class OrderSerializer(serializers.ModelSerializer):
#     address = AddressSerializer(many=False)
#     customer = UserSerializer(many=False,required=False)
#     products  = ConnectProductOrderPivotSerializer(many=True)

#     def get_or_create_products(self, products):
#         product_ids = []
#         for product in products:
#             product_instance, created = ConnectProductOrderPivot.objects.get_or_create(pk=product.get('id'), defaults=product)
#             product_ids.append(product_instance.pk)
#         return product_ids

#     class Meta:
#         model = Order
#         fields = ('id', 'tracking_number', 'customer_id', 'customer_contact', 'status', 'amount',
#         'sales_tax', 'paid_total', 'total', 'coupon_id', 'shop_id', 'discount', 'payment_id',
#         'address', 'logistics_provider', 'delivery_fee', 'delivery_time', 'deleted_at', 'created_at',
#         'updated_at', 'customer', 'products','card')
    
#     def create(self, validated_data):
#         product = validated_data.pop('products', [])
#         address_data = validated_data.pop('address')
#         order = Order.objects.create(**validated_data)
#         order.save()
#         order.products.set(self.get_or_create_products(product))
#         Address.objects.create(order=order, **address_data)
#         return order

    # For later use 
    # def update(self, instance, validated_data):
    #     package = validated_data.pop('package', [])
    #     instance.package.set(self.create_or_update_packages(package))
    #     fields = ['order_id', 'is_cod']
    #     for field in fields:
    #         try:
    #             setattr(instance, field, validated_data[field])
    #         except KeyError:  # validated_data may not contain all fields during HTTP PATCH
    #             pass
    #     instance.save()
    #     return instance


class RegisterSerializer(serializers.ModelSerializer):
    permission = serializers.CharField(default='CUSTOMER')

    class Meta:
        model = Register
        fields = ('email', 'name', 'password', 'permission')



class AuthResponseSerializer(serializers.ModelSerializer):
    permissions = PermissionsSerializer(many=True)
    
    class Meta:
        model = AuthResponse
        fields = ('token', 'permissions')

class PasswordChangeResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordChangeResponse
        fields = ('id', 'success', 'message')


class OtpResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtpResponse
        fields = ('id', 'message', 'success', 'phone_number', 'provider', 'is_contact_exist')


class MeSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False)
    address = UserAddressSerializer(many=True)
    permissions = PermissionsSerializer(many=True)

    class Meta:
        model = Me
        fields = ('is_active', 'id', 'name', 'email', 'email_verified_at', 'created_at', 'updated_at', 
        'shop_id', 'profile', 'address', 'permissions')


class SocialLoginTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLoginToken
        fields = ('provider', 'access_token')



class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ('original','thumbnail','id')

class TagSerializer(serializers.ModelSerializer):
    image = AttachmentSerializer(many=True)
    type = TypesSerializer
    
    class Meta:
        model = Tag
        fields = ('id', 'name','slug','icon','image','details','type', 'created_at','updated_at')


class AuthorSerializer(serializers.ModelSerializer):
    image = AttachmentSerializer(many=False)
    cover_image = AttachmentSerializer(many=False)
    socials = SocialsSerializer(many=True)

    class Meta:
        model = Author
        fields = ('id','name','is_approved','image','cover_image','slug','bio','born','death','languages',
        'socials','created_at','updated_at','products_count')

class ManufacturerSerializer(serializers.ModelSerializer):
    type = TypesSerializer(many=False)
    image = AttachmentSerializer(many=False)
    cover_image = AttachmentSerializer(many=False)
    socials = SocialsSerializer(many=True)

    class Meta:
        model = Manufacturer
        fields = ('name','is_approved','image','cover_image','slug','type','description','website',
        'socials','created_at','updated_at','products_count')


class CouponSerializer(serializers.ModelSerializer):
    image = AttachmentSerializer(many=False)
    class Meta:
        model = Coupon
        fields = ('id','code','description','image','type','amount','active_from','expire_at',
        'created_at','updated_at','deleted_at','is_valid')


class VerifiedCheckoutDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerifiedCheckoutData
        fields = ('total_tax','shipping_charge','unavailable_products','wallet_currency','wallet_amount')


class OrderSerializer(serializers.ModelSerializer):
    customer = UserSerializer(many=False, required=False)
    # status = OrderStatusSerializer(many=False)
    coupon = CouponSerializer(many=False, required=False)
    shop = ShopSerializer(many=False, required=False)
    products = ConnectProductOrderPivotSerializer(many=True)
    address = AddressSerializer(many=False)
    # shipping_address = serializers.SerializerMethodField()

    def get_or_create_products(self, products):
        product_ids = []
        for product in products:
            product_instance, created = ConnectProductOrderPivot.objects.get_or_create(pk=product.get('id'), defaults=product)
            product_ids.append(product_instance.pk)
        return product_ids

    class Meta:
        model = Order
        fields = ('tracking_number', 'customer_id', 'customer_contact', 'customer', 'parent_order', 
        'children', 'status', 'amount', 'sales_tax', 'total', 'paid_total', 'payment_id', 'payment_gateway',
        'coupon', 'shop', 'discount', 'delivery_fee', 'delivery_time', 'products',
        'address', 'id', 'created_at', 'updated_at')
    
    # def get_address(self, obj):
    #     order_billing_address = UserAddress.objects.get(customer_id=obj.customer_id, type='billing')
    #     serializer = UserAddressSerializer(order_billing_address, many=False)
    #     return serializer.data
    
    # def get_shipping_address(self, obj):
    #     order_shipping_address = UserAddress.objects.get(customer_id=obj.customer_id, type='shipping')
    #     serializer = UserAddressSerializer(order_shipping_address, many=False)
    #     return serializer.data

    def create(self, validated_data):
        product = validated_data.pop('products', [])
        address_data = validated_data.pop('address')
        # shipping_address_data = validated_data.pop('shipping_address')
        order = Order.objects.create(**validated_data)
        order.save()
        order.products.set(self.get_or_create_products(product))
        Address.objects.create(order=order, **address_data)
        return order