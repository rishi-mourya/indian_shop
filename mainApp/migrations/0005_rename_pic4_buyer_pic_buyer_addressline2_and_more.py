# Generated by Django 4.1.2 on 2023-02-01 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0004_alter_buyer_addressline1'),
    ]

    operations = [
        migrations.RenameField(
            model_name='buyer',
            old_name='pic4',
            new_name='pic',
        ),
        migrations.AddField(
            model_name='buyer',
            name='addressline2',
            field=models.CharField(blank=True, default='', max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='buyer',
            name='addressline3',
            field=models.CharField(blank=True, default='', max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='buyer',
            name='addressline4',
            field=models.CharField(blank=True, default='', max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='buyer',
            name='addressline1',
            field=models.CharField(max_length=150),
        ),
    ]