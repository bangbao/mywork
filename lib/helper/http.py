# coding: utf-8

import json
from django.http import HttpResponse
from .serializer import gen_csv_data


def JsonResponse400(msg):
    resp = {'status': False,
            'msg': msg,
            'errors': {'detail': msg}}
    return json_response(resp, 400)


def json_response(data, status=200):
    """ Return json response
    """
    response = HttpResponse(json.dumps(data, ensure_ascii=False),
                            content_type='application/json; charset=utf-8',
                            status=status)
    return response


def csv_response(data, filename):
    """生成csv格式的文件下载
    """
    if isinstance(filename, unicode):
        filename = filename.encode('utf-8')
    csv_data = gen_csv_data(data)
    response = HttpResponse(csv_data, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % filename
    return response
