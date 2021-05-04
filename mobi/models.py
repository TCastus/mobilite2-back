from django.db import models
from django.core.validators import *
from .consts import *


# TODO: Implement the model and use it
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

    name = models.CharField(max_length=100, verbose_name="Nom du pays")
    continent = models.CharField(max_length=30, choices=CONTINENTS, verbose_name="Continent")
    ECTSConversion = models.FloatField(default=0, verbose_name="Facteur de conversion des ECTS")

    def __str__(self):
        return f"{self.name} in {self.continent}"


class City(models.Model):
    """
    Database model describing a city available for an exchange.
    Average grades automatically update when a review is posted.
    """

    class Meta:
        verbose_name_plural = "Cities"

    name = models.CharField(max_length=100, verbose_name="Nom de la ville")
    country = models.ForeignKey(
        "Country",
        related_name="cities",
        on_delete=models.CASCADE,
        verbose_name="Nom du pays de la ville"
    )
    nb_inhabitants = models.PositiveIntegerField(
        max_length=None, blank=True, null=True,
        verbose_name="Nombre d'habitants"
    )

    night_life_average_grade = models.DecimalField(
        max_digits=2, decimal_places=1, default=0, null=True,
        verbose_name="Note sur la vie nocturne"
    )
    cultural_life_average_grade = models.DecimalField(
        max_digits=2, decimal_places=1, default=0, null=True,
        verbose_name="Note sur la vie culturelle"
    )
    cost_of_living_average_grade = models.DecimalField(
        max_digits=2, decimal_places=1, default=0, null=True,
        verbose_name="Note sur le coût de la vie"
    )
    security_average_grade = models.DecimalField(
        max_digits=2, decimal_places=1, default=0, null=True,
        verbose_name="Note de sécurité"
    )
    rent_average = models.IntegerField(
        default=0, null=True,
        verbose_name="Loyer moyen"
    )

    def __str__(self):
        return f"{self.name} in {self.country}"


class University(models.Model):
    """
    Databse object which represents a university and its characteristics
    """

    class Meta:
        verbose_name_plural = "Universities"

    name = models.CharField(max_length=1000, verbose_name="Nom de l'université")
    city = models.ForeignKey(
        "City",
        related_name="universities",
        on_delete=models.CASCADE,
        verbose_name="Ville de l'université"
    )
    website = models.URLField(blank=True, verbose_name="Site Internet")

    latitude = models.DecimalField(
        max_digits=11, decimal_places=6, null=True, blank=True,
        verbose_name="Latitude"
    )
    longitude = models.DecimalField(
        max_digits=11, decimal_places=6, null=True, blank=True,
        verbose_name="Longitude"
    )

    cwur_rank = models.IntegerField(
        null=True, blank=True,
        verbose_name="Classement CWUR")

    department_availability = models.ManyToManyField(
        'DepartementINSA',
        verbose_name="Disponibilité selon le Département"
    )

    access = models.CharField(
        max_length=100,
        choices=ACCESS,
        default='Medium',
        verbose_name="Demande / Difficulté d'accès"
    )

    univ_appartment = models.BooleanField(
        null=True, blank=True,
        verbose_name="Présence d'appartements sur le campus"
    )

    courses_difficulty = models.DecimalField(
        max_digits=2, decimal_places=1, default=0, null=True,
        verbose_name="Note sur la difficulté des cours"
    )
    courses_interest = models.DecimalField(
        max_digits=2, decimal_places=1, default=0, null=True,
        verbose_name="Note sur l'intérêt des cours"
    )
    student_proximity = models.DecimalField(
        max_digits=2, decimal_places=1, default=0, null=True,
        verbose_name="Note sur la proximité sociale des étudiants"
    )
    financial_aid = models.ManyToManyField(
        'FinancialAid',
        related_name="financial_aid",
        verbose_name="Aides disponibles pour cette université"
    )

    def __str__(self):
        return f"{self.name}"

    def city_name(self):
        return f"{self.city.name}"

    def country_name(self):
        return f"{self.city.country.name}"


class DepartementINSA(models.Model):
    class Meta:
        verbose_name_plural = "Departements INSA"

    name = models.CharField(
        max_length=100,
        choices=DEPARTEMENTINSA,
        unique=True,
        verbose_name="Département INSA"
    )

    def __str__(self):
        return self.name


