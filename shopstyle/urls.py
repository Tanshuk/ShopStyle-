"""
Root URL configuration for ShopStyle.
Every app has its own urls.py; we include them here with a namespace.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Customise the admin panel header
admin.site.site_header  = 'ShopStyle Administration'
admin.site.site_title   = 'ShopStyle Admin'
admin.site.index_title  = 'Welcome to ShopStyle Dashboard'

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),

    # Our apps
    path('',            include('apps.core.urls',      namespace='core')),
    path('accounts/',   include('apps.accounts.urls',  namespace='accounts')),
    path('products/',   include('apps.products.urls',  namespace='products')),
    path('cart/',       include('apps.cart.urls',      namespace='cart')),
    path('wishlist/',   include('apps.wishlist.urls',  namespace='wishlist')),
    path('orders/',     include('apps.orders.urls',    namespace='orders')),
    path('payments/',   include('apps.payments.urls',  namespace='payments')),
    path('reviews/',    include('apps.reviews.urls',   namespace='reviews')),
    path('dashboard/',  include('apps.dashboard.urls', namespace='dashboard')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)