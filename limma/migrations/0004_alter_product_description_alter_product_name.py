# Generated by Django 4.2.5 on 2024-09-11 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('limma', '0003_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=600),
        ),
    ]
