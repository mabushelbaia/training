# Generated by Django 5.0.1 on 2024-03-25 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_alter_wishlist_listing_alter_wishlist_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
