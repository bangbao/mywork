# coding: utf-8

import json
import datetime
import codecs


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


def json_dumps(data, **kwargs):
    """json.dumps数据
    """
    kwargs['cls'] = ComplexEncoder
    if 'ensure_ascii' not in kwargs:
        kwargs['ensure_ascii'] = False
    return json.dumps(data, **kwargs)


def json_loads(data, **kwargs):
    """json.loads数据
    """
    return json.loads(data, **kwargs)


def zfill_list_by_separate_string(s, length=0, func=str, default=None,
                                  skip_empty=True, separate=','):
    """根据分隔符生成指定长度的列表
    """
    if not length:
        zlist = [f for f in s.split(separate) if f or not skip_empty]
        return zlist

    zlist = [default for _ in xrange(length)]
    slist = s.split(separate)
    for idx, f in enumerate(slist):
        if idx >= length:
            break
        if not f and skip_empty:
            continue
        zlist[idx] = func(f)
    return zlist


def gen_csv_data(datalist):
    """
    生成 csv 编码及格式的数据
    :return:
    """
    data = codecs.BOM_UTF8
    for line in datalist:
        rows = ''
        for row in line:
            if row and ',' in str(row) or ('\n' in str(row)):
                row = '\"' + row + '\"'
            rows += unicode(row).encode('utf-8') + ',' if row else ','
        if rows[-1] == ',':
            rows = rows[:-1]
        data += rows + '\n'

    return data
