"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin

from django.urls import path
from django.conf.urls import include

from .rest import router, UserViewSet
from . import views as topical_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),

	path('api/', include(router.urls)),
	path('api/usersetup/', topical_views.setup_user, name = 'user_setup'),
	path('api/me/', UserViewSet.as_view({ 'get': 'me' }), name = 'me'),
	path('api/search/', topical_views.search_products, name='search_products'),
	path('api/ingredient/fuzzy/<str:fuzzy>/', topical_views.fuzzy_name, name = 'fuzzy_name'),
	path('api/product/notfound/<str:upc>/', topical_views.product_404, name = 'product-404')
]
