# Generated by Django 4.2.5 on 2024-01-04 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hospital', '0012_article_article_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='subject',
            field=models.CharField(max_length=256),
        ),
    ]
