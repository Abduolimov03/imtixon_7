from django.urls import path
from .views import CardCreate, AddToCard, CardItemUpdate

urlpatterns = [
    path('get-create/', CardCreate.as_view()),
    path('add-to-card/', AddToCard.as_view()),
    path('card-item/update/<int:pk>/', CardItemUpdate.as_view()),

]