# Generated by Django 4.2 on 2024-07-08 20:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserAdmin', '0006_alter_myuser_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='date_of_birth',
            field=models.DateField(default=datetime.date(2004, 7, 8)),
        ),
    ]
