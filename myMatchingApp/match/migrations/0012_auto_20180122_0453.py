# Generated by Django 2.0.1 on 2018-01-22 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0011_auto_20180122_0424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matching',
            name='algorithm',
            field=models.CharField(choices=[('Shapley Gale Blue Proposes', 'Shapley Gale Blue Proposes'), ('Shapley Gale Red Proposes', 'Shapley Gale Red Proposes')], default='Shapley Gale Blue Proposes', max_length=50),
        ),
    ]
