# Generated by Django 4.2.5 on 2024-01-04 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hospital', '0014_article_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='done',
            field=models.BooleanField(default=False),
        ),
    ]
