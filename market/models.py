from django.db import models
from django.utils import timezone

class Item(models.Model):
    # TODO use foreign keys
    # brand = models.ForeignKey(
    #     'item.Brand',
    #     on_delete=models.CASCADE,
    # )
    # type = models.ForeignKey(
    #     'item.Type',
    #     on_delete=models.CASCADE,
    # )
    # product = models.ForeignKey(
    #     'item.Brand.Product',
    #     on_delete=models.CASCADE,
    # )

    GENDER_CHOICES = (
        ('M', 'Mens'),
        ('W', 'Womens'),
        ('K', 'Kids'),
        ('U', 'Unisex'),
    )

    id = models.AutoField(primary_key=True)
    brand = models.TextField()
    type = models.TextField()
    product = models.TextField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
    )
    price = models.FloatField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.brand + self.type + self.product
