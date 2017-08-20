# coding: utf-8

import json
import xlrd

filepath = u'/Users/xiaoshuidi/Downloads/副本水滴数据2.xlsx'
filepath = u'/data/srv/caspain/副本水滴数据2.xlsx'

wb = xlrd.open_workbook(filepath)
sheet = wb.sheet_by_name(u'好房在库的水滴房源')
values = sheet.col_values(5)
phones = set([str(int(v)) for v in values[1:]])


# 校验手机是否存在
from django.contrib.auth.models import User
from db.models import UserProfile, Employer

noexists = []
for phone in phones:
    u = UserProfile.objects.filter(phone=phone).first()
    if u: print phone, u.id, u.name, u.company, u.created_at
    else: noexists.append(phone)



# volga
from openchannels.models import ShowRooms, ShowHouses

shuidi_ids = []
for obj in ShowRooms.objects.filter(is_delete=False, channel=3):
    room = obj.room
    apartment = room.apartment
    shuidi_id = '{}{}'.format(apartment.id, room.id)
    shuidi_ids.append(shuidi_id)


import json
with open('/home/ubuntu/volga_shuidi_ids.json', 'wb') as f:
    json.dump(shuidi_ids, f)


# caspain
from openchannels.models import ShowRooms, ShowHouses

shuidi_ids = []
for obj in ShowRooms.objects.filter(is_delete=False, channel=3):
    room = obj.room
    house = room.house
    shuidi_id = str(house.id)
    shuidi_ids.append(shuidi_id)


import json
with open('/home/ubuntu/caspain_shuidi_ids.json', 'wb') as f:
    json.dump(shuidi_ids, f)


cids = shuidi_ids


with open('/home/ubuntu/volga_shuidi_ids.json', 'rb') as f:
    vids = json.load(f)

vids = set([str(v) for v in vids])
cids = set(cids)
same = cids & vids
print len(same)

result = set(cids)
result.update(vids)
len(result)

values = sheet.col_values(0)
pingan_ids = set([str(int(v)) for v in values[1:]])


same = pingan_ids & result
print len(same)
diff = pingan_ids.difference(result)
print len(diff)

