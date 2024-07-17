# Generated by Django 4.2 on 2024-07-14 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_shop_app', '0006_alter_product_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='rating',
            field=models.IntegerField(choices=[(1, '1 Sterne'), (2, '2 Sterne'), (3, '3 Sterne'), (4, '4 Sterne'), (5, '5 Sterne')], default=3),
        ),
    ]