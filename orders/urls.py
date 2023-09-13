from django.urls import path
from . import views

urlpatterns=[

    path('cart/<int:id>', views.cart, name='cart'),
    path('order_history/', views.order_history, name='order_history'),
    path('order/', views.order, name='order'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('pay/', views.pay, name='pay'),
    path('delivery_manage/',views.delivery_manage,name='delivery_manage')
    

    
]