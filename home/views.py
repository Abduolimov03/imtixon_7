from django.shortcuts import render
from django.core.serializers import serialize
from django.template.defaulttags import comment
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from django.db.models import Q
from .models import Kompyuter, Comment
from .serializers import KompyuterSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser



class CommentCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        kompyuter = get_object_or_404(Kompyuter, id=pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, kompyuter=kompyuter)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        kompyuter = get_object_or_404(Kompyuter, id=pk)
        if request.user.is_superuser:
            comments = kompyuter.comments.all()
        else:
            comments = kompyuter.comments.filter(user=request.user)

        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CommentDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        comment = get_object_or_404(Comment, id=pk)

        if not request.user.is_superuser and comment.user != request.user:
            return Response({
                'err': 'Siz bu sharhni ko‘ra olmaysiz',
                'status': status.HTTP_403_FORBIDDEN
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = CommentSerializer(comment)
        return Response({'data': serializer.data, 'status': status.HTTP_200_OK})

class CommentUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        comment = get_object_or_404(Comment, id=pk)

        if comment.user != request.user:
            return Response({
                'err': 'Siz faqat o‘z sharhingizni o‘zgartira olasiz',
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'err': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        comment = get_object_or_404(Comment, id=pk)

        if comment.user != request.user:
            return Response({
                'err': 'Siz faqat o‘z sharhingizni o‘zgartira olasiz',
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = CommentSerializer(instance=comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'err': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CommentDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        comment = get_object_or_404(Comment, id=pk)

        if comment.user != request.user:
            return Response({
                'error': 'Siz faqat oz sharhingizni ochira olasiz',
                'status': status.HTTP_400_BAD_REQUEST
            })

        comment.delete()
        return Response({'message': 'Sharh ochirildi', 'status': status.HTTP_200_OK})







#### CRUD
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def komp_list(request):
    kompyuters = Kompyuter.objects.all()

    category = request.GET.get('category')
    if category:
        kompyuters = kompyuters.filter(category__name=category)

    search = request.GET.get('search')
    if search:
        kompyuters = kompyuters.filter(
            Q(brand__icontains=search) | Q(model__icontains=search)
        )

    price_gt = request.GET.get('price_gt')
    if price_gt:
        kompyuters = kompyuters.filter(price__gt=price_gt)

    price_lt = request.GET.get('price_lt')
    if price_lt:
        kompyuters = kompyuters.filter(price__lt=price_lt)

    ordering = request.GET.get('ordering')
    if ordering:
        kompyuters = kompyuters.order_by(ordering)

    paginator = LimitOffsetPagination()
    paginator.page_size = 2
    paginated_kompyuter = paginator.paginate_queryset(kompyuters, request)

    serializer = KompyuterSerializer(paginated_kompyuter, many=True)
    data = {
        'data': serializer.data,
        'count': len(kompyuters),
        'status': status.HTTP_200_OK
    }
    return paginator.get_paginated_response(data)



@api_view(['POST'])
@permission_classes([IsAdminUser])
def kompyuter_create(request):
    serializer = KompyuterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'status': status.HTTP_200_OK})
    return Response({'status': status.HTTP_400_BAD_REQUEST, 'err': serializer.errors})



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def kompyuter_detail(request, pk):
    try:
        kompyuter = Kompyuter.objects.get(id=pk)
    except Kompyuter.DoesNotExist:
        return Response({'status': status.HTTP_400_BAD_REQUEST})
    serializer = KompyuterSerializer(kompyuter)
    data = {
        'data': serializer.data,
        'status': status.HTTP_200_OK
    }
    return Response(data)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def kompyuter_update(request, pk):
    kompyuter = get_object_or_404(Kompyuter, id=pk)

    if not request.user.is_superuser:
        return Response({'detail': 'Sizda ruxsat yo‘q!'}, status=status.HTTP_403_FORBIDDEN)

    serializer = KompyuterSerializer(instance=kompyuter, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'status': status.HTTP_200_OK, 'data': serializer.data})
    return Response({'status': status.HTTP_400_BAD_REQUEST, 'err': serializer.errors})


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def kompyuter_delete(request, pk):
    try:
        kompyuter = Kompyuter.objects.get(id=pk)
    except Kompyuter.DoesNotExist:
        return Response({'status': status.HTTP_400_BAD_REQUEST})
    kompyuter.delete()
    return Response({'status': status.HTTP_200_OK})
