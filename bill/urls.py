"""
URL configuration for bill project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from billapp import views
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/',views.SignUpView.as_view(),name="signup"),
    path("",views.SignInView.as_view(),name="signin"),
    path("index/",views.index.as_view(),name="index"),
    path("company/detail/",views.CompanyDetailView.as_view(),name="company-detail"),
    path("generate/bill/",views.GenerateBillReceiptView.as_view(),name="generate-bill"),
    path("signout/",views.SignOutView.as_view(),name="signout"),
    path('item/<int:pk>/remove',views.ItemDeleteView.as_view(),name="delete"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
