# Generated by Django 5.0.6 on 2024-06-12 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movielist', '0005_review_review_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='avg_rating',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='watchlist',
            name='number_ratings',
            field=models.IntegerField(default=0),
        ),
    ]