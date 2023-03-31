import json

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from stock_app.business.search_stock import *
from django.views.decorators.csrf import csrf_exempt
from stock_app.models import StockSelect, StockBasics, StockNews
import re
from stock_app.business.news.business.tushare_handle import TuShare


def stock_list(request):
    '''
    股票列表
    :param request:
    :return:
    '''
    stock_list = StockBasics.objects.values_list('code', 'name', 'area', 'industry', 'list_date')
    return render(request, 'stock_list.html', {'stock_list': stock_list})


def stock_sync(request):
    '''
    股票同步
    :param request:
    :return:
    '''
    ts = TuShareApi()
    stock_data_list = ts.get_stock_list()
    stock_data = []
    for l in stock_data_list:
        stock_obj = StockBasics(code=l[0], name=l[1], area=l[2], industry=l[3], list_date=l[4])
        stock_data.append(stock_obj)
    StockBasics.objects.bulk_create(stock_data, ignore_conflicts=True)
    return redirect(stock_list)


# Create your views here.
def stock_real_time_view(request):
    codes = list(StockSelect.objects.values_list('code', flat=True))
    stock_item = stock_real_time(codes)
    return render(request, 'stock_information.html', {'stock_item': stock_item})


def stock_select_list(request):
    codes = list(StockSelect.objects.values_list('code', flat=True))
    stock_item = stock_real_time(codes)
    return render(request, 'stock_select_manager.html', {'stock_item': stock_item})


def stock_index(request):
    '''
    行情
    :param request:
    :return:
    '''
    return render(request, 'stock_index.html')


def market(request):
    data = stock_to_be_raised()
    return render(request, 'market.html', {'data': data})


@csrf_exempt
def search_stock(request):
    '''
    查询股票
    :param request:
    :return:
    '''
    if request.method == 'POST':
        code = request.POST.get('code')
        if code:

            if re.match('[0-9]{4,10}', code):
                response = search_stock_code(code)
            else:
                code_ = StockBasics.objects.filter(name=code).first().code
                response = search_stock_code(code_)
            return render(request, 'stock_detail.html', response)
        else:
            return render(request, 'stock_detail.html', {"msg": '请输入正确代码或名称.'})


@csrf_exempt
def add_select(request):
    '''
    添加股票到自选
    :param request:
    :return:
    '''
    if request.method == 'POST':
        code = request.POST.get('code')
        if code:
            if StockSelect.objects.filter(code=code).first():
                return render(request, 'stock_detail.html', {"msg": '该股票已添加，请勿重复添加.'})
            else:
                StockSelect.objects.create(code=code)
        return redirect('position_stock_list')


@csrf_exempt
def position_stock_list(request):
    codes = list(StockSelect.objects.values_list('code', flat=True))
    stock_item = stock_manage(codes)
    return render(request, 'stock_select_manager.html', {'stock_item': stock_item})


@csrf_exempt
def deselect_stock(request):
    return redirect('position_stock_list')


@csrf_exempt
def get_kline(request):
    tsa = TuShareApi()
    data = json.loads(request.body.decode(encoding='utf8'))
    stock_name = data.get('name')
    time = data.get('time')
    code = data.get('code')
    data = tsa.get_stock_data(code, int(time))
    c = tsa.kline_base(data.get('mydate'), data.get('kdata'), stock_name)
    # return render(request,'kline.html',{'data':c})
    return JsonResponse(json.loads(c))


def get_kline_chart(request):
    return HttpResponse(content=open(r"D:\项目\stcok_information_platform\templates\kline.html").read())


@csrf_exempt
def get_full_chart(request):
    tsa = TuShareApi()
    data = json.loads(request.body.decode(encoding='utf8'))
    stock_name = data.get('name')
    time = data.get('time')
    code = data.get('code')
    data = tsa.get_stock_data(code, int(time))
    c = tsa.full_chart(mydate=data.get('mydate'), kdata=data.get('kdata'), data_5=data.get('madata_5'),
                       data_10=data.get('madata_10'), data_20=data.get('madata_20'),
                       volume_rise=data.get('volume_rise'), volume_drop=data.get('volume_drop'), name=stock_name)
    print(type(c.dump_options()))
    return JsonResponse(json.loads(c.dump_options()))


def stock_news_sync(request):
    tu = TuShare()
    data = tu.get_all_platform_news()
    all = StockNews.objects.all()
    all.delete()
    for d in data:
        obj = []
        for info in d.get('info'):
            obj.append(StockNews(time=info[0], content=info[1], platform=d.get('platform'), type=d.get('type')))
        StockNews.objects.bulk_create(obj, ignore_conflicts=True)
    return JsonResponse({'code': 200})


def stock_news(request):
    return render(request, 'news/stock_news.html', )


def get_sina_news(request):
    data_list = StockNews.objects.filter(platform='新浪', type='1').values_list('time', 'content')
    return render(request, 'news/sina_news.html', {'data': list(data_list)})


def get_east_money_news(request):
    hour_news = StockNews.objects.filter(platform='东方财富', type='1').values_list('time', 'content')
    important_news = StockNews.objects.filter(platform='东方财富', type='2').values_list('time', 'content')
    return render(request, 'news/east_money_news.html',
                  {'hour_news': list(hour_news), 'important_news': list(important_news)})
