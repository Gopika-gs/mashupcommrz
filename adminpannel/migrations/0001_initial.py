# Generated by Django 4.0.5 on 2022-06-24 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=200)),
                ('price', models.FloatField()),
                ('product_description', models.CharField(max_length=1000)),
                ('product_picture', models.FileField(upload_to='')),
                ('is_active', models.SmallIntegerField(default=1)),
            ],
        ),
    ]
