import imp
from django.contrib.auth.models import User, Group
from django.shortcuts import render
from .models import *
from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend,FilterSet
from .serializers import *
from .paginations import CustomPagination
from django_filters import CharFilter, NumberFilter, BooleanFilter

# Create your views here.
class UserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoadUserView(APIView):
    def get(self, request, format=None):
        try:
            user = request.user
            user = UserSerializer(user)

            return Response(
                user.data,
                status=status.HTTP_200_OK
            )


        except:
            return Response(
                {'error':'Something went wrong when trying to load user'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LogoutView(APIView):
    def post(self, request):
       return Response('true')

class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ProductFilter(FilterSet):
    categories = CharFilter(field_name='categories__slug', lookup_expr='iexact')
    type = CharFilter(field_name='type__slug', lookup_expr='iexact')
    name = CharFilter(field_name='name', lookup_expr='icontains')
    shop_id = NumberFilter(field_name='shop_id', lookup_expr='exact')

    class Meta:
        model = Product
        fields = ['categories']


class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    # serializer_class = ProductWithRelatedSerializer
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    search_fields = ['type__slug','categories__slug']
    # filterset_fields = ['categories__slug']
    filterset_class = ProductFilter

class CategoryFilter(FilterSet):
    parent_id__isnull = BooleanFilter(field_name='parent_id', lookup_expr='isnull')

    class Meta:
        model = Categories
        fields = {
            'name': ['icontains'],
            'slug': ['exact'],
            }

class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['type__slug']
    # filterset_fields = ['name','slug']
    filterset_class = CategoryFilter
    
class TypesViewSet(viewsets.ModelViewSet):
    queryset = Types.objects.all()
    serializer_class = TypesSerializer
    lookup_field = 'slug'

class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    lookup_field = 'slug'
    pagination_class = CustomPagination

class ShopSettingsViewSet(viewsets.ModelViewSet):
    queryset = ShopSettings.objects.all()
    serializer_class = ShopSettingsSerializer

class ShopLocationViewSet(viewsets.ModelViewSet):
    queryset = ShopLocation.objects.all()
    serializer_class = ShopLocationSerializer

class ShopImageViewSet(viewsets.ModelViewSet):
    queryset = ShopImage.objects.all()
    serializer_class = ShopImageSerializer

class SettingsViewSet(viewsets.ModelViewSet):
    queryset = Settings.objects.filter(id=1)
    serializer_class = SettingsSerializer


class TypeSettingsViewSet(viewsets.ModelViewSet):
    queryset = TypeSettings.objects.all()
    serializer_class = TypeSettingsSerializer

class promo_sliders(viewsets.ModelViewSet):
    queryset = PromotionalSliders.objects.all()
    serializer_class = PromotionalSlidersSerializer

class banner_image(viewsets.ModelViewSet):
    queryset = BannerImage.objects.all()
    serializer_class = BannerImageSerializer

class banners(viewsets.ModelViewSet):
    queryset = Banners.objects.all()
    serializer_class = BannersSerializer

class SeoViewSet(viewsets.ModelViewSet):
    queryset = Seo.objects.all()
    serializer_class = SeoSerializer

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class OptionsViewSet(viewsets.ModelViewSet):
    queryset = Options.objects.all()
    serializer_class = OptionsSerializer

class ContactDetailsViewSet(viewsets.ModelViewSet):
    queryset = ContactDetails.objects.all()
    serializer_class = ContactDetailsSerializer

class DeliveryTimeViewSet(viewsets.ModelViewSet):
    queryset = DeliveryTime.objects.all()
    serializer_class = DeliveryTimeSerializer


class TokenViewSet(viewsets.ModelViewSet):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserAddressViewSet(viewsets.ModelViewSet):
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'tracking_number'
    pagination_class = CustomPagination


class RegisterViewSet(viewsets.ModelViewSet):
    queryset = Register.objects.all()
    serializer_class = RegisterSerializer


class PermissionsViewSet(viewsets.ModelViewSet):
    queryset = Permissions.objects.all()
    serializer_class = PermissionsSerializer


class AuthResponseViewSet(viewsets.ModelViewSet):
    queryset = AuthResponse.objects.all()
    serializer_class = AuthResponseSerializer


class PasswordChangeResponseViewSet(viewsets.ModelViewSet):
    queryset = PasswordChangeResponse.objects.all()
    serializer_class = PasswordChangeResponseSerializer


class OtpResponseViewSet(viewsets.ModelViewSet):
    queryset = OtpResponse.objects.all()
    serializer_class = OtpResponseSerializer

class MeViewSet(viewsets.ModelViewSet):
    queryset = Me.objects.all()
    serializer_class = MeSerializer
    pagination_class = None

class OrderStatusViewSet(viewsets.ModelViewSet):
    queryset = OrderStatus.objects.all()
    serializer_class = OrderStatusSerializer
    pagination_class = CustomPagination


class SocialLoginTokenViewSet(viewsets.ModelViewSet):
    queryset = SocialLoginToken.objects.all()
    serializer_class = SocialLoginTokenSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    pagination_class = CustomPagination

class ManufacturerViewSet(viewsets.ModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    pagination_class = CustomPagination


class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    pagination_class = CustomPagination

class VerifiedCheckoutDataViewSet(viewsets.ModelViewSet):
    queryset = VerifiedCheckoutData.objects.all()
    serializer_class = VerifiedCheckoutDataSerializer

class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer

class OrderProductPivotViewSet(viewsets.ModelViewSet):
    queryset = OrderProductPivot.objects.all()
    serializer_class = OrderProductPivotSerializer

class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer

class OrderPivot(viewsets.ModelViewSet):
    queryset = ConnectProductOrderPivot.objects.all()
    serializer_class = ConnectProductOrderPivotSerializer









