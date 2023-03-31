from django.db import models


# Create your models here.

class StockSelect(models.Model):
    code = models.CharField(max_length=10)

    class Meta:
        db_table = 't_stockSelect'


class StockBasics(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    area = models.CharField(max_length=10, default=None)
    industry = models.CharField(max_length=10, default=None)
    list_date = models.CharField(max_length=50, default=None)

    class Meta:
        db_table = 't_stockBasics'


class StockNews(models.Model):
    time = models.CharField(max_length=10)
    content = models.CharField(max_length=1000)
    platform = models.CharField(max_length=1000, default='新浪')
    type = models.CharField(max_length=500, default=1, verbose_name='1 A股')

    class Meta:
        db_table = 't_stock_news'
