"""gurushop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from unicodedata import name
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from rest_framework import routers
from store import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

router = routers.DefaultRouter()
router.register(r'products', views.ProductsViewSet, 'products')
# popular products 
router.register(r'categories', views.CategoriesViewSet, 'categories')
router.register(r'types', views.TypesViewSet)
router.register(r'tags', views.TagViewSet) 
router.register(r'shops', views.ShopViewSet)
router.register(r'authors', views.AuthorViewSet)
# top authors 
router.register(r'manufacturers', views.ManufacturerViewSet)
# top manufacturers 
router.register(r'coupons', views.CouponViewSet)
# coupons verify
router.register(r'orders', views.OrderViewSet)
router.register(r'order-status', views.OrderStatusViewSet)
# refunds 
router.register(r'orders/checkout/verify', views.VerifiedCheckoutDataViewSet)
# downloads 
# downloads digital file
router.register(r'users', views.UserViewSet)
router.register(r'adress', views.UserAddressViewSet)
# user me -- Done below
# token -- Done below 
# user register -- Done below 
# forgot password 
# verify forget password 
# change password 
# user logout -- Done below 
# subscribe to newsletter 
# contact us 
# social login token 
# verify otp code 
# otp login 
# update contact 
router.register(r'settings', views.SettingsViewSet, 'settings')
router.register(r'attachments', views.AttachmentViewSet)
router.register(r'order-pivot', views.OrderPivot)




urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls,)),
    path('api/user/', include('store.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_refresh'),
    path('users/', include('users.urls')),
    path('', include('dashboard.urls')),
    path('store/', include('store.urls')),
    path('accounts/', include('allauth.urls')),
    path('api-auth/', include('rest_framework.urls')),
    #path('account/', include('django.contrib.auth.urls')),
    path('password_reset/done', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)