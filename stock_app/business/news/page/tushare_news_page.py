from stock_app.business.news.base.page_object import NewPageElement


class TuSharePage(object):
    '''
    页面元素管理
    '''

    def __init__(self, webdriver):
        self.driver = webdriver

    user = NewPageElement(id_='login-account', describe='账号')
    password = NewPageElement(id_='login-password', describe='密码')
    captcha_img = NewPageElement(id_='login-captcha-img', describe='验证码图片')
    captcha = NewPageElement(id_='login-captcha', describe='验证码')
    login = NewPageElement(id_='login-btn', describe='登录按钮')
    login_info = NewPageElement(xpath='//*[@id="login-common-info"]/label', describe='登录信息')

    news_data = NewPageElement(xpath='//*[@id="navigation"]/li[4]/a', describe='资讯数据')
    sina_A = NewPageElement(xpath='//*[@id="chan_10"]', describe='新浪A股')
    sina_A_news_content = NewPageElement(xpath='//*[@id="news_10"]//div[@class="news_content"]', describe='新浪A股新闻',
                                         index='n')
    sina_A_news_time = NewPageElement(xpath='//*[@id="news_10"]//div[@class="news_datetime"]',
                                      describe='新浪A股新闻时间', index='n')
    east_money = NewPageElement(xpath='//*[@id="data_source_head"]/span[2]/a', describe='东方财富')
    east_money_24hour = NewPageElement(xpath='//*[@id="chan_102"]', describe='东方财富全球24小时新闻')
    east_money_important_news = NewPageElement(xpath='//*[@id="chan_101"]', describe='东方财富要闻')
    east_money_24hour_time = NewPageElement(xpath='//*[@id="news_102"]//div[@class="news_datetime"]',
                                            describe='东方财富24小时新闻时间', index='n')
    east_money_24hour_content = NewPageElement(xpath='//*[@id="news_102"]//div[@class="news_content"]',
                                               describe='东方财富24小时新闻内容', index='n')
    east_money_world_time = NewPageElement(xpath='//*[@id="news_101"]//div[@class="news_datetime"]',
                                           describe='东方财富全球新闻时间', index='n')
    east_money_world_content = NewPageElement(xpath='//*[@id="news_101"]//div[@class="news_content"]',
                                              describe='东方财富全球新闻内容', index='n')
