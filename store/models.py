import email
from email.policy import default
from importlib.abc import Traversable
from io import open_code
from tabnanny import verbose
import types
from django.db import models
# from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField
from django.db.models.fields.files import ImageField
from django.db.models.fields.related import OneToOneField
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.crypto import get_random_string
from django.utils.text import slugify

# Create your models here.
class Customer(models.Model):
	"""Defines customers"""
	user = models.OneToOneField('User', on_delete=models.CASCADE, null=True, blank=True)
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	email_verified_at = models.DateTimeField(null=True)
	created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
	is_active = models.BooleanField(null=True)
	shop_id = models.IntegerField(null=True, blank=True, default=1)
	
	def __str__(self):
		return self.name


class Seo(models.Model):
	ogImage = models.CharField(max_length=200, null=True, blank=True)
	ogTitle = models.CharField(max_length=200, null=True, blank=True)
	metaTags = models.CharField(max_length=200, null=True, blank=True)
	metaTitle = models.CharField(max_length=200, null=True, blank=True)
	canonicalUrl = models.CharField(max_length=200, null=True, blank=True)
	ogDescription = models.CharField(max_length=200, null=True, blank=True)
	twitterHandle = models.CharField(max_length=200, null=True, blank=True)
	metaDescription = models.CharField(max_length=200, null=True, blank=True)
	twitterCardType = models.CharField(max_length=200, null=True, blank=True)

	def __str__(self):
		return str(self.id)


class Logo(models.Model):
	name = models.CharField(max_length=200)
	original = models.ImageField()
	thumbnail = models.ImageField()

	def __str__(self):
		return self.name

	@property
	def imageURL(self):
		try:
			url = self.original.url
		except:
			url = ''
		return url


class DeliveryTime(models.Model):
	title = models.CharField(max_length=200, null=True, blank=True)
	description = models.CharField(max_length=200, null=True, blank=True)

	def __str__(self):
		return self.title


class Socials(models.Model):
	url = models.CharField(max_length=200)
	icon = models.CharField(max_length=200)

	def __str__(self):
		return self.icon

	class Meta:
		verbose_name_plural = 'Socials'


class Location(models.Model):
	lat = models.FloatField()
	lng = models.FloatField()
	city = models.CharField(max_length=200)
	state = models.CharField(max_length=200)
	country = models.CharField(max_length=200)
	formattedAddress = models.CharField(max_length=200)

	def __str__(self):
		return self.formattedAddress


class ContactDetails(models.Model):
	contact = models.CharField(max_length=200, null=True, blank=True)
	socials = models.ManyToManyField(Socials)
	website = models.CharField(max_length=200, null=True, blank=True)
	location = models.ForeignKey(Location, on_delete=models.CASCADE)

	def __str__(self):
		return self.contact


class Options(models.Model):
	seo = models.ForeignKey(Seo, on_delete=models.CASCADE)
	logo = models.ForeignKey(Logo, on_delete=models.CASCADE)
	useOtp = models.BooleanField(default=False)
	currency = models.CharField(max_length=200, blank=True, null=True)
	taxClass = models.IntegerField()
	siteTitle = models.CharField(max_length=200)
	deliveryTime = models.ManyToManyField(DeliveryTime)
	siteSubtitle = models.CharField(max_length=200, null=True, blank=True)
	shippingClass = models.IntegerField()
	contactDetails = models.ForeignKey(ContactDetails, on_delete=models.CASCADE)
	minimumOrderAmount = models.IntegerField()

	class Meta:
		verbose_name_plural = 'Options'

	def __str__(self):
		return str(self.id)


