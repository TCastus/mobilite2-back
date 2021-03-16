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
    class Meta:
        verbose_name_plural = "Countries"

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
    class Meta:
        verbose_name_plural = "Cities"

    name = models.CharField(max_length=100)
    country = models.ForeignKey("Country", on_delete=models.CASCADE)
    nb_inhabitants = models.PositiveIntegerField(max_length=None, blank=True, null=True)

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
        verbose_name_plural = "Universities"

    name = models.CharField(max_length=1000)
    city = models.ForeignKey("City", on_delete=models.CASCADE)
    website = models.URLField(blank=True)

    latitude = models.DecimalField(
        max_digits=11, decimal_places=6, null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=11, decimal_places=6, null=True, blank=True
    )

    cwur_rank = models.IntegerField(null=True, blank=True)

    department_availability = models.ManyToManyField('DepartementINSA')

    contract_type = models.CharField(max_length=100, choices=CONTRACTS, default='X')

    univ_appartment = models.BooleanField(null=True, blank=True)

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
        return f"{self.name}"


class DepartementINSA(models.Model):
    class Meta:
        verbose_name_plural = "Departements INSA"

    name = models.CharField(max_length=100, choices=DEPARTEMENTINSA, unique=True)

    def __str__(self):
        return self.name

class Semester(models.Model):
    name = models.CharField(max_length=100, choices=SEMESTER, unique=True)

    def __str__(self):
        return self.name

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
    rent = models.IntegerField(blank=True, null=True)

    comments = models.TextField(blank=True, null=True)

    visa = models.BooleanField()
    courses_difficulty = models.PositiveIntegerField(validators=[MaxValueValidator(5)])
    student_proximity = models.PositiveIntegerField(validators=[MaxValueValidator(5)])
    courses_interest = models.PositiveIntegerField(validators=[MaxValueValidator(5)])

    semester_accepted = models.ManyToManyField('Semester')
    certif_languages = models.CharField(
        verbose_name="Certifications requises pour les langues",
        max_length=100, choices=LANGUAGES,
        default="AUCUN"
    )

    # Contact of the writer
    contact = models.BooleanField(verbose_name="Autorisation d'affichage du contact")
    email = models.EmailField(verbose_name="Adresse email", default="exemple@mail.fr")
    department = models.CharField(
        verbose_name="Département INSA",
        max_length=30,
        choices=DEPARTEMENTINSA,
        default="TC"
    )
    name = models.CharField(verbose_name="Nom", max_length=100)
    surname = models.CharField(verbose_name="Prénom", max_length=100)
    diploma_year = models.PositiveIntegerField(
        verbose_name="Année de départ en échange",
        validators=[MinValueValidator(2000), MaxValueValidator(2050)],
    )

    def save(self, *args, **kwargs):
        """
        Update the grade fields for the university and city when saving the review
        """
        super(ExchangeReview, self).save(*args, **kwargs)

        # Get city & university
        city = University.objects.get(id=self.university.id).city
        uni = University.objects.get(id=self.university.id)
        # Get every Exchange Review which is in this uni
        reviews_city = ExchangeReview.objects.filter(university__city=city)
        reviews_uni = ExchangeReview.objects.filter(university=uni)


        # Work out the sum of the grades for each category
        culture = reviews_city.aggregate(models.Avg('culture'))
        night_life = reviews_city.aggregate(models.Avg('night_life'))
        cost_of_living = reviews_city.aggregate(models.Avg('cost_of_living'))
        security = reviews_city.aggregate(models.Avg('security'))
        rent = reviews_city.aggregate(models.Avg('rent'))


        # Work out the average grades for university criteria
        courses_difficulty = reviews_uni.aggregate(models.Avg('courses_difficulty'))
        student_proximity = reviews_uni.aggregate(models.Avg('student_proximity'))
        courses_interest = reviews_uni.aggregate(models.Avg('courses_interest'))

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
