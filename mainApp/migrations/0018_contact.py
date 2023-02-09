# Generated by Django 4.1.2 on 2023-02-05 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0017_checkoutproduct_qty_checkoutproduct_total'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=60)),
                ('phone', models.IntegerField(max_length=15)),
                ('subject', models.CharField(max_length=50)),
                ('message', models.TextField()),
                ('status', models.IntegerField(choices=[(0, 'Active'), (1, 'Done')], default=0)),
                ('date', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]