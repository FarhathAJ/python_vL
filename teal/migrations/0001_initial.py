# Generated by Django 5.0.6 on 2024-06-20 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='chkboxoption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('optionname', models.CharField(max_length=100)),
                ('optionvalue', models.CharField(max_length=100)),
            ],
        ),
    ]
