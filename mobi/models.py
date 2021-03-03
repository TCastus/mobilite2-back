from django.db import models
from django.core.validators import *
from .consts import *

# Create your models here.
class Country(models.Model):
    """
    Database model describing a country available for an exchange
    """
    name = models.CharField(max_length=100)
    continent = models.CharField(max_length=30, choices=CONTINENTS)
    ECTSConversion = models.FloatField(default=0)

    def __str__(self):
        return self.name


class City(models.Model):
    """
    Database model describing a city available for an exchange.
    Average grades automatically update when a review is posted.
    """
    name = models.CharField(max_length=100)
    country = models.ForeignKey("Country", on_delete=models.CASCADE)
    nb_inhabitants = models.IntegerField(max_length=None, blank=True, validators=[MinValueValidator(0, 0)])

    night_life_average_grade = models.DecimalField(
        max_digits=2, decimal_places=1, default=0, null=True
    )
    cultural_life_average_grade = models.DecimalField(
        max_digits=2, decimal_places=1, default=0, null=True
    )
    security_average_grade = models.DecimalField(
        max_digits=2, decimal_places=1, default=0, null=True
    )

    def __str__(self):
        return f"{self.name} in {self.country}"


class University(models.Model):
    name = models.CharField(max_length=1000)
    city = models.ForeignKey("City", on_delete=models.CASCADE)
    website = models.URLField(blank=True)

    latitude = models.DecimalField(
        max_digits=11, decimal_places=6, null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=11, decimal_places=6, null=True, blank=True
    )

    review_rank = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    CWUR_rank = models.IntegerField(null=True, blank=True)

    Department_availability = models.ManyToManyField('DepartementINSA')


class DepartementINSA(models.Model):
    name = models.CharField(max_length=100, choices=DEPARTEMENTINSA)





class ExchangeReview(models.Model):
    pass
    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None):
    #     super(self, models.Model).save(force_insert=False, force_update=False, using=None,
    #          update_fields=None)
    # Update les métriques de l'université