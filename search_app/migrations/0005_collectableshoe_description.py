# Generated by Django 5.1.4 on 2024-12-28 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search_app', '0004_delete_bio_delete_participant'),
    ]

    operations = [
        migrations.AddField(
            model_name='collectableshoe',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
