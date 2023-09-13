from django.urls import path
from . import views

 
urlpatterns = [
    path('', views.main, name='main'),
    path('signup_user/', views.signup_user, name='signup_user'),
    path('login_view/', views.login_view, name='login_view'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('update_user/',views.update_user,name='update_user'),
    path('category_admin/',views.category_admin,name='category-admin'),
    path('category_user/',views.category_user,name="category_user"),
    path('dishes_user/<int:id>/',views.dishes_user,name="dishes_user"),
    path('edit_category/<int:id>/', views.edit_category, name='edit_category'),
    path('delete_category/<int:id>/', views.delete_category, name='delete_category'),
    path('dishes_admin/<int:id>/', views.dishes_admin, name='dishes-admin'),
    path('edit_dish/<int:id>/', views.edit_dish, name='edit_dish'),
    path('delete_dish/<int:id>/', views.delete_dish, name='delete_dish'),
    path('add_category/', views.add_category, name='add_category'),
    path('add_dish/', views.add_dish, name='add-dish'),
    path('logout_user/',views.logout_user,name='logout_user'),
    path('logout_manager/',views.logout_manager,name='logout_manager')
]