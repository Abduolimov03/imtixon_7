from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=120)
    desc = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Kompyuter(models.Model):
    brand = models.CharField(max_length=120)
    model = models.CharField(max_length=120)
    desc = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    image = models.ImageField(upload_to='computer_images/', blank=True, null=True,default='computer_images/default.jpg')

    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return self.model


class Comment(models.Model):
    kompyuter = models.ForeignKey(Kompyuter, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.user


