# Generated by Django 3.1.5 on 2021-01-21 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('receipt', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receipt',
            name='item',
            field=models.ManyToManyField(blank=True, null=True, to='receipt.Item'),
        ),
    ]
