# Generated by Django 4.2.2 on 2023-07-26 05:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0010_bid"),
    ]

    operations = [
        migrations.AddField(
            model_name="listing",
            name="bid",
            field=models.ManyToManyField(
                blank=True, null=True, related_name="listing_bid", to="auctions.bid"
            ),
        ),
    ]