from django.shortcuts import render, get_object_or_404
from django.core.serializers import serialize
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import  Response
from home.models import Kompyuter
from .serializers import OrderSerializer, OrderItemSerializer
from .models import Order, OrderItem
from user_acc.user_perm import IsUser
from card.models import Card, CardItem
from rest_framework.permissions import IsAdminUser





class OrderCreate(APIView):
    permission_classes = [IsUser, ]

    def post(self, request):
        card = get_object_or_404(Card, user=request.user)
        if not card.items.exists():
            return Response({'error':'Bosh card', 'status':status.HTTP_400_BAD_REQUEST})

        order = Order.objects.create(user = request.user)
        for item in card.items.all():
            OrderItem.objects.create(
                order=order,
                kompyuter=item.kompyuter,
                ammount=item.ammount,
                price = item.kompyuter.price
            )


        card.items.all().delete()
        return Response({'message':'order yaratildi', 'status':status.HTTP_201_CREATED})



class OrderList(APIView):
    permission_classes = [IsUser, ]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-id')
        serializer = OrderSerializer(orders, many=True)
        return Response(
            {'data': serializer.data},
            status=status.HTTP_200_OK
        )

class OrderDetail(APIView):
    permission_classes = [IsUser, ]

    def get(self, request, pk):
        order = get_object_or_404(Order, id=pk, user=request.user)
        serializer = OrderSerializer(order)
        return Response({
            'data': serializer.data,
            'status': status.HTTP_200_OK
        })


class OrderStatusUpdate(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, pk):
        order = get_object_or_404(Order, id=pk)

        new_status = request.data.get("status")
        valid_statuses = [choice[0] for choice in Order.STATUS_CHOISE]

        if new_status not in valid_statuses:
            return Response({
                "error": f"Status '{new_status}' noto‘g‘ri. Faqat {valid_statuses} dan foydalaning.",
                "status": status.HTTP_400_BAD_REQUEST
            })

        order.status = new_status
        order.save()

        serializer = OrderSerializer(order)
        return Response({
            "message": "Buyurtma statusi yangilandi",
            "data": serializer.data,
            "status": status.HTTP_200_OK
        })


class OrderDelete(APIView):
    permission_classes = [IsUser, ]
    def delete(self, request, pk):
        order = get_object_or_404(Order, id=pk, user=request.user)
        order.delete()
        return Response(
            {'message': 'Order ochirildi'},
            status=status.HTTP_200_OK
        )