class Settings(models.Model):
	"""The site settings needed to define site details"""
	options = models.ForeignKey(Options, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

	class Meta:
		verbose_name_plural = 'Settings'

	def __str__(self):
		return str(self.id)


class TypeSettings(models.Model):
	"""This model defines the site theme for Type Model"""
	isHome = models.BooleanField()

	#Layout options
	CLASSIC = 'classic'
	MODERN = 'modern'
	STANDARD = 'standard'
	COMPACT = 'compact'
	MINIMAL = 'minimal'
	LAYOUT_CHOICES = [
		(CLASSIC, 'Classic'),
		(MODERN, 'Modern'),
		(STANDARD, 'Standard'),
		(COMPACT, 'Compact'),
		(MINIMAL, 'Minimal'),
	]
	layoutType = models.CharField(max_length=20, choices=LAYOUT_CHOICES, default=CLASSIC)

	#Product Card Options
	KRYPTON = 'krypton'
	RADON = 'radon'
	OGANESSON = 'oganesson'
	NEON = 'neon'
	XENON = 'xenon'
	HELIUM = 'helium'
	ARGON = 'argon'
	CARD_CHOICES = [
		(KRYPTON, 'Krypton'),
		(RADON, 'Radon'),
		(OGANESSON, 'Oganesson'),
		(NEON, 'Neon'),
		(XENON, 'Xenon'),
		(HELIUM, 'Helium'),
		(ARGON, 'Argon'),
	]
	productCard = models.CharField(max_length=20, choices=CARD_CHOICES, default=ARGON)

	def __str__(self):
		return self.layoutType + ' ' + self.productCard

	class Meta:
		verbose_name_plural = 'TypeSettings'


class PromotionalSliders(models.Model):
	"""Model for promotional sliders for each page"""
	original = models.ImageField(null=True, blank=True)
	thumbnail = models.ImageField(null=True, blank=True)

	def __str__(self):
		return str(self.id)

	class Meta:
		verbose_name_plural = 'PromotionalSliders'


class BannerImage(models.Model):
	"""Specifies images to use on banners"""
	name = models.CharField(max_length=200, null=True, blank=True)
	original = models.ImageField()
	thumbnail = models.ImageField(null=True, blank=True)


	def __str__(self):
		return str(self.id)


class Banners(models.Model):
	"""Model for the banner for each page"""
	type_id = models.IntegerField()
	title = models.CharField(max_length=200)
	description = models.CharField(max_length=200, null=True, blank=True)
	image = models.ForeignKey(BannerImage, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title

	class Meta:
		verbose_name_plural = 'Banners'


class Types(models.Model):
	"""Defines shop types from a selection of types we have"""
	name = models.CharField(max_length=20)
	settings = models.ForeignKey(TypeSettings, on_delete=models.CASCADE)
	slug = models.SlugField()
	icon = models.CharField(max_length=20)
	promotional_sliders = models.ManyToManyField(PromotionalSliders, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	banners = models.ManyToManyField(Banners)

	def __str__(self):
		return self.name 

	def get_absolute_url(self):
		return reverse('types-detail', kwargs={'slug':self.slug})

	class Meta:
		verbose_name_plural = 'Types'
		

class ShopImage(models.Model):
	name = models.CharField(max_length=200)
	original = models.ImageField()
	thumbnail = models.ImageField()

	def __str__(self):
		return self.name

	@property
	def imageURL(self):
		try:
			url = self.original.url
		except:
			url = ''
		return url

class Address(models.Model):
	zip = models.CharField(max_length=200)
	city = models.CharField(max_length=200)
	state = models.CharField(max_length=200)
	country = models.CharField(max_length=200)
	street_address = models.CharField(max_length=200)

	class Meta:
		verbose_name_plural = 'User Addresses'

	def __str__(self):
		return self.street_address

class CreateAddress(models.Model):
	customer_id = models.IntegerField(null=True, blank=True)
	title = models.CharField(max_length=200)
	BILLING = 'billing'
	SHIPPING = 'shipping'
	Type = [
		(BILLING, 'Billing'),
		(SHIPPING, 'Shipping'),
	]
	type = models.CharField(max_length=200, choices=Type)
	default = models.BooleanField(null=True, blank=True)
	address = models.ForeignKey(Address, on_delete=models.CASCADE)

	def __str__(self):
		return self.title

	class Meta:
		verbose_name_plural = 'Create Addresses'

	def __str__(self):
		return self.street_address



class ShopLocation(models.Model):
	lat = models.FloatField()
	lng = models.FloatField()
	city = models.CharField(max_length=200)
	state = models.CharField(max_length=200)
	country = models.CharField(max_length=200)
	formattedAddress = models.CharField(max_length=200)

	def __str__(self):
		return self.formattedAddress


class ShopSettings(models.Model):
	name = models.CharField(max_length=200)
	contact = models.CharField(max_length=20)
	socials = models.ManyToManyField(Socials)
	website = models.CharField(max_length=20)
	location = models.ForeignKey(ShopLocation, on_delete=models.CASCADE)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = 'ShopSettings'

class Profile(models.Model):
	avatar = models.ForeignKey(ShopImage, on_delete=models.CASCADE, null=True, blank=True)
	bio = models.TextField(null=True, blank=True)
	socials = models.ForeignKey(Socials, null=True, blank=True, on_delete=models.CASCADE)
	contact = models.CharField(max_length=20, null=True, blank=True)
	customer_id = models.IntegerField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.id)


class ShopOwner(models.Model):
	name = models.CharField(max_length=200)
	email = models.EmailField()
	email_verified_at = models.DateTimeField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	is_active = models.IntegerField(default=1)
	shop_id = models.IntegerField(null=True, blank=True)
	profile = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)

	def __str__(self):
		return self.name

class Shop(models.Model):
	ownerId = models.IntegerField()
	name = models.CharField(max_length=200)
	slug = models.SlugField(max_length=200)
	description = models.TextField()
	cover_image = models.ForeignKey(ShopImage, on_delete=models.CASCADE)
	logo = models.ForeignKey(Logo, on_delete=models.CASCADE)
	is_active = models.IntegerField()
	address = models.ForeignKey(Address, on_delete=models.CASCADE)
	settings = models.ForeignKey(ShopSettings, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	orders_count = models.IntegerField(null=True, blank=True)
	products_count = models.IntegerField(null=True, blank=True)
	owner = models.ForeignKey(ShopOwner, null=True, blank=True, on_delete=models.CASCADE)


	def __str__(self):
		return self.name


class ProductImage(models.Model):
	name = models.CharField(max_length=200)
	original = models.ImageField()
	thumbnail = models.ImageField(null=True, blank=True)

	def __str__(self):
		return self.name

	
	class Meta:
		ordering = ['pk']

	@property
	def imageURL(self):
		try:
			url = self.original.url
		except:
			url = ''
		return url


class ProductGallery(models.Model):
	name = models.CharField(max_length=200)
	images = models.ManyToManyField(ProductImage)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = 'ProductGalleries'


class CategoryPivot(models.Model):
	product_id = models.IntegerField()
	category_id = models.IntegerField()

	def __str__(self):
		return str(self.product_id)


# class Children(models.Model):
# 	name = models.CharField(max_length=200, null=True, blank=True)
# 	slug = models.CharField(max_length=200, null=True, blank=True)
# 	icon = models.CharField(max_length=200, blank=True, null=True)
# 	details = models.TextField(null=True, blank=True)
# 	parent = models.ForeignKey('Categories', related_name='+', null=True, blank=True, on_delete=models.CASCADE)
# 	type_id = models.IntegerField()
# 	created_at = models.DateTimeField(auto_now_add=True)
# 	updated_at = models.DateTimeField(auto_now=True)
# 	deleted_at = models.DateTimeField(null=True, blank=True)
# 	products_count = models.IntegerField(null=True, blank=True)
# 	parentId = models.IntegerField(null=True, blank=True)
# 	children = models.ManyToManyField('self', blank=True)

# 	def __str__(self):
# 		return self.name

# 	class Meta:
# 		verbose_name_plural = 'Children'

class Categories(models.Model):
	name = models.CharField(max_length=200)
	slug = models.SlugField()
	icon = models.CharField(max_length=20,null=True, blank=True)
	image = models.ManyToManyField(ProductImage, blank=True)
	details = models.TextField(null=True, blank=True)
	parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
	typeId = models.IntegerField(null=True, blank=True)
	parentId = models.IntegerField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
	deleted_at = models.DateTimeField(null=True, blank=True)
	type = models.ForeignKey(Types, on_delete=models.CASCADE, blank=True, null=True)
	children = models.ManyToManyField('self', blank=True)
	products_count = models.IntegerField(null=True, blank=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = 'Categories'

class Attachment(models.Model):
	original = models.ImageField(null=True, blank=True)
	thumbnail = models.ImageField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.id)

class Tag(models.Model):
	name = models.CharField(max_length=200)
	slug = models.CharField(max_length=200)
	parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
	details = models.TextField(null=True, blank=True)
	image = models.ManyToManyField(Attachment, blank=True)
	icon = models.CharField(max_length=50, null=True, blank=True)
	type = models.ForeignKey(Types, on_delete=models.CASCADE, null=True, blank=True)
	products = models.ManyToManyField('Product', blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

	def __str__(self):
		return self.name


class VariationOption(models.Model):
	name = models.CharField(max_length=100)
	value = models.CharField(max_length=100)

	def __str__(self):
		return self.name


class Variation(models.Model):
	title = models.CharField(max_length=200)
	price = models.IntegerField()
	sku = models.CharField(max_length=100, null=True, blank=True)
	is_disable = models.BooleanField(null=True, blank=True)
	sale_price = models.IntegerField(null=True, blank=True)
	quantity = models.IntegerField(null=True, blank=True)
	options = models.ForeignKey(VariationOption, on_delete=models.CASCADE)

	def __str__(self):
		return self.title


class Product(models.Model):
	name = models.CharField(max_length=200)
	slug = models.SlugField(max_length=200, null=True, unique=True, editable=False)
	description = models.TextField(blank=True, null=True)
	price = models.FloatField(null=True)
	sales_price = models.FloatField(blank=True, null=True)
	sku = models.CharField(max_length=200, null=True, blank=True)
	quantity = models.IntegerField(null=True)
	in_stock = models.BooleanField(blank=True, null=True, default=True)
	is_taxable = models.BooleanField(null=True, blank=True, default=False)
	is_digital = models.BooleanField(null=True, blank=True, default=False)
	is_external = models.BooleanField(null=True, blank=True, default=False)
	external_product_url = models.CharField(max_length=200, null=True, blank=True)
	external_product_button_text = models.CharField(max_length=200, null=True, blank=True)
	shipping_class_id = models.IntegerField(null=True, blank=True)
	digital_file = models.ForeignKey('DigitalFile', on_delete=models.CASCADE, null=True, blank=True)

	PUBLISH = 'publish'
	DRAFT = 'draft'
	ProductStatus = [
		(PUBLISH, 'Publish'),
		(DRAFT, 'Draft'),
	]
	status = models.CharField(max_length=200, choices=ProductStatus, default=PUBLISH)

	SIMPLE = 'simple'
	VARIABLE = 'variable'
	ProductType = [
		(SIMPLE, 'Simple'),
		(VARIABLE, 'Variable'),
	]
	product_type = models.CharField(max_length=200, choices=ProductType, default=SIMPLE)

	unit = models.CharField(max_length=15, blank=True, null=True)
	height = models.FloatField(null=True, blank=True)
	width = models.FloatField(null=True, blank=True)
	length = models.FloatField(null=True, blank=True)
	image = models.ForeignKey(ProductImage, null=True, on_delete=models.CASCADE)
	gallery = models.ForeignKey(ProductGallery, on_delete=models.CASCADE, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
	max_price = models.FloatField(null=True, blank=True)
	min_price = models.FloatField(null=True, blank=True)
	type = models.ForeignKey(Types, null=True, on_delete=models.CASCADE)
	shop = models.ForeignKey(Shop, null=True, on_delete=models.CASCADE)
	categories = models.ManyToManyField(Categories)
	tags = models.ManyToManyField(Tag, blank=True)
	variations = models.ManyToManyField('AttributeValue', blank=True)
	variation_options = models.ManyToManyField(Variation, blank=True)
	pivot = models.ForeignKey('OrderProductPivot', null=True, blank=True, on_delete=models.CASCADE)
	orders = models.ManyToManyField('Order', blank=True)
	# related_products = models.ManyToManyField('self', blank=True)
	manufacturer = models.ForeignKey('Manufacturer', null=True, blank=True, on_delete=models.CASCADE)


	def __str__(self):
		return self.name
	
	def save(self, *args, **kwargs):
		if not self.slug:
			value = self.name
			self.slug = slugify(value, allow_unicode=True)
			super().save(*args, **kwargs)

	class Meta:
		ordering = ['pk']

class Status(models.Model):
	name = models.CharField(max_length=200)
	serial = models.IntegerField(null=True, blank=True)
	color = models.CharField(max_length=10)
	created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

	def __str__(self):
		return self.name
		
def random_string():
	unique_id =  get_random_string(length=10)
	return unique_id


class Order(models.Model):
	tracking_number = models.CharField(max_length=15, default=random_string, null=True, blank=True)
	customer_contact = models.CharField(max_length=15, null=True)
	status = models.CharField(blank=True, null=True, max_length=10)
	amount = models.FloatField(null=True)
	address = models.ForeignKey(Address, null=True, blank=True, on_delete=models.CASCADE)
	sales_tax = models.FloatField(null=True)
	paid_total = models.FloatField(null=True)
	total = models.FloatField(null=True)
	coupon = models.ForeignKey('Coupon', on_delete=models.CASCADE, blank=True, null=True)
	parent_order = models.ForeignKey('self', related_name='+', blank=True, on_delete=models.SET_NULL, null=True)
	shop = models.ForeignKey(Shop, on_delete=models.CASCADE, blank=True, null=True)
	discount = models.FloatField(null=True)
	payment_id = models.IntegerField(null=True)

	STRIPE = 'STRIPE'
	CASH_ON_DELIVERY = 'CASH_ON_DELIVERY'
	CASH = 'CASH'
	FULL_WALLET_PAYMENT = 'FULL_WALLET_PAYMENT'

	PaymentGatewayType = [
		(STRIPE, 'stripe'),
		(CASH_ON_DELIVERY, 'cod'),
		(CASH, 'Cash'),
		(FULL_WALLET_PAYMENT, 'Full Wallet Payment'),
	]

	payment_gateway = models.CharField(max_length=200, choices=PaymentGatewayType, null=True, blank=True)
	logistics_provider = models.CharField(max_length=200, null=True, blank=True)
	delivery_fee = models.FloatField(null=True)
	delivery_time = models.CharField(max_length=200,null=True,blank=True)
	deleted_at = models.DateTimeField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
	customer = models.ForeignKey('User', on_delete=models.CASCADE, null=True,blank=True)
	products = models.ManyToManyField(Product)
	children = models.ManyToManyField('self', blank=True)
	card = models.ForeignKey('CardInput', null=True, blank=True, on_delete=models.SET_NULL)

	def __str__(self):
		return str(self.id)

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True,blank=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total

class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address


class Snippet(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	title =  models.CharField(max_length=100, blank=True, default='')
	code = models.TextField()
	linenos = models.BooleanField(default=False)


class Token(models.Model):
	email = models.CharField(max_length=200, null=True, blank=True)
	password = models.CharField(max_length=20, null=True, blank=True)

	def __str__(self):
		return self.name

class AccountManager(BaseUserManager):

    def create_superuser(self, email, username, name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, username, name, password, **other_fields)

    def create_user(self, email, username, name, password, **other_fields):

        if not email:
            raise ValueError('You must provide an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username,
                          name=name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
	def defaultPermission():
		default = Permissions.objects.filter(id=1)
		return default

	email = models.EmailField(unique=True,blank=True)
	username = models.CharField(max_length=150, unique=True,blank=True)
	name = models.CharField(max_length=150, blank=True)
	start_date = models.DateTimeField(default=timezone.now)
	shop_id = models.IntegerField(blank=True, null=True)
	profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
	permissions = models.ManyToManyField('Permissions', default=defaultPermission, blank=True)
	is_staff = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	email_verified_at = models.DateTimeField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
	updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)
	
	objects = AccountManager()
	
	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['name', 'email']

	def __str__(self):
		return self.username



class UserAddress(models.Model):
	title = models.CharField(max_length=200)
	type = models.CharField(max_length=200)
	default = models.IntegerField(default=0)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='address', null=True, blank=True)
	address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
	customer_id = models.IntegerField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

	class Meta:
		verbose_name_plural = 'User Addresses'

	def __str__(self):
		return self.title




class Permissions(models.Model):
	name = models.CharField(max_length=200)
	guard_name = models.CharField(max_length=200,null=True,blank=True)
	created_at = models.DateTimeField(auto_now_add=True,null=True)
	updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)

	class Meta:
		verbose_name_plural = 'Permissions'

	def __str__(self):
		return self.name

class AuthResponse(models.Model):
	token = models.CharField(max_length=200, null=True)
	permissions = models.ManyToManyField(Permissions, blank=True)

	def __str__(self):
		return self.token


class PasswordChangeResponse(models.Model):
	success = models.BooleanField(null=True)
	message = models.TextField(null=True, blank=True)

	def __str__(self):
		return self.message

class OtpResponse(models.Model):
	id = models.CharField(primary_key=True, max_length=200)
	message = models.TextField(null=True, blank=True)
	success = models.BooleanField(null=True)
	phone_number = models.CharField(max_length=100, blank=True, null=True)
	provider = models.CharField(max_length=20, blank=True, null=True)
	is_contact_exist = models.BooleanField(null=True)

	def __str__(self):
		return str(self.id)


class Register(models.Model):
	name = models.CharField(max_length=200, null=True, blank=True)
	email = models.CharField(max_length=200, null=True, blank=True)
	password = models.CharField(max_length=20, null=True, blank=True)
	permission = models.CharField(max_length=200, default='CUSTOMER')

	def __str__(self):
		return self.name


class Me(models.Model):
	is_active = models.IntegerField(default=1, blank=True, null=True)
	name =  models.CharField(max_length=200)
	email = models.EmailField()
	email_verified_at = models.DateField(blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
	shop_id = models.IntegerField(default=1, blank=True, null=True)
	profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
	address = models.ManyToManyField(UserAddress, blank=True)
	permissions = models.ManyToManyField(Permissions)
	
	class Meta:
		verbose_name_plural = 'Me'

	def __str__(self):
		return self.name
	

class OrderStatus(models.Model):
	name = models.CharField(max_length=200)
	serial = models.IntegerField()
	color = models.CharField(max_length=20)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name_plural = 'Order Statuses'

	def __str__(self):
		return self.name


class SocialLoginToken(models.Model):
	provider = models.CharField(max_length=200)
	access_token = models.TextField()

	def __str__(self):
		return self.provider

class Author(models.Model):
	name = models.CharField(max_length=200)
	is_approved = models.BooleanField(default=False)
	image = models.ForeignKey(Attachment, on_delete=models.CASCADE, null=True, blank=True)
	cover_image = models.ForeignKey(Attachment, related_name="+", on_delete=models.CASCADE, null=True, blank=True)
	slug = models.CharField(max_length=200)
	bio = models.TextField(null=True, blank=True)
	born = models.DateTimeField(null=True, blank=True)
	death = models.DateTimeField(null=True, blank=True)
	languages = models.CharField(max_length=200)
	socials = models.ManyToManyField(Socials, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	products_count = models.IntegerField(null=True, blank=True)


class Manufacturer(models.Model):
	name = models.CharField(max_length=200)
	is_approved = models.BooleanField(default=False)
	image = models.ForeignKey(Attachment, on_delete=models.CASCADE, null=True, blank=True)
	cover_image = models.ForeignKey(Attachment, related_name='+', on_delete=models.CASCADE, blank=True, null=True)
	slug = models.CharField(max_length=200, null=True, blank=True)
	type = models.CharField(max_length=200,null=True, blank=True)
	description = models.TextField(null=True, blank=True)
	website = models.CharField(max_length=200,null=True,blank=True)
	socials = models.ManyToManyField(Socials,blank=True)
	created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
	updated_at = models.DateTimeField(auto_now=True)
	products_count = models.IntegerField

	def __str__(self):
		return self.name

class Coupon(models.Model):
	code = models.CharField(max_length=100)
	description = models.TextField(null=True,blank=True)
	image = models.ForeignKey(Attachment, on_delete=models.CASCADE, null=True, blank=True)
	type = models.ForeignKey(Types,on_delete=models.CASCADE,null=True,blank=True)
	amount = models.IntegerField(null=True,blank=True)
	active_from = models.DateTimeField(null=True,blank=True)
	expire_at = models.DateTimeField(null=True,blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	deleted_at = models.DateTimeField(null=True,blank=True)
	is_valid = models.BooleanField(null=True,blank=True)

	def __str__(self):
		return self.code

class VerifiedCheckoutData(models.Model):
	total_tax = models.FloatField(null=True,blank=True)
	shipping_charge = models.IntegerField(null=True, blank=True)
	unavailable_products = models.ManyToManyField(Product,blank=True)
	wallet_currency = models.IntegerField(null=True, blank=True)
	wallet_amount = models.IntegerField(null=True, blank=True)

	def __str__(self):
		return str(self.id)


class OrderProductPivot(models.Model):
	order_id = models.IntegerField(null=True, blank=True)
	product_id = models.IntegerField(null=True, blank=True)
	variation_option_id = models.IntegerField(null=True, blank=True)	
	order_quantity = models.IntegerField(null=True, blank=True)
	unit_price = models.FloatField(null=True, blank=True)
	subtotal = models.FloatField(null=True, blank=True)

class ConnectProductOrderPivot(models.Model):
	product_id = models.IntegerField(null=True)
	variation_option_id = models.IntegerField(null=True)
	order_quantity = models.IntegerField(null=True)
	unit_price = models.FloatField(null=True)
	subtotal = models.FloatField(null=True)

	def __str__(self):
		return str(self.id)


class DigitalFile(models.Model):
	created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
	attachment =models.ForeignKey(Attachment, on_delete=models.CASCADE, null=True, blank=True)
	fileable = models.BooleanField(null=True, blank=True)
	url = models.URLField(blank=True, null=True)

class WalletPoint(models.Model):
	amount = models.FloatField(null=True, blank=True)

class Refund(models.Model):
	title = models.CharField(max_length=200, null=True)
	description = models.CharField(max_length=200, null=True, blank=True)
	images = models.ManyToManyField(Attachment, blank=True)
	amount = models.CharField(max_length=200, null=True, blank=True)

	APPROVED = 'APPROVED'
	PENDING = 'PENDING'
	REJECTED = 'REJECTED'
	PROCESSING = 'PROCESSING'
	RefundStatus = [
		(APPROVED, 'Approved'),
		(PENDING, 'Pending'),
		(REJECTED, 'Rejected'),
		(PROCESSING, 'Processing'),
	]

	status = models.CharField(max_length=200, choices=RefundStatus)

	shop = models.ForeignKey(Shop, on_delete=models.CASCADE, blank=True, null=True)
	order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
	customer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, null=True)

class Attribute(models.Model):
	name = models.CharField(max_length=200, null=True)
	shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True, blank=True)
	slug = models.CharField(max_length=200, null=True, blank=True)
	values = models.ManyToManyField('AttributeValue', blank=True)
	created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name



class AttributeValue(models.Model):
	created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
	shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True, blank=True)
	value = models.CharField(max_length=200, null=True, blank=True)
	meta = models.CharField(max_length=200, null=True, blank=True)

	def __str__(self):
		return self.value 


class CardInput(models.Model):
	number = models.CharField(max_length=200, null=True)
	expriryMonth = models.CharField(max_length=200, null=True)
	expiryYear = models.CharField(max_length=200, null=True)
	cvv = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)