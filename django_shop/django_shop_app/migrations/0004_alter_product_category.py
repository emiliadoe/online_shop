# Generated by Django 4.2.1 on 2024-06-30 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_shop_app', '0003_cartitem_delete_category_product_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('S', 'Schokolade'), ('G', 'Gummibaerchen'), ('K', 'Kaugummis'), ('B', 'Bonbons'), ('So', 'Sonstiges')], max_length=2),
        ),
    ]
