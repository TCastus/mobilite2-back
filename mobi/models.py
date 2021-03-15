from django.db import models
from django.core.validators import *
from .consts import *


# class NoteField(models.PositiveIntegerField):
#     """
#     Custom field for a grade between 0 and 5
#     """
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(validators=[MaxValueValidator(5)], *args, **kwargs)


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
    cost_of_living_average_grade = models.DecimalField(
        max_digits=2, decimal_places=1, default=0, null=True
    )
    security_average_grade = models.DecimalField(
        max_digits=2, decimal_places=1, default=0, null=True
    )
    rent_average = models.DecimalField(max_digits=2, decimal_places=1, default=0, null=True)

    def __str__(self):
        return f"{self.name} in {self.country}"


class University(models.Model):
    """
    Databse object which represents a university and its characteristics
    """

    class Meta:
        verbose_name_plural = "universities"

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

    univ_appartment = models.BooleanField()

    courses_difficulty = models.DecimalField(
        max_digits=2, decimal_places=1, default=0, null=True
    )
    courses_interest = models.DecimalField(
        max_digits=2, decimal_places=1, default=0, null=True
    )
    student_proximity = models.DecimalField(
        max_digits=2, decimal_places=1, default=0, null=True
    )

    def __str__(self):
        return f"{self.name} \nAvailable for {self.department_availability} \nType de mobilité : {self.contract_type}"


class DepartementINSA(models.Model):
    name = models.CharField(max_length=100, choices=DEPARTEMENTINSA, unique=True)

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
    """
    Represents a finalcial aid that can be asked for an student exchange
    """

    university = models.ForeignKey("University", null=True, on_delete=models.CASCADE)
    country = models.ForeignKey("Country", null=True, on_delete=models.CASCADE)
    organization = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    approx_amount = models.PositiveIntegerField(blank=True)
    period = models.CharField(max_length=100, choices=PERIOD)


class ExchangeReview(models.Model):
    """
    A exchange review posted by a student
    """
    university = models.ForeignKey("University", on_delete=models.CASCADE)

    culture = models.PositiveIntegerField()
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

    def save(self, *args, **kwargs):
        """
        Update the grade fields for the university and city when saving the review
        """
        super(ExchangeReview, self).save(*args, **kwargs)

        # Get city & university
        city = University.objects.get(id=self.university.id).city
        uni = University.objects.get(id=self.university.id)
        # Get every Exchange Review which is in this uni
        reviews = University.objects.filter(university__city=city)

        # Work out the sum of the grades for each category
        culture = reviews.aggregate(models.Avg('culture'))
        night_life = reviews.aggregate(models.Avg('night_life'))
        cost_of_living = reviews.aggregate(models.Avg('cost_of_living'))
        security = reviews.aggregate(models.Avg('security'))
        rent = reviews.aggregate(models.Avg('rent'))

        # Work out the average grades for university criteria
        courses_difficulty = reviews.filter(university=uni).aggregate(models.Avg('courses_difficulty'))
        student_proximity = reviews.filter(university=uni).aggregate(models.Avg('student_proximity'))
        courses_interest = reviews.filter(university=uni).aggregate(models.Avg('courses_interest'))

        # Save the average values
        city.cultural_life_average_grade = culture['culture__avg']
        city.night_life_average_grade = night_life['night_life__avg']
        city.cost_of_living_average_grade = cost_of_living['cost_of_living__avg']
        city.security_average_grade = security['security__avg']
        city.rent_average = rent['rent__avg']

        uni.courses_difficulty = courses_difficulty['courses_difficulty__avg']
        uni.courses_interest = courses_interest['courses_interest__avg']
        uni.student_proximity = student_proximity['student_proximity__avg']

        # Update the university object & save
        city.save()
        uni.save()
