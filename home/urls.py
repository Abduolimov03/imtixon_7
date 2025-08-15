from django.urls import path
from .views import komp_list, kompyuter_delete, kompyuter_detail, kompyuter_update, kompyuter_create

urlpatterns = [
    path('kompyuters/', komp_list, name='kompyuter_list'),
    path('kompyuter/create/', kompyuter_create, name='kompyuter_create'),
    path('kompyuter/<int:pk>/detail/', kompyuter_detail, name='kompyuter_detail'),
    path('kompyuter/<int:pk>/delete/', kompyuter_delete, name='kompyuter_delete'),
    path('kompyuter/<int:pk>/update/', kompyuter_update, name='kompyuter_update'),
]