# Generated by Django 4.1.3 on 2023-03-27 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockBasics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 't_stockBasics',
            },
        ),
    ]
