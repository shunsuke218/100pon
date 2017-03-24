#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import codecs
import json 
import re

#第3章: 正規表現

#Wikipediaの記事を以下のフォーマットで書き出したファイルjawiki-country.json.gzがある．
#
#1行に1記事の情報がJSON形式で格納される
#各行には記事名が"title"キーに，記事本文が"text"キーの辞書オブジェクトに格納され，そのオブジェクトがJSON形式で書き出される
#ファイル全体はgzipで圧縮される
#以下の処理を行うプログラムを作成せよ．
file = "jawiki-country.json"

#20. JSONデータの読み込み
#Wikipedia記事のJSONファイルを読み込み，「イギリス」に関する記事本文を表示せよ．問題21-29では，ここで抽出した記事本文に対して実行せよ．
print "Q20: "
with open(file,'r') as original:
    for line in original.readlines():
        linejson = json.loads(line)
        if linejson["title"].find("イギリス".decode("utf-8")) > -1:
            text = linejson["text"]
print text

#21. カテゴリ名を含む行を抽出
#記事中でカテゴリ名を宣言している行を抽出せよ．
print "\nQ21: "
print '\n'.join([ line for line in text.split('\n') if line.find("Category:") > -1])
    
#22. カテゴリ名の抽出
#記事のカテゴリ名を（行単位ではなく名前で）抽出せよ．
print "\nQ22: "
for line in text.split('\n'):
    if line.find("Category:") > -1:
        print re.search(r"Category:([^\|\]]*)", line).group(1)

#23. セクション構造
#記事中に含まれるセクション名とそのレベル（例えば"== セクション名 =="なら1）を表示せよ．
print "\nQ23: "
for line in text.split('\n'):
    for result in re.findall("^=.*",line):
        print result, len(re.findall("=", result))/2 - 1

#24. ファイル参照の抽出
#記事から参照されているメディアファイルをすべて抜き出せ．
print "\nQ24: "
for line in text.split('\n'):
    for result in re.findall("\\[[^]]*\\]",line):
        for result in re.findall(u"((?:File:|file:|ファイル:)(.*(?:jpg|jpeg|svg|pdf)))|(http.*pdf)", result):
            print result[1] or result[2]

#25. テンプレートの抽出
#記事中に含まれる「基礎情報」テンプレートのフィールド名と値を抽出し，辞書オブジェクトとして格納せよ．
print "\nQ25: "
temp = re.search(u"{{基礎情報.*}}", text, re.DOTALL).group(0)
a = 100
b = i = 2
while a is not b:
    result = ''.join(temp[0:i])
    a,b = result.count('{{'), result.count('}}')
    i += 1
result = [ item for item in re.split("\n\|", result[2:-2]) if item.count("=")]

dictionary =  dict( item.split(" = ", 1) for item in result )
for key, item in dictionary.iteritems():
    print key + ":    " +  item

#26. 強調マークアップの除去
#25の処理時に，テンプレートの値からMediaWikiの強調マークアップ（弱い強調，強調，強い強調のすべて）を除去してテキストに変換せよ（参考: マークアップ早見表）．
print "\nQ26: "
regex = re.compile(r"(\"|\')+(.+?)(\"|\')+")
dictionary =  dict( item.split(" = ", 1) for item in result )
for key, item in dictionary.iteritems():
    print key + ":    " +  re.sub(regex, "\g<2>",item)

#27. 内部リンクの除去
#26の処理に加えて，テンプレートの値からMediaWikiの内部リンクマークアップを除去し，テキストに変換せよ（参考: マークアップ早見表）．
print "\nQ27: "
regex = re.compile(r"(\"|\'|\[+[^\]]+\||\[)+(.+?)(\"|\'|\])+")
dictionary =  dict( item.split(" = ", 1) for item in result )
for key, item in dictionary.iteritems():
    print key + ":    " +  re.sub(regex, "\g<2>",item)

#28. MediaWikiマークアップの除去
#27の処理に加えて，テンプレートの値からMediaWikiマークアップを可能な限り除去し，国の基本情報を整形せよ．
print "\nQ28: "
regex = re.compile(r"(\"|\'|\[+[^\]]+\||\[|{+[^}]+\||{)+(.+?)(\"|\'|\]|})+", re.DOTALL)
regex2 = re.compile(r"<ref *[^>]*>.+?</ref>|<ref *[^>]*>|<br */>", re.DOTALL)
dictionary =  dict( item.split(" = ", 1) for item in result )
for key, item in dictionary.iteritems():
    print key + ":    " +  re.sub(regex2, "", re.sub(regex, "\g<2>",item))


#29. 国旗画像のURLを取得する
#テンプレートの内容を利用し，国旗画像のURLを取得せよ．（ヒント: MediaWiki APIのimageinfoを呼び出して，ファイル参照をURLに変換すればよい）
print "\nQ29: "
import urllib2, urllib
image = dictionary[u"国旗画像"]
url = "https://commons.wikimedia.org/w/api.php?format=json&action=query&prop=imageinfo&&iiprop=url&titles=File:" + urllib.quote_plus(image)
print re.search(r'{"url":"([^"]*)', urllib2.urlopen( url ).read()).group(1)
