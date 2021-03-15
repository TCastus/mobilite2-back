from django.db import models
from django.core.validators import *
from .consts import *


class NoteField(models.PositiveIntegerField):
    """
    Custom field for a grade between 0 and 5
    """
    def __init__(self, *args, **kwargs):
        super().__init__(validators=[MaxValueValidator(5)], *args, **kwargs)


class Country(models.Model):
    """
    Database model describing a country available for an exchange
    """
    name = models.CharField(max_length=100)
    continent = models.CharField(max_length=30, choices=CONTINENTS)
    ECTSConversion = models.FloatField(default=0)

    def __str__(self):
        return f"{self.name} in {self.continent}"


class City(models.Model):
    """
    Database model describing a city available for an exchange.
    Average grades automatically update when a review is posted.
    """
    name = models.CharField(max_length=100)
    country = models.ForeignKey("Country", on_delete=models.CASCADE)
    nb_inhabitants = models.PositiveIntegerField(max_length=None, blank=True)

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
    cwur_rank = models.IntegerField(null=True, blank=True)

    department_availability = models.ManyToManyField('DepartementINSA')
    
    contract_type = models.CharField(max_length=100, choices=CONTRACTS, default='X')

    def __str__(self):
        return f"{self.name} \nAvailable for {self.department_availability} \nType de mobilité : {self.contract_type}"


class DepartementINSA(models.Model):
    name = models.CharField(max_length=100, choices=DEPARTEMENTINSA)

    def __str__(self):
        return self.name


class Student(models.Model):
    department = models.CharField(max_length=30, choices=DEPARTEMENTINSA)
    email = models.EmailField(default="exemple@mail.fr")
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100, blank=True)
    diploma_year = models.PositiveIntegerField(validators=[MinValueValidator(2000), MaxValueValidator(2050)])

    def __str__(self):
        return f"{self.name} {self.surname}"

class FinancialAid(models.Model):
    organization = models.CharField(max_length=100)  # mettre un manytomany a la place
    name = models.CharField(max_length=100)
    approx_amount = models.PositiveIntegerField(blank=True)
    period = models.CharField(max_length=100, choices=PERIOD)


class ExchangeReview(models.Model):
    university = models.ForeignKey("University", on_delete=models.CASCADE)

    culture = models.PositiveIntegerField(validators=[MaxValueValidator(5)])
    night_life = models.PositiveIntegerField(validators=[MaxValueValidator(5)])
    cost_of_living = models.PositiveIntegerField(validators=[MaxValueValidator(5)])
    security = models.PositiveIntegerField(validators=[MaxValueValidator(5)])

    univ_appartment = models.BooleanField()
    rent = models.IntegerField(blank=True)

    comments = models.TextField(blank=True)

    visa = models.BooleanField()
    courses_difficulty = models.PositiveIntegerField(validators=[MaxValueValidator(5)])
    student_proximity = models.PositiveIntegerField(validators=[MaxValueValidator(5)])
    courses_interest = models.PositiveIntegerField(validators=[MaxValueValidator(5)])

    year_accepted = models.CharField(max_length=100, choices=YEAR)
    languages = models.CharField(max_length=100, choices=LANGUAGES)

    contact = models.BooleanField()