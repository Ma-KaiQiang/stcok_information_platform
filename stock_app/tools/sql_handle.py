# -*- coding: utf-8 -*-
'''
@Time    : 2020/12/16 10:24
@Author  : MaKaiQiang
@File    : pymysql
'''
import pymysql

from colorama import Fore, init

init(autoreset=True)


class PyMysql:

    def __init__(self):
        self.conn = pymysql.connect(host='localhost', port=3306, user='root', password='123456',
                                    database='gato_cloud_release_03')
        self.cursor = self.conn.cursor()

    def add(self, table, fields, values, row=None):
        '''
        :param table:数据库表
        :param fields: 字段list
        :param values: 值list
        :return:
        '''
        try:
            if row:
                sql = f'insert into {table} ({fields}) values(%s) where id ={row}'
            else:
                sql = f'insert into {table} ({fields}) values(%s) '
            self.cursor.executemany(sql, tuple(values))
            # list(map(lambda text: self.cursor.execute(text), map(lambda value: f'insert into {table} ({fields}) VALUES ("{(value)}");', values)))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()

    def select(self, table, field, condition=False):
        try:
            if condition:
                key = list(condition.keys())[0]
                value = list(condition.values())[0]
                text = f'select {field} from {table} where {key}="{value}"'
            else:
                text = f'select {field} from {table} where {field} is not null '
            self.cursor.execute(text)
            data = self.cursor.fetchall()
            data = list(map(lambda x: x[0], data))

            return data
        except Exception as e:
            print(f'{table}表查询数据错误：{e}')
            return False

    def modify(self, table, fields, values):
        try:
            if self.field_is_exists(table, fields):
                sql = f'UPDATE {table} SET {fields} = (%s) WHERE id = (%s)'
                self.cursor.executemany(sql, tuple(values))
                self.conn.commit()
                print(Fore.GREEN + '-' * 81 + ' Storage ' + '-' * 81)
                for v in values:
                    print(Fore.YELLOW + f'* {v[0]} update to table "{table}" index = {v[1]} field = "{fields}"')
            else:
                raise
        except Exception as e:
            self.conn.rollback()
            print(f'{table}表插入数据错误：{e}')

    def delete(self, table):
        try:
            text = f'delete from {table};'
            self.cursor.execute(text)
            self.conn.commit()
        except Exception as e:
            print(f'清空{table}表中数据出错:{e}')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':
    with PyMysql() as p:
        c = p.select('t_attendance', "staffId", {"staffName": "萧瑞"})
        print(c)
