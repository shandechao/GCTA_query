# Generated by Django 5.2.2 on 2025-06-07 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_sequencepatternsearch_unique_pattern_per_sequence'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sequencepatternsearch',
            name='search_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
