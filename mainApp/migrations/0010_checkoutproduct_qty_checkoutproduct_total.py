# Generated by Django 4.1.2 on 2023-02-04 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0009_checkout_checkoutproduct'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkoutproduct',
            name='qty',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='checkoutproduct',
            name='total',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
    ]
