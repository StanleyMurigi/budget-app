# Generated by Django 5.0.6 on 2025-03-23 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0003_alter_budget_name_alter_category_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='allocated_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
