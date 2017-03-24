#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import codecs
import json 
import re

#第4章: 形態素解析

#夏目漱石の小説『吾輩は猫である』の文章（neko.txt）をMeCabを使って形態素解析し，その結果をneko.txt.mecabというファイルに保存せよ．このファイルを用いて，以下の問に対応するプログラムを実装せよ．
#
#なお，問題37, 38, 39はmatplotlibもしくはGnuplotを用いるとよい．
file = "neko.txt.mecab"

#30. 形態素解析結果の読み込み
#形態素解析結果（neko.txt.mecab）を読み込むプログラムを実装せよ．ただし，各形態素は表層形（surface），基本形（base），品詞（pos），品詞細分類1（pos1）をキーとするマッピング型に格納し，1文を形態素（マッピング型）のリストとして表現せよ．第4章の残りの問題では，ここで作ったプログラムを活用せよ．
print "\nQ30: "
#surface	pos,pos1,pos2,*,*,*,base,read,pron
neko = []
sentence = []
with open(file,'r') as original:
    for line in original.readlines():
        if line == "EOS\n":
            neko.append(sentence)
            sentence = []
            continue
        surface, morpheme = line.split('	')
        morpheme = morpheme.split(',')
        tempdict = { \
                     "surface":surface, \
                     "pos": morpheme[0], \
                     "pos1": morpheme[1], \
                     "base": morpheme[-3] \
                     }
        sentence.append(dict(tempdict))
'''
for line in neko:
    print "[ "
    for word in line:
        #print word
        print "    { "
        for key, item in word.iteritems():
            print "        " + key + ":    " +  item
        print "    }"
    print "]"
'''

#31. 動詞
#動詞の表層形をすべて抽出せよ．
print "\nQ31: "
verb = set()
for line in neko:
    for word in line:
        if word["pos"] == "動詞":
            verb.add(word["surface"])
for content in verb:
    print content

#32. 動詞の原形
#動詞の原形をすべて抽出せよ．
print "\nQ32: "
verborig = set()
for line in neko:
    for word in line:
        if word["pos"] == "動詞":
            verborig.add(word["base"])
for content in verborig:
    print content

#33. サ変名詞
#サ変接続の名詞をすべて抽出せよ．
print "\nQ33: "
sahen_noun = set()
for line in neko:
    for word in line:
        if word["pos"] == "名詞" and word["pos1"] == "サ変接続":
            sahen_noun.add(word["surface"])
for content in sahen_noun:
    print content

#34. 「AのB」
#2つの名詞が「の」で連結されている名詞句を抽出せよ．
print "\nQ34: "
meishi_ku = set()
for line in neko:
    length = len(line)
    for index, word in enumerate(line):
        if word["surface"] == "の" and word["pos"] == "助詞":
            try:
                prev = line[index - 1]
                following = line[index + 1]
                if prev["pos"] == "名詞" and following["pos"] == "名詞":
                    meishi_ku.add( prev["surface"] + word["surface"] + following["surface"])
            except:
                pass
for content in meishi_ku:
    print content

#35. 名詞の連接
#名詞の連接（連続して出現する名詞）を最長一致で抽出せよ．
print "\nQ35: "
meishi_rensetsu = set()
for line in neko:
    length = len(line)
    for index, word in enumerate(line):
        if word["pos"] == "名詞":
            try:
                prev = line[index - 1]
                following = line[index + 1]
                if prev["pos"] != "名詞" and following["pos"] == "名詞":
                    temp = word["surface"]
                    while following["pos"] == "名詞":
                        temp += following["surface"]
                        index += 1
                        try:
                            following = line[index + 1]
                        except:
                            pass
                        finally:
                            meishi_rensetsu.add(temp)
            except:
                pass
for content in meishi_rensetsu:
    print content


#36. 単語の出現頻度
#文章中に出現する単語とその出現頻度を求め，出現頻度の高い順に並べよ．
print "\nQ36: "
from collections import Counter
all_words = []
for line in neko:
    for word in line:
        all_words.append(word["surface"])
frequent = Counter(all_words)
for word, number in frequent.most_common():
    print str(number) + ":    " + word

#37. 頻度上位10語
#出現頻度が高い10語とその出現頻度をグラフ（例えば棒グラフなど）で表示せよ．
print "\nQ37: "
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot, draw, show
from matplotlib.font_manager import FontProperties

font_path = '/usr/share/fonts/truetype/takao-gothic/TakaoPGothic.ttf'
font_prop = FontProperties(fname=font_path)
matplotlib.rcParams['font.family'] = font_prop.get_name()

#label = []
#total = []
label = [word[0].decode('utf-8') for word in frequent.most_common(10)]
total = [word[1] for word in frequent.most_common(10)]
width = [i for i in range(10)]
'''
for word, number in frequent.most_common(10):
    print word.decode('utf-8')
    label.append(word.decode('utf-8'))
    total.append(number)
'''
#np.array(number)
plt.bar(width, total)
plt.xticks(width, label)
draw()
show()

#なお，問題37, 38, 39はmatplotlibもしくはGnuplotを用いるとよい．


#38. ヒストグラム
#単語の出現頻度のヒストグラム（横軸に出現頻度，縦軸に出現頻度をとる単語の種類数を棒グラフで表したもの）を描け．

#39. Zipfの法則
#単語の出現頻度順位を横軸，その出現頻度を縦軸として，両対数グラフをプロットせよ．
