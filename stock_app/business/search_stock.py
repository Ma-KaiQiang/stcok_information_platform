import json
import time
import tushare as ts
import requests
from jsonpath import jsonpath
from pyecharts.charts import Kline, Line, Bar, Grid
from pyecharts import options as opts

KEY = '33v2UrxJXsip5CLyfNp2EBtC9X'
TUSHARETOKEN = '4c8c3409afee26594afad81a05e8ab044a8b7958c27a6613fc9fe41f'


class TuShareApi():
    def __init__(self):
        ts.set_token(TUSHARETOKEN)
        self.pro = ts.pro_api()

    def get_stock_list(self):
        data = self.pro.query(api_name='stock_basic', exchange='', fields='symbol,name,area,industry,list_date')
        data.reset_index(inplace=True)
        stock_data_list = data[['symbol', 'name', 'area', 'industry', 'list_date']].to_dict()
        code = stock_data_list.get('symbol')
        name = stock_data_list.get('name')
        area = stock_data_list.get('area')
        industry = stock_data_list.get('industry')
        list_date = stock_data_list.get('list_date')
        l = []
        for i in code:
            l.append([code.get(i), name.get(i), area.get(i), industry.get(i), list_date.get(i)])
        return l

    def get_stock_data(self, code, days, start_date=None, end_date=None):
        df = ts.get_hist_data(code, start=start_date, end=end_date)
        df_time = df[:days]
        mydate = df_time.index.tolist()
        kdata = df_time[['open', 'close', 'low', 'high']].values.tolist()
        madata_5 = df_time['ma5'].values.tolist()
        madata_10 = df_time['ma10'].values.tolist()
        madata_20 = df_time['ma20'].values.tolist()
        volume_rise = [df_time.volume[x] if df_time.close[x] > df_time.open[x] else "0" for x in
                       range(0, len(df_time.index))]
        volume_drop = [df_time.volume[x] if df_time.close[x] <= df_time.open[x] else "0" for x in
                       range(0, len(df_time.index))]
        d = {'mydate': mydate[::-1],
             'kdata': kdata[::-1],
             'madata_5': madata_5[::-1],
             'madata_10': madata_10[::-1],
             'madata_20': madata_20[::-1],
             'volume_rise': volume_rise[::-1],
             'volume_drop': volume_drop[::-1]
             }
        return d

    def moving_average_chart(self, mydate, data_5, data_10, data_20, name) -> Line:
        moving_average = (
            Line()
            .add_xaxis(mydate)
            .add_yaxis("ma5", data_5, is_smooth=True)
            .add_yaxis("ma10", data_10, is_smooth=True)
            .add_yaxis("ma20", data_20, is_smooth=True)
            .set_global_opts(title_opts=opts.TitleOpts(title="%s-移动平均线" % name),
                             datazoom_opts=[opts.DataZoomOpts()],
                             )
            .set_series_opts(
                label_opts=opts.LabelOpts(is_show=False),
            )
        )
        return moving_average
        # 成交量

    def volume_chart(self, mydate, volume_rise, volume_drop, name) -> Bar:
        bar = (
            Bar()
            .add_xaxis(mydate)
            .add_yaxis("volume_rise", volume_rise, stack=True, color=["#ec0000"])
            .add_yaxis("volume_drop", volume_drop, stack=True, color=["#00da3c"])
            .set_global_opts(title_opts=opts.TitleOpts(title="%s-成交量" % name),
                             datazoom_opts=[opts.DataZoomOpts()], )
            .set_series_opts(
                label_opts=opts.LabelOpts(is_show=False),
            )
        )
        return bar

    # K 线图
    def kline_base(self, mydate, data, name) -> Kline:
        kline = (
            Kline()
            .add_xaxis(mydate)
            .add_yaxis("%s" % name, data, markpoint_opts=opts.MarkLineOpts(
                data=[opts.MarkLineItem(type_="max", value_dim="close")]
            ), markline_opts=opts.MarkLineOpts(
                data=[opts.MarkLineItem(type_="max", value_dim="close")]
            ),
                       itemstyle_opts=opts.ItemStyleOpts(
                           color="#ec0000",
                           color0="#00da3c",
                           border_color="#8A0000",
                           border_color0="#008F28",
                       ),
                       )
            .set_global_opts(
                yaxis_opts=opts.AxisOpts(is_scale=True,
                                         splitarea_opts=opts.SplitAreaOpts(
                                             is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                                         ),
                                         ),
                xaxis_opts=opts.AxisOpts(is_scale=True,
                                         axislabel_opts=opts.LabelOpts(rotate=-30)),
                title_opts=opts.TitleOpts(title="股票走势"),
                datazoom_opts=[opts.DataZoomOpts()],
                toolbox_opts=opts.ToolboxOpts(is_show=True)
            ).dump_options_with_quotes()
        )
        return kline

    # full chart
    def full_chart(self, mydate, kdata, data_5, data_10, data_20, volume_rise, volume_drop, name):
        kline = (
            Kline()
            .add_xaxis(mydate)
            .add_yaxis("%s" % name, kdata, markpoint_opts=opts.MarkLineOpts(
                data=[opts.MarkLineItem(type_="max", value_dim="close")]
            ), markline_opts=opts.MarkLineOpts(
                data=[opts.MarkLineItem(type_="max", value_dim="close")]
            ),
                       itemstyle_opts=opts.ItemStyleOpts(
                           color="#ec0000",
                           color0="#00da3c",
                           border_color="#8A0000",
                           border_color0="#008F28",
                       ),
                       )
            .set_global_opts(
                yaxis_opts=opts.AxisOpts(is_scale=True,
                                         splitarea_opts=opts.SplitAreaOpts(
                                             is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                                         ),
                                         ),
                xaxis_opts=opts.AxisOpts(is_scale=True,
                                         axislabel_opts=opts.LabelOpts(rotate=-30)),
                title_opts=opts.TitleOpts(title="股票走势"),
                datazoom_opts=[opts.DataZoomOpts(xaxis_index=[0, 1])],
                toolbox_opts=opts.ToolboxOpts(is_show=True),
                legend_opts=opts.LegendOpts(pos_left="20%")
            )
        )
        line = (
            Line()
            .add_xaxis(mydate)
            .add_yaxis("5日线", data_5, is_smooth=True)
            .add_yaxis("10日线", data_10, is_smooth=True)
            .add_yaxis("20日线", data_20, is_smooth=True)
            .set_global_opts(title_opts=opts.TitleOpts(title="移动平均线"))
            .set_series_opts(
                label_opts=opts.LabelOpts(is_show=False),
            )
        )
        bar = (
            Bar()
            .add_xaxis(mydate)
            .add_yaxis("volume_rise", volume_rise, stack=True, color=["#ec0000"], )
            .add_yaxis("volume_drop", volume_drop, stack=True, color=["#00da3c"], )
            .set_global_opts(title_opts=opts.TitleOpts(),
                             legend_opts=opts.LegendOpts(pos_right="20%"))
            .set_series_opts(
                label_opts=opts.LabelOpts(is_show=False),
            )
        )

        overlap_kline_line = kline.overlap(line)
        grid = Grid()
        grid.add(
            overlap_kline_line,
            grid_opts=opts.GridOpts(pos_left="10%", pos_right="8%", height="50%"),
        )
        grid.add(
            bar,
            grid_opts=opts.GridOpts(
                pos_left="10%", pos_right="8%", pos_top="70%", height="16%"
            ),
        )
        return grid


