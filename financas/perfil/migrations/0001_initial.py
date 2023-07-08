# Generated by Django 4.2.2 on 2023-07-03 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoria', models.CharField(max_length=50)),
                ('essencial', models.BooleanField(default=False)),
                ('valor_planejamento', models.FloatField(default=0)),
            ],
        ),
    ]