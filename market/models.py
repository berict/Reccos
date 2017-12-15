import datetime

from django.db import models
from django.utils import timezone
from django_countries.fields import CountryField


class Item(models.Model):
    PAYMENT_CHOICES = (
        ('PP', 'PayPal'),
        ('PW', 'Paymentwall'),
        ('GW', 'Google Wallet'),
        ('BP', 'Bank payments'),
        ('OT', 'Other'),
    )
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    sold = models.IntegerField(default=0)

    payments = models.CharField(max_length=2, choices=PAYMENT_CHOICES, default='OT')
    price = models.FloatField()

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.brand + self.type + self.product


class Product(models.Model):
    BRAND_CHOICES = (
        ('AD', 'Adidas'),
        ('NI', 'Nike'),
        ('PU', 'Puma'),
        ('UM', 'Umbro'),
        ('NE', 'New Balance'),
        ('UN', 'Under Armour'),
        ('MI', 'Mizuno'),
        ('LO', 'Lotto'),
        ('JO', 'Joma'),
        ('AS', 'Asics'),
        ('CO', 'Concave'),
        ('DI', 'Diadora'),
        ('PA', 'Pantofola D\'Oro'),
        ('PE', 'Penalty'),
        ('WA', 'Warrior'),
        ('MI', 'Mitre'),
        ('OT', 'Other')
    )

    GENDER_CHOICES = (
        ('M', 'Mens'),
        ('W', 'Womens'),
        ('K', 'Kids'),
        ('U', 'Unisex'),
    )

    name = models.CharField(max_length=50)
    brand = models.CharField(max_length=2, choices=BRAND_CHOICES, default='OT')
    type = models.ForeignKey('Type', on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    description = models.CharField(max_length=100)
    pid = models.CharField(max_length=16)
    size = models.IntegerField()
    color = models.TextField()


class Type(models.Model):
    TYPE_CHOICES = (
        ('BO', 'Boots'),
        ('GL', 'Gloves'),
        ('FO', 'Footballs'),
        ('SP', 'Shin Pads'),
        ('FS', 'Football Shirts'),
        ('SI', 'Shirts'),
        ('SH', 'Shorts'),
        ('SO', 'Socks'),
        ('BL', 'Base Layer'),
        ('JK', 'Jackets'),
        ('EQ', 'Equipments'),
    )

    type = models.CharField(max_length=2, choices=TYPE_CHOICES, default='EQ')
    tier = models.IntegerField()


class TypeBoot(Type):
    PITCH_CHOICES = (
        ('FG', 'Firm Ground'),
        ('SG', 'Soft Ground'),
        ('AG', 'Artificial Ground'),
        ('TF', 'Turf'),
        ('ST', 'Street'),
        ('HG', 'Hard Ground'),
        ('IN', 'Indoor'),
    )

    pitch = models.CharField(max_length=2, choices=PITCH_CHOICES)


class Delivery(models.Model):
    shipping = models.FloatField()
    eta = models.ForeignKey('DateRange', on_delete=models.CASCADE)
    available_country = CountryField(multiple=True)


class DateRange(models.Model):
    min = models.IntegerField()
    max = models.IntegerField()

    def min_days(self):
        return self.min

    def max_days(self):
        return self.max

    def min_date(self):
        return datetime.date.today() + datetime.timedelta(days=self.min)

    def max_date(self):
        return datetime.date.today() + datetime.timedelta(days=self.max)
