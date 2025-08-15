from django.db import models

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
    image = models.ImageField(upload_to='computer_images/', blank=True, null=True,default='computer_images/default.jpg'
)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return self.model