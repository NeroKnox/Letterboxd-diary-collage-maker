# -*- coding:utf-8 -*-
ranges = [
  {"from": ord(u"\u3300"), "to": ord(u"\u33ff")},         # compatibility ideographs
  {"from": ord(u"\ufe30"), "to": ord(u"\ufe4f")},         # compatibility ideographs
  {"from": ord(u"\uf900"), "to": ord(u"\ufaff")},         # compatibility ideographs
  {"from": ord(u"\U0002F800"), "to": ord(u"\U0002fa1f")}, # compatibility ideographs
  {'from': ord(u'\u3040'), 'to': ord(u'\u309f')},         # Japanese Hiragana
  {"from": ord(u"\u30a0"), "to": ord(u"\u30ff")},         # Japanese Katakana
  {"from": ord(u"\u2e80"), "to": ord(u"\u2eff")},         # cjk radicals supplement
  {"from": ord(u"\u4e00"), "to": ord(u"\u9fff")},
  {"from": ord(u"\u3400"), "to": ord(u"\u4dbf")},
  {"from": ord(u"\U00020000"), "to": ord(u"\U0002a6df")},
  {"from": ord(u"\U0002a700"), "to": ord(u"\U0002b73f")},
  {"from": ord(u"\U0002b740"), "to": ord(u"\U0002b81f")},
  {"from": ord(u"\U0002b820"), "to": ord(u"\U0002ceaf")}  # included as of Unicode 8.0
]

def is_cjk(char):
  return any([range["from"] <= ord(char) <= range["to"] for range in ranges])

def has_cjk(string):
  i = 0
  while i<len(string):
    if is_cjk(string[i]):
      return True
    i += 1
  return False

from langdetect import detect, DetectorFactory
DetectorFactory.seed = 0
from guess_language import guess_language


juon = '呪怨'
idi_smotri = 'Иди и смотри'
parasite = '기생충'
chungking = '重慶森林'
shutter = 'ชัตเตอร์ กดติดวิญญาณ'
RRR = 'రౌద్రం రణం రుధిరం'
khrustaliov = 'Хрусталёв, машину!'
stalker = 'Сталкер'
roublev = 'Андрей Рублёв'
m = 'M - Eine Stadt sucht einen Mörder'
berlin = 'Der Himmel über Berlin'
boot = 'Das Boot'
welle = 'Die Welle'

print(guess_language(welle))

