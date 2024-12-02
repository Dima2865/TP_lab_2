from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('customers', views.customers_list, name='customers'),
    path('buy/<int:product_id>/', views.PurchaseCreate.as_view(), name='buy'),
]
