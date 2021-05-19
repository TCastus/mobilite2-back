# Generated by Django 3.2 on 2021-05-19 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mobi', '0002_auto_20210510_1426'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exchangereview',
            name='semester_accepted',
        ),
        migrations.AddField(
            model_name='exchangereview',
            name='semester',
            field=models.CharField(blank=True, choices=[('4A-S1', '4A-S1'), ('4A-S2', '4A-S2'), ('5A-S1', '5A-S1'), ('5A-S2', '5A-S2'), ('4A', '4A'), ('5A', '5A')], max_length=30, verbose_name='Semestre de mobilité'),
        ),
        migrations.AlterField(
            model_name='departementinsa',
            name='name',
            field=models.CharField(choices=[('BB', 'Biosciences Biochimie et Biotechnologie'), ('BIM', 'Bioinformatique et Modélisation'), ('GCU', 'Génie Civil et Urbanisme'), ('GE', 'Génie Electrique'), ('GEN', 'Génie Energétique et Environnement'), ('GI', 'Génie Industriel'), ('GM', 'Génie Mécanique'), ('IF', 'Informatique'), ('SGM', 'Science et Génie Matériaux'), ('TC', 'Télécommunications, Services et Usages')], max_length=100, unique=True, verbose_name='Département INSA'),
        ),
        migrations.AlterField(
            model_name='exchangereview',
            name='department',
            field=models.CharField(choices=[('BB', 'Biosciences Biochimie et Biotechnologie'), ('BIM', 'Bioinformatique et Modélisation'), ('GCU', 'Génie Civil et Urbanisme'), ('GE', 'Génie Electrique'), ('GEN', 'Génie Energétique et Environnement'), ('GI', 'Génie Industriel'), ('GM', 'Génie Mécanique'), ('IF', 'Informatique'), ('SGM', 'Science et Génie Matériaux'), ('TC', 'Télécommunications, Services et Usages')], default='TC', max_length=30, verbose_name='Département INSA'),
        ),
        migrations.AlterField(
            model_name='exchangereview',
            name='financial_aid',
            field=models.ManyToManyField(blank=True, to='mobi.FinancialAid', verbose_name='Aides reçus lors de la mobilité'),
        ),
        migrations.AlterField(
            model_name='semester',
            name='name',
            field=models.CharField(choices=[('4A-S1', '4A-S1'), ('4A-S2', '4A-S2'), ('5A-S1', '5A-S1'), ('5A-S2', '5A-S2'), ('4A', '4A'), ('5A', '5A')], max_length=100, unique=True, verbose_name='Semestre'),
        ),
    ]
