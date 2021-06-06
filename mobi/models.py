from django.db import models
from django.core.validators import *
from .consts import *


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

    def __str__(self):
        return f"{self.name} in {self.country}"


class University(models.Model):
    """
    Database object which represents a university and its characteristics
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
        max_digits=18, decimal_places=14, null=True, blank=True,
        verbose_name="Latitude"
    )
    longitude = models.DecimalField(
        max_digits=18, decimal_places=14, null=True, blank=True,
        verbose_name="Longitude"
    )

    cwur_rank = models.IntegerField(
        null=True, blank=True,
        verbose_name="Classement CWUR")

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

    def courses_difficulty(self):
        reviews_uni = ExchangeReview.objects.filter(university=self)
        if len(reviews_uni) == 0:
            return {'courses_difficulty__avg':0}
        courses_difficulty = reviews_uni.aggregate(models.Avg('courses_difficulty'))

        if not courses_difficulty:
            return 0

        return courses_difficulty

    def courses_interest(self):
        reviews_uni = ExchangeReview.objects.filter(university=self)
        if len(reviews_uni) == 0:
            return 0
        courses_interest = reviews_uni.aggregate(models.Avg('courses_interest'))
        return courses_interest

    def student_proximity(self):
        reviews_uni = ExchangeReview.objects.filter(university=self)
        if len(reviews_uni) == 0:
            return 0
        student_proximity = reviews_uni.aggregate(models.Avg('student_proximity'))
        return student_proximity

    def review_number(self):
        reviews_uni = ExchangeReview.objects.filter(university=self)
        number = reviews_uni.count()
        return number

    def culture(self):
        reviews_city = ExchangeReview.objects.filter(university__city=self.city)
        if len(reviews_city) == 0:
            return {'culture__avg':0}
        culture = reviews_city.aggregate(models.Avg('culture'))
        return culture

    def night_life(self):
        reviews_city = ExchangeReview.objects.filter(university__city=self.city)
        if len(reviews_city) == 0:
            return {'night_life__avg': 0}
        night_life = reviews_city.aggregate(models.Avg('night_life'))
        return night_life

    def cost_of_living(self):
        reviews_city = ExchangeReview.objects.filter(university__city=self.city)
        if len(reviews_city) == 0:
            return {'cost_of_living__avg': 0}
        cost_of_living = reviews_city.aggregate(models.Avg('cost_of_living'))
        return cost_of_living

    def security(self):
        reviews_city = ExchangeReview.objects.filter(university__city=self.city)
        if len(reviews_city) == 0:
            return 0
        security = reviews_city.aggregate(models.Avg('security'))
        return security

    def rent(self):
        reviews_city = ExchangeReview.objects.filter(university__city=self.city)
        if len(reviews_city) == 0:
            return 0
        rent = reviews_city.aggregate(models.Avg('rent'))
        return rent

    def department(self):
        placesE = PlacesExchange.objects.filter(university__id=self.id)
        placesDD = PlacesDD.objects.filter(university__id=self.id)
        outputSet = set()

        for place in placesE:
            outputSet.update([dep.name for dep in place.department_availability.all()])
        for place in placesDD:
            outputSet.update([dep.name for dep in place.department_availability.all()])

        return outputSet





class DepartementINSA(models.Model):
    """
    Database object that countains the name of each INSA Department
    """

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
    """
    Database object representing a set of available spots for exchanges
    """

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
        return f"{self.university.name} : {self.number} places pour {'/'.join([semester.name for semester in self.semester.all()])} pour {'/'.join([dep.name for dep in self.department_availability.all()])} en Echange"


class PlacesDD(models.Model):
    """
    Database object representing a set of available spots for double degree
    """

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
        return f"{self.university.name} : {self.number} places pour {'/'.join([dep.name for dep in self.department_availability.all()])} en DD"





class Semester(models.Model):
    """
    Database object that countains the semesters on which students can go on exchange or other type of mobility
    """

    name = models.CharField(max_length=100, choices=SEMESTER, unique=True, verbose_name="Semestre")

    def __str__(self):
        return f"{self.name}"


class FinancialAid(models.Model):
    """
    Database object that represents a financial aid that can be asked for a student exchange
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

    datetime = models.DateField(verbose_name="Jour de publication", auto_now_add=True)

    university = models.ForeignKey(
        "University",
        related_name='reviews',
        on_delete=models.CASCADE,
        verbose_name="Université concernée")

    culture = models.DecimalField(
        max_digits=2, decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name="Note sur la vie culturelle",
        default=0
    )

    night_life = models.DecimalField(
        max_digits=2, decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name="Note sur la vie nocturne",
        default=0
    )

    cost_of_living = models.DecimalField(
        max_digits=2, decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name="Note sur le coût de la vie",
        default=0
    )

    security = models.DecimalField(
        max_digits=2, decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name="Note de sécurité",
        default=0
    )

    courses_difficulty = models.DecimalField(
        max_digits=2, decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name="Difficulté des cours",
        default=0
    )

    student_proximity = models.DecimalField(
        max_digits=2, decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name="Proximité sociale avec les étudiants",
        default=0
    )

    courses_interest = models.DecimalField(
        max_digits=2, decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name="Intérêt par rapport aux cours",
        default=0

    )

    mobility_type = models.CharField(
        max_length=100, choices=MOBITYPE, default='E',
        verbose_name="Type de mobilité",
    )


    univ_appartment = models.BooleanField(verbose_name="Appartements disponibles sur le campus")
    rent = models.IntegerField(blank=True, null=True, verbose_name="Approximation du loyer")

    comments = models.TextField(blank=True, null=True, verbose_name="Commentaires")

    visa = models.TextField(blank=True, null=True, verbose_name="Obtention du visa")

    semester = models.CharField(max_length=30, choices=SEMESTER, blank=True, verbose_name="Semestre de mobilité")

    certif_languages = models.CharField(
        verbose_name="Certifications requises pour les langues",
        max_length=100, choices=LANGUAGES,
        default="AUCUN"
    )
    financial_aid = models.ManyToManyField(
        'FinancialAid',
        blank=True,
        verbose_name="Aides reçus lors de la mobilité"
    )

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
    year = models.PositiveIntegerField(
        verbose_name="Année de départ en échange",
        validators=[MinValueValidator(2000), MaxValueValidator(2100)],
    )

    def __str__(self):
        return f"Review from {self.surname}"

