# Generated by Django 2.0.1 on 2018-02-14 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('giver', '0005_auto_20180201_2012'),
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=100)),
            ],
        ),
    ]