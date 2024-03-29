# Generated by Django 3.1.7 on 2021-03-29 14:58

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nom de la ville')),
                ('nb_inhabitants', models.PositiveIntegerField(blank=True, null=True, verbose_name="Nombre d'habitants")),
                ('night_life_average_grade', models.DecimalField(decimal_places=1, default=0, max_digits=2, null=True, verbose_name='Note sur la vie nocturne')),
                ('cultural_life_average_grade', models.DecimalField(decimal_places=1, default=0, max_digits=2, null=True, verbose_name='Note sur la vie culturelle')),
                ('cost_of_living_average_grade', models.DecimalField(decimal_places=1, default=0, max_digits=2, null=True, verbose_name='Note sur le coût de la vie')),
                ('security_average_grade', models.DecimalField(decimal_places=1, default=0, max_digits=2, null=True, verbose_name='Note de sécurité')),
                ('rent_average', models.IntegerField(default=0, null=True, verbose_name='Loyer moyen')),
            ],
            options={
                'verbose_name_plural': 'Cities',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nom du pays')),
                ('continent', models.CharField(choices=[('AS', 'Asie'), ('AF', 'Afrique'), ('AdN', 'Amerique du Nord'), ('AdS', 'Amerique du Sud'), ('EU', 'Europe'), ('OC', 'Oceanie')], max_length=30, verbose_name='Continent')),
                ('ECTSConversion', models.FloatField(default=0, verbose_name='Facteur de conversion des ECTS')),
            ],
            options={
                'verbose_name_plural': 'Countries',
            },
        ),
        migrations.CreateModel(
            name='DepartementINSA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('BS', 'Biosciences'), ('GCU', 'Génie Civil et Urbanisme'), ('GE', 'Génie Electrique'), ('GEN', 'Génie Energétique et Environnement'), ('GI', 'Génie Industriel'), ('GM', 'Génie Mécanique'), ('IF', 'Informatique'), ('SGM', 'Science et Génie Matériaux'), ('TC', 'Télécommunications, Services et Usages')], max_length=100, unique=True, verbose_name='Département INSA')),
            ],
            options={
                'verbose_name_plural': 'Departements INSA',
            },
        ),
        migrations.CreateModel(
            name='FinancialAid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization', models.CharField(max_length=100, verbose_name="Nom de l'Organisation de l'aide")),
                ('name', models.CharField(max_length=100, unique=True, verbose_name="Nom de l'aide")),
                ('approx_amount', models.PositiveIntegerField(blank=True, verbose_name='Montant approximatif')),
                ('period', models.CharField(choices=[('Hebdo', 'Hebdomadaire'), ('Mensuel', 'Mensuel'), ('Trim', 'Trimestriel'), ('Sem', 'Semestriel'), ('An', 'Annuel')], max_length=100, verbose_name='Périodicité des aides')),
            ],
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('4A-S1', '4A-S1'), ('4A-S2', '4A-S2'), ('5A-S1', '5A-S1'), ('5A-S2', '5A-S2')], max_length=100, unique=True, verbose_name='Semestre')),
            ],
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000, verbose_name="Nom de l'université")),
                ('website', models.URLField(blank=True, verbose_name='Site Internet')),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=11, null=True, verbose_name='Latitude')),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=11, null=True, verbose_name='Longitude')),
                ('cwur_rank', models.IntegerField(blank=True, null=True, verbose_name='Classement CWUR')),
                ('contract_type', models.CharField(choices=[('DD', 'Double Diplôme'), ('E', 'Echange'), ('X', 'Inconnu'), ('DD+E', 'Double Diplôme & Echange')], default='X', max_length=100, verbose_name='Type de mobilité')),
                ('places', models.IntegerField(blank=True, null=True, verbose_name='Nombre de places disponibles')),
                ('access', models.CharField(choices=[('High', 'Demande forte'), ('Medium', 'Demande normale'), ('Low', 'Demande faible')], default='Medium', max_length=100, verbose_name="Demande / Difficulté d'accès")),
                ('univ_appartment', models.BooleanField(blank=True, null=True, verbose_name="Présence d'appartements sur le campus")),
                ('courses_difficulty', models.DecimalField(decimal_places=1, default=0, max_digits=2, null=True, verbose_name='Note sur la difficulté des cours')),
                ('courses_interest', models.DecimalField(decimal_places=1, default=0, max_digits=2, null=True, verbose_name="Note sur l'intérêt des cours")),
                ('student_proximity', models.DecimalField(decimal_places=1, default=0, max_digits=2, null=True, verbose_name='Note sur la proximité sociale des étudiants')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='universities', to='mobi.city', verbose_name="Ville de l'université")),
                ('department_availability', models.ManyToManyField(to='mobi.DepartementINSA', verbose_name='Disponibilité selon le Département')),
                ('financial_aid', models.ManyToManyField(related_name='financial_aid', to='mobi.FinancialAid', verbose_name='Aides disponibles pour cette université')),
            ],
            options={
                'verbose_name_plural': 'Universities',
            },
        ),
        migrations.CreateModel(
            name='ExchangeReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('culture', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(5)], verbose_name='Note sur la vie culturelle')),
                ('night_life', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(5)], verbose_name='Note sur la vie nocturne')),
                ('cost_of_living', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(5)], verbose_name='Note sur le coût de la vie')),
                ('security', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(5)], verbose_name='Note de sécurité')),
                ('mobility_type', models.CharField(choices=[('DD', 'Double Diplôme'), ('E', 'Echange')], default='E', max_length=100, verbose_name='Type de mobilité')),
                ('univ_appartment', models.BooleanField(verbose_name="Présence d'appartements sur le campus")),
                ('rent', models.IntegerField(blank=True, null=True, verbose_name='Approximation du loyer')),
                ('comments', models.TextField(blank=True, null=True, verbose_name='Commentaires')),
                ('visa', models.BooleanField()),
                ('courses_difficulty', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(5)], verbose_name='Difficulté des cours')),
                ('student_proximity', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(5)], verbose_name='Proximité sociale avec les étudiants')),
                ('courses_interest', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(5)], verbose_name='Intérêt des cours')),
                ('certif_languages', models.CharField(choices=[('TOEIC', 'TOEIC'), ('INC', 'INCONNU'), ('AUCUN', 'AUCUN')], default='AUCUN', max_length=100, verbose_name='Certifications requises pour les langues')),
                ('contact', models.BooleanField(verbose_name="Autorisation d'affichage du contact")),
                ('email', models.EmailField(default='exemple@mail.fr', max_length=254, verbose_name='Adresse email')),
                ('department', models.CharField(choices=[('BS', 'Biosciences'), ('GCU', 'Génie Civil et Urbanisme'), ('GE', 'Génie Electrique'), ('GEN', 'Génie Energétique et Environnement'), ('GI', 'Génie Industriel'), ('GM', 'Génie Mécanique'), ('IF', 'Informatique'), ('SGM', 'Science et Génie Matériaux'), ('TC', 'Télécommunications, Services et Usages')], default='TC', max_length=30, verbose_name='Département INSA')),
                ('name', models.CharField(max_length=100, verbose_name='Nom')),
                ('surname', models.CharField(max_length=100, verbose_name='Prénom')),
                ('year', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(2000), django.core.validators.MaxValueValidator(2050)], verbose_name='Année de départ en échange')),
                ('financial_aid', models.ManyToManyField(to='mobi.FinancialAid', verbose_name='Aides reçus lors de la mobilité')),
                ('semester_accepted', models.ManyToManyField(to='mobi.Semester', verbose_name='Semestres acceptés')),
                ('university', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='mobi.university', verbose_name='Université concernée')),
            ],
        ),
        migrations.AddField(
            model_name='city',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cities', to='mobi.country', verbose_name='Nom du pays de la ville'),
        ),
    ]
