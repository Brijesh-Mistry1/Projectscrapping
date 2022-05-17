# Generated by Django 3.2.6 on 2021-10-26 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cust_name', models.CharField(max_length=160, verbose_name='Customer Name')),
                ('cust_status', models.BooleanField(default=True, verbose_name='Status')),
            ],
        ),
    ]