from django.core.serializers import serialize
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from home.models import Kompyuter
from .serializers import CardSerializer, CardItemSerializer
from .models import Card, CardItem
from user_acc.user_perm import IsUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes



class CardCreate(APIView):
    permission_classes = [IsUser, ]
    def post(self, request):
        card, created = Card.objects.get_or_create(user=request.user)
        serializer = CardSerializer(card)
        return Response({'data':serializer.data , "status":status.HTTP_201_CREATED if created else status.HTTP_200_OK })


class AddToCard(APIView):
    permission_classes = [IsUser, ]

    def post(self, request):
        kompyuter_id = request.data['kompyuter_id']
        ammount = int(request.data['ammount'])

        if not Kompyuter.objects.filter(id=kompyuter_id).exists():
            return Response({
                'error': 'Siz mavjud bo‘lmagan komyuterni tanladingiz',
                'status': status.HTTP_400_BAD_REQUEST
            })

        if ammount <= 0 or ammount > 100:
            return Response({
                'error': 'Siz xato ma’lumot kiritdingiz',
                'status': status.HTTP_400_BAD_REQUEST
            })

        card, _ = Card.objects.get_or_create(user=request.user)
        kompyuter_obj = Kompyuter.objects.get(id=kompyuter_id)

        card_item = CardItem.objects.filter(card=card, kompyuter=kompyuter_obj).first()

        if card_item:
            card_item.ammount += ammount
            card_item.save()
        else:
            card_item = CardItem.objects.create(
                card=card,
                kompyuter=kompyuter_obj,
                ammount=ammount
            )

        serializer = CardItemSerializer(card_item)

        return Response({
            'data': serializer.data,
            'status': status.HTTP_201_CREATED
        })

class CardItemUpdate(APIView):
    permission_classes = [IsUser, ]

    def post(self, request, pk):
        count = request.data.get('count', None)
        mtd = request.data.get('mtd', None)

        try:
            kompyuter = CardItem.objects.get(card__user=request.user, id=pk)
        except CardItem.DoesNotExist:
            return Response({'error': 'Card item topilmadi', 'status': status.HTTP_404_NOT_FOUND})

        if count is not None:
            kompyuter.ammount = int(count)
            kompyuter.save()

        elif mtd:
            if mtd == '+':
                kompyuter.ammount += 1
                kompyuter.save()

            elif mtd == '-':
                if kompyuter.ammount == 1:
                    kompyuter.delete()
                    return Response({
                        'msg': 'Item o‘chirildi',
                        'status': status.HTTP_200_OK
                    })
                else:
                    kompyuter.ammount -= 1
                    kompyuter.save()
        else:
            return Response({'error': 'Error', 'status': status.HTTP_400_BAD_REQUEST})

        serializer = CardItemSerializer(kompyuter)
        data = {
            'data': serializer.data,
            'status': status.HTTP_200_OK,
            'msg': 'Ozgartirildi'
        }
        return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def card_detail(request):
    try:
        cart = Card.objects.get(user=request.user)
    except Card.DoesNotExist:
        return Response({'detail': 'Sizning savatingiz bo‘sh'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CardSerializer(cart)
    return Response({'data': serializer.data, 'status': status.HTTP_200_OK})


@api_view(['POST'])
def card_remove_item(request):
    kompyuter_id = request.data.get('kompyuter_id')
    if not kompyuter_id:
        return Response({'error': 'kompyuter_id kerak'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        card = Card.objects.get(user=request.user)
    except Card.DoesNotExist:
        return Response({'error': 'Savat topilmadi'}, status=status.HTTP_404_NOT_FOUND)

    try:
        item = card.items.get(kompyuter_id=kompyuter_id)
        item.delete()
        return Response({'status': 'Mahsulot o‘chirildi'}, status=status.HTTP_200_OK)
    except CardItem.DoesNotExist:
        return Response({'error': 'Mahsulot savatda topilmadi'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def card_clear(request):
    try:
        card = Card.objects.get(user=request.user)
    except Card.DoesNotExist:
        return Response({'error': 'Savat topilmadi'}, status=status.HTTP_404_NOT_FOUND)

    card.items.all().delete()
    return Response({'status': 'Savat tozalandi'}, status=status.HTTP_200_OK)



