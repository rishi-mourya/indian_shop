# Generated by Django 4.1.2 on 2023-01-31 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0002_alter_buyer_addressline1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyer',
            name='addressline1',
            field=models.CharField(max_length=150),
        ),
    ]
