# Generated by Django 4.1.2 on 2023-02-05 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0019_alter_contact_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='phone',
            field=models.CharField(max_length=15),
        ),
    ]
