#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import sys
import types
import re

#00. 文字列の逆順
#文字列"stressed"の文字を逆に（末尾から先頭に向かって）並べた文字列を得よ．
print "Q00: "
string = "stressed"
print string[::-1]

#01. 「パタトクカシーー」
#「パタトクカシーー」という文字列の1,3,5,7文字目を取り出して連結した文字列を得よ．
print "\nQ01: "
string = u"パタトクカシーー"
#print ''.join([ j for (i,j) in enumerate(string) if i % 2 is 1])
print ''.join(list(string)[1:len(string):2]) # Like this better.


#02. 「パトカー」＋「タクシー」＝「パタトクカシーー」
#「パトカー」＋「タクシー」の文字を先頭から交互に連結して文字列「パタトクカシーー」を得よ．
print "\nQ02: "
string_1 = u"パトカー"
string_2 = u"タクシー"
print ''.join([ a+b for a,b in zip(string_1,string_2) ])

#03. 円周率
#"Now I need a drink, alcoholic of course, after the heavy lectures involving quantum mechanics."という文を単語に分解し，各単語の（アルファベットの）文字数を先頭から出現順に並べたリストを作成せよ．
print "\nQ03: "
string = "Now I need a drink, alcoholic of course, after the heavy lectures involving quantum mechanics."
print [ str(len(a)) for a in re.split(r'[^a-zA-Z]+',string) ]

#04. 元素記号
#"Hi He Lied Because Boron Could Not Oxidize Fluorine. New Nations Might Also Sign Peace Security Clause. Arthur King Can."という文を単語に分解し，1, 5, 6, 7, 8, 9, 15, 16, 19番目の単語は先頭の1文字，それ以外の単語は先頭に2文字を取り出し，取り出した文字列から単語の位置（先頭から何番目の単語か）への連想配列（辞書型もしくはマップ型）を作成せよ．
print "\nQ04: "
string = "Hi He Lied Because Boron Could Not Oxidize Fluorine. New Nations Might Also Sign Peace Security Clause. Arthur King Can."
numlist = [1, 5, 6, 7, 8, 9, 15, 16, 19]
print {n: a[:1] if n in numlist else a[:2] for (n,a) in enumerate(string.split(' '), 1)}

#05. n-gram
#与えられたシーケンス（文字列やリストなど）からn-gramを作る関数を作成せよ．この関数を用い，"I am an NLPer"という文から単語bi-gram，文字bi-gramを得よ．
print "\nQ05: "
string = "I am an NLPer"
def ngram(string, mode="word"):
    list = string.split(' ') if mode == "word" else string
    return zip(list, list[1:])
print ngram(string)
print ngram(string, "char")

#06. 集合
#"paraparaparadise"と"paragraph"に含まれる文字bi-gramの集合を，それぞれ, XとYとして求め，XとYの和集合，積集合，差集合を求めよ．さらに，'se'というbi-gramがXおよびYに含まれるかどうかを調べよ．
print "\nQ06: "
string1 = "paraparaparadise"
string2 = "paragraph"
X = ngram(string1, "char")
Y = ngram(string2, "char")
print "X: ", X
print "Y: ", Y
print "Sum: ", X + Y
print "Intersection: ", [bigram for bigram in X if bigram in set(Y)]
print "Difference: ", set(X) - set(Y)
print "X contains 'se'" if ('s','e') in X else "", "Y contains 'se'" if ('s','e') in Y else ""

#07. テンプレートによる文生成
#引数x, y, zを受け取り「x時のyはz」という文字列を返す関数を実装せよ．さらに，x=12, y="気温", z=22.4として，実行結果を確認せよ．
print "\nQ07: "
def create_string(x, y, z):
    print str(x) + "時の" + str(y) + "は" + str(z)
create_string(x=12, y="気温", z=22.4)

#08. 暗号文
#与えられた文字列の各文字を，以下の仕様で変換する関数cipherを実装せよ．
#
#英小文字ならば(219 - 文字コード)の文字に置換
#その他の文字はそのまま出力
#この関数を用い，英語のメッセージを暗号化・復号化せよ．
print "\nQ08: "
def cipher(string):
    return ''.join([ chr(219 - ord(char)) if char.islower() else char for char in string ])
string = "Original message"
print string + ": " + string + "\nCiphered: " + cipher(string) + "\nDe-ciphered: " + cipher(cipher(string))

#09. Typoglycemia
#スペースで区切られた単語列に対して，各単語の先頭と末尾の文字は残し，それ以外の文字の順序をランダムに並び替えるプログラムを作成せよ．ただし，長さが４以下の単語は並び替えないこととする．適当な英語の文（例えば"I couldn't believe that I could actually understand what I was reading : the phenomenal power of the human mind ."）を与え，その実行結果を確認せよ．
print "\nQ09: "
import random
string = "I couldn't believe that I could actually understand what I was reading : the phenomenal power of the human mind ."
result = []
for word in string.split(" "):
    mixed = word[0] + ''.join(random.sample(word[1:-1],len(word)-2)) + word[-1] if len(word) > 4 else word
    result.append(mixed)
print ' '.join(result)

