# Generated by Django 5.0.1 on 2024-02-05 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_remove_customuser_name_alter_customuser_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(default=True, to='main_app.category'),
        ),
    ]