def json_parse(data, value='data'):
    data_ = jsonpath(data, f'$..{value}')
    return data_


def search_stock_code(code):
    result = requests.post(url='http://stock.salefx.cn:10000/api/stock/realTime', data={'key': KEY, 'codes': code})
    data = json_parse(result.json())
    return data[0].get(code)


def stock_real_time(codes: list):
    code_str = ','.join(codes)
    result = requests.post(url='http://stock.salefx.cn:10000/api/stock/realTime',
                           data={'key': KEY, 'codes': code_str})
    data = json_parse(result.json())[0]
    if isinstance(data, str):
        data = json.loads(data)
    stock_info_l = [[data[s].get('code'),
                     data[s].get('name'),
                     data[s].get('open'),
                     data[s].get('high'),
                     data[s].get('low'),
                     data[s].get('price'),
                     data[s].get('pchange')] for s
                    in codes]
    return stock_info_l


def stock_manage(codes: list):
    code_str = ','.join(codes)
    result = requests.post(url='http://stock.salefx.cn:10000/api/stock/realTime',
                           data={'key': KEY, 'codes': code_str})
    data = json_parse(result.json())[0]
    if isinstance(data, str):
        data = json.loads(data)
    stock_info_l = []
    for code in codes:
        s = stock_pressure_support(code)
        stock_info_l.append([data[code].get('code'), data[code].get('name')] + s)
    return stock_info_l


def stock_pressure_support(code):
    response = requests.post(url='http://stock.salefx.cn:10000/api/stock/pressureSupport',
                             params={'code': code, 'key': KEY})
    time.sleep(1.5)
    data = json_parse(response.json())[0]
    print(data, 55)
    l = [data.get('ylw'), data.get('zcw', ''), data.get('zsw', ''), data.get('zyw', ''),
         data.get('opinions_of_investment', '')]

    return l


def stock_to_be_raised():
    from datetime import datetime
    date = datetime.now().strftime('%Y%m%d')
    response = requests.get(url='http://stock.salefx.cn:10000/api/stock/toBeRaised',
                            params={'date': date, 'key': KEY})
    stock_data = json_parse(response.json(), 'stockData')[0]
    data = [d.update({'change': round(d.get('change') * 100, 2)}) for d in stock_data]

    # stock_data_list = [[d.get('name'), d.get('price'), d.get('buyDays'), d.get('cBuyDays'), round(d.get('change')*100,2)] for d in
    #                    stock_data]
    return stock_data


def tt():
    df = ts.pro_api('000001')
    return df


if __name__ == '__main__':
    a = TuShareApi()
    print(a.get_stock_data(code='000001', days=30))
