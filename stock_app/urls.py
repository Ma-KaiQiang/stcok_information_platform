"""stcok_information_platform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from stock_app.views import *

urlpatterns = [
    path('stockRealTime/', stock_real_time_view, name='stock_real_time'),
    path('stockList/', stock_list, name='stock_list'),
    path('stockSync/', stock_sync, name='stock_sync'),
    path('stockSelect/', stock_select_list, name='stock_select_list'),
    path('stockIndex/', stock_index, name='stock_index'),
    path('market/', market, name='market'),
    path('stockDetail/', search_stock, name='search_stock'),
    path('addSelect/', add_select, name='add_select'),
    path('positionStock', position_stock_list, name='position_stock_list'),
    path('deselectStock/', deselect_stock, name='deselect_stock'),
    path('klineChart/', get_kline_chart, name='kline_chart'),
    path('kline/', get_kline, name='kline'),
    path('stockNews/', stock_news, name='stock_news'),
    path('stockNewsSync/', stock_news_sync),
    path('sinaNews/', get_sina_news,name='sina_news'),
    path('eastMoneyNews/', get_east_money_news,name='east_money_news'),
    path('fullChart/', get_full_chart,name='full_chart'),

]
