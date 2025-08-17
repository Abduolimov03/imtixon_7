from django.urls import path
from .views import komp_list, kompyuter_delete, kompyuter_detail, kompyuter_update, kompyuter_create, CommentCreateAPIView, CommentListAPIView, CommentUpdateAPIView, CommentDeleteAPIView, CommentDetailAPIView


urlpatterns = [
    path('kompyuters/', komp_list, name='kompyuter_list'),
    path('kompyuter/create/', kompyuter_create, name='kompyuter_create'),
    path('kompyuter/<int:pk>/detail/', kompyuter_detail, name='kompyuter_detail'),
    path('kompyuter/<int:pk>/delete/', kompyuter_delete, name='kompyuter_delete'),
    path('kompyuter/<int:pk>/update/', kompyuter_update, name='kompyuter_update'),
    path('kompyuter/<int:pk>/comments/', CommentListAPIView.as_view(), name='comment-list'),
    path('kompyuter/<int:pk>/comment/detail/', CommentDetailAPIView.as_view(), name='comment-detail'),
    path('kompyuter/<int:pk>/comments/create/', CommentCreateAPIView.as_view(), name='comment-create'),
    path('kompyuter/comments/<int:pk>/update/', CommentUpdateAPIView.as_view(), name='comment-update'),
    path('kompyuter/comments/<int:pk>/delete/', CommentDeleteAPIView.as_view(), name='comment-delete'),

]