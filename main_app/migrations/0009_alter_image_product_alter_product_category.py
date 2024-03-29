# Generated by Django 5.0.1 on 2024-02-07 12:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0008_alter_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='product',
            field=models.ForeignKey(null=[0], on_delete=django.db.models.deletion.CASCADE, to='main_app.product'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(default=True, to='main_app.category'),
        ),
    ]