class PlacesExchange(models.Model):
    class Meta:
        verbose_name_plural = "Places disponibles pour des échanges académiques"

    university = models.ForeignKey(
        "University",
        related_name="placesExchange",
        on_delete=models.CASCADE,
        verbose_name="Université"
    )

    number = models.IntegerField(
        default=0,
        verbose_name="Nombre de places"
    )

    semester = models.ManyToManyField(
        'Semester',
        verbose_name="Semestres concernés"
    )

    department_availability = models.ManyToManyField(
        'DepartementINSA',
        verbose_name="Disponibilité selon le Département"
    )

    def __str__(self):
        return f"{self.number} places pour {'/'.join([semester.name for semester in self.semester.all()])} pour départements {'/'.join([dep.name for dep in self.department_availability.all()])} en Echange"


class PlacesDD(models.Model):
    class Meta:
        verbose_name_plural = "Places disponibles pour des doubles diplômes"

    university = models.ForeignKey(
        "University",
        related_name="placesDD",
        on_delete=models.CASCADE,
        verbose_name="Université"
    )

    number = models.IntegerField(
        default=0,
        verbose_name="Nombre de places"
    )

    department_availability = models.ManyToManyField(
        'DepartementINSA',
        verbose_name="Disponibilité selon le Département"
    )

    def __str__(self):
        return f"{self.number} places pour départements {'/'.join([dep.name for dep in self.department_availability.all()])} en DD"




class Semester(models.Model):
    name = models.CharField(max_length=100, choices=SEMESTER, unique=True, verbose_name="Semestre")

    def __str__(self):
        return f"{self.name}"


class FinancialAid(models.Model):
    """
    Represents a financial aid that can be asked for a student exchange
    """

    organization = models.CharField(max_length=100, verbose_name="Nom de l'Organisation de l'aide")
    name = models.CharField(max_length=100, verbose_name="Nom de l'aide", unique=True)
    approx_amount = models.PositiveIntegerField(blank=True, verbose_name="Montant approximatif")
    period = models.CharField(
        max_length=100,
        choices=PERIOD,
        verbose_name="Périodicité des aides"
    )

    def __str__(self):
        return f"{self.name}"


class ExchangeReview(models.Model):
    """
    A exchange review posted by a student
    """
    university = models.ForeignKey(
        "University",
        related_name='reviews',
        on_delete=models.CASCADE,
        verbose_name="Université concernée")

    culture = models.PositiveIntegerField(
        validators=[MaxValueValidator(5)],
        verbose_name="Note sur la vie culturelle"
    )
    night_life = models.PositiveIntegerField(
        validators=[MaxValueValidator(5)],
        verbose_name="Note sur la vie nocturne"
    )
    cost_of_living = models.PositiveIntegerField(
        validators=[MaxValueValidator(5)],
        verbose_name="Note sur le coût de la vie"
    )
    security = models.PositiveIntegerField(
        validators=[MaxValueValidator(5)],
        verbose_name="Note de sécurité"
    )
    mobility_type = models.CharField(
        max_length=100, choices=MOBITYPE, default='E',
        verbose_name="Type de mobilité"
    )

    univ_appartment = models.BooleanField(verbose_name="Présence d'appartements sur le campus")
    rent = models.IntegerField(blank=True, null=True, verbose_name="Approximation du loyer")

    comments = models.TextField(blank=True, null=True, verbose_name="Commentaires")

    visa = models.BooleanField()
    courses_difficulty = models.PositiveIntegerField(
        validators=[MaxValueValidator(5)],
        verbose_name="Difficulté des cours"
    )
    student_proximity = models.PositiveIntegerField(
        validators=[MaxValueValidator(5)],
        verbose_name="Proximité sociale avec les étudiants"
    )
    courses_interest = models.PositiveIntegerField(
        validators=[MaxValueValidator(5)],
        verbose_name="Intérêt des cours"
    )

    semester_accepted = models.ManyToManyField('Semester', verbose_name="Semestres acceptés")
    certif_languages = models.CharField(
        verbose_name="Certifications requises pour les langues",
        max_length=100, choices=LANGUAGES,
        default="AUCUN"
    )
    financial_aid = models.ManyToManyField(
        'FinancialAid',
        verbose_name="Aides reçus lors de la mobilité"
    )

    # Contact of the writer
    contact = models.BooleanField(verbose_name="Autorisation d'affichage du contact")
    email = models.EmailField(verbose_name="Adresse email")
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

    def __str__(self):
        return f"Review from {self.surname}"

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
