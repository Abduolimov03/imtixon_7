from django.db import models
from kompyuter.settings import AUTH_USER_MODEL
from home.models import Kompyuter

User = AUTH_USER_MODEL


class Card(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())


class CardItem(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='items')
    kompyuter = models.ForeignKey(Kompyuter, on_delete=models.CASCADE, blank=True, null=True)
    ammount = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.kompyuter.brand

    @property
    def total_price(self):
        return self.kompyuter.price * self.ammount