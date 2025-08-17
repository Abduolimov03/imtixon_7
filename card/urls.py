from django.urls import path
from .views import CardCreate, AddToCard, CardItemUpdate, card_detail, card_clear, card_remove_item

urlpatterns = [
    path('get-create/', CardCreate.as_view()),
    path('add-to-card/', AddToCard.as_view()),
    path('card-item/update/<int:pk>/', CardItemUpdate.as_view()),
    path('card/', card_detail, name='card-detail'),
    path('card/remove/', card_remove_item, name='cart-remove'),
    path('card/clear/', card_clear, name='cart-clear'),

]