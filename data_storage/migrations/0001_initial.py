# Generated by Django 5.1.1 on 2024-09-19 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ParsedContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(max_length=500)),
                ('title', models.CharField(blank=True, max_length=500)),
                ('description', models.TextField(blank=True)),
                ('keywords', models.TextField(blank=True)),
                ('headings', models.JSONField(blank=True, null=True)),
                ('text', models.TextField(blank=True)),
                ('links', models.JSONField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
