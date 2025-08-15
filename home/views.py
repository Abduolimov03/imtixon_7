from django.shortcuts import render
from django.core.serializers import serialize
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.models import Q
from .models import Kompyuter
from .serializers import KompyuterSerializer
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


@api_view(['GET', ])
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
        'data':serializer.data,
        'count':len(kompyuters),
        'status':status.HTTP_200_OK
    }
    return paginator.get_paginated_response(data)

@api_view(['POST', ])
def kompyuter_create(request):
    serializer = KompyuterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'status':status.HTTP_200_OK})
    return Response({'status':status.HTTP_400_BAD_REQUEST})

@api_view(['GET', ])
def kompyuter_detail(request, pk):
    try:
        kompyuter = Kompyuter.objects.get(id=pk)
    except Kompyuter.DoesNotExist:
        return Response({'status':status.HTTP_400_BAD_REQUEST})
    serializer = KompyuterSerializer(kompyuter)
    data = {
        'data':serializer.data,
        'status':status.HTTP_200_OK
    }
    return Response(data)

@api_view(['PUT', ])
def kompyuter_update(request, pk):
    kompyuter = Kompyuter.objects.get(id=pk)
    serializer = KompyuterSerializer(kompyuter, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'status':status.HTTP_200_OK})
    return Response({'status':status.HTTP_400_BAD_REQUEST})

@api_view(['PATCH', ])
def kompyuter_update(request, pk):
    kompyuter = Kompyuter.objects.get(id=pk)
    serializer = KompyuterSerializer(kompyuter, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'status':status.HTTP_200_OK})
    return Response({'status':status.HTTP_400_BAD_REQUEST})

@api_view(['DELETE', ])
def kompyuter_delete(request, pk):
    try:
        kompyuter = Kompyuter.objects.get(id=pk)
    except Kompyuter.DoesNotExist:
        return Response({'status':status.HTTP_400_BAD_REQUEST})
    kompyuter.delete()
    return Response({'status':status.HTTP_200_OK})





