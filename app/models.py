from django.db import models

# Create your models here.
class Product(models.Model):
    no = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    price = models.FloatField()
    quantity = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.name
