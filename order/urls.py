from django.urls import path
from .views import OrderCreate, OrderList, OrderDetail, OrderStatusUpdate, OrderDelete

urlpatterns = [
    path('get-create/', OrderCreate.as_view()),
    path('order-list/', OrderList.as_view()),
    path('order-detail/<int:pk>/', OrderDetail.as_view()),
    path('order-status/<int:pk>/', OrderStatusUpdate.as_view()),
    path('order-delete/<int:pk>/', OrderDelete.as_view()),

]