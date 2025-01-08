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
from billapp.views import ManageItemsView, generate_items_pdf,send_items_email


urlpatterns = [
   
    path('admin/', admin.site.urls),
   
    path('signup/',views.SignUpView.as_view(),name="signup"),
   
    path("signin/",views.SignInView.as_view(),name="signin"),
   
    path("signout/",views.SignOutView.as_view(),name="signout"),
    
    path("",views.LandingpageView.as_view(),name="landingpage"),

    path("index/",views.index.as_view(),name="index"),
   
    path("company/detail/",views.CompanyDetailView.as_view(),name="company-detail"),

    path("receiver/",views.ReceiverView.as_view(),name="receiver"),
   
    path("shipto/",views.Shipto.as_view(),name="shipto"),
   
    path("generate/bill/<int:pk>/",views.GenerateBillReceiptView.as_view(),name="generate-bill"),
    
    path("invoice/<int:pk>/",views.Invoice.as_view(),name="invoice"),
   
    path('delete-item/<int:pk>/<int:bill_id>/', views.ItemDeleteView.as_view(), name='delete-item'),   
   
    path('manage-items/pdf/<int:pk>/', generate_items_pdf, name='generate_items_pdf'),
   
    path('manage-items/email/<int:pk>/', send_items_email, name='send_items_email'),
    
    path('manage-items/', ManageItemsView.as_view(), name='manage_items'),

    path('add-to-save/<int:pk>/',views.SaveBillView.as_view(),name="add-to-save"),

    path('saved/', views.SavedBillSummaryView.as_view(), name='save_bill'),
   


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
