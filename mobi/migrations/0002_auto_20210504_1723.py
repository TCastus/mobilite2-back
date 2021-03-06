# Generated by Django 3.2 on 2021-05-04 15:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mobi', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='university',
            name='contract_type',
        ),
        migrations.RemoveField(
            model_name='university',
            name='places',
        ),
        migrations.AlterField(
            model_name='exchangereview',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='Adresse email'),
        ),
        migrations.CreateModel(
            name='PlacesExchange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(default=0, verbose_name='Nombre de places')),
                ('department_availability', models.ManyToManyField(to='mobi.DepartementINSA', verbose_name='Disponibilité selon le Département')),
                ('semester', models.ManyToManyField(to='mobi.Semester', verbose_name='Semestres concernés')),
                ('university', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='placesExchange', to='mobi.university', verbose_name='Université')),
            ],
            options={
                'verbose_name_plural': 'Places disponibles pour des échanges académiques',
            },
        ),
        migrations.CreateModel(
            name='PlacesDD',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(default=0, verbose_name='Nombre de places')),
                ('department_availability', models.ManyToManyField(to='mobi.DepartementINSA', verbose_name='Disponibilité selon le Département')),
                ('university', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='placesDD', to='mobi.university', verbose_name='Université')),
            ],
            options={
                'verbose_name_plural': 'Places disponibles pour des doubles diplômes',
            },
        ),
    ]
