#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import codecs
import json 
import re


#第6章: 英語テキストの処理
#
#英語のテキスト（nlp.txt）に対して，以下の処理を実行せよ．
file = "nlp.txt"

#50 文区切り
#(. or ; or : or ? or !) → 空白文字 → 英大文字というパターンを文の区切りと見なし，入力された文書を1行1文の形式で出力せよ．
print "Q50:"
with open(file, 'r') as input:
    raw_input = input.read().rsplit('\n')
    sentences = []
    for each_line in raw_input:
        if len(re.findall("[\.;:\?!]+\s", each_line)) is 0:
            sentences.append(each_line)
            continue
        sentences += [ each for each in re.findall("[^\.;:\?!]+[\.;:\?!](?=\s+[A-Z]|$)", each_line) ]

    for sentence in sentences:
        print sentence

#51 単語の切り出し
#空白を単語の区切りとみなし，50の出力を入力として受け取り，1行1単語の形式で出力せよ．ただし，文の終端では空行を出力せよ．
print "\nQ51:"
for sentence in sentences:
    for word in sentence.split(' '):
        print word

#52 ステミング
#51の出力を入力として受け取り，Porterのステミングアルゴリズムを適用し，単語と語幹をタブ区切り形式で出力せよ． Pythonでは，Porterのステミングアルゴリズムの実装としてstemmingモジュールを利用するとよい．
print "\nQ52:"
from stemming.porter2 import stem
for sentence in sentences:
    for word in sentence.split(' '):
        print word + '\t' + stem(word)


#53. Tokenization
#Stanford Core NLPを用い，入力テキストの解析結果をXML形式で得よ．また，このXMLファイルを読み込み，入力テキストを1行1単語の形式で出力せよ．
print "\nQ53:"
from pycorenlp import StanfordCoreNLP
from xml.etree import ElementTree as Etree

nlp = StanfordCoreNLP('http://localhost:9000')
#java -mx5g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -timeout 10000
properties={
    'timeout': '50000',
    'annotators': 'tokenize,ssplit,lemma,pos,ner,parse',
    'outputFormat': 'xml'
}
'''
# Merge all outputs to one
for first, sentence in enumerate(sentences):
    data = Etree.fromstring(nlp.annotate(sentence, properties))
    if not first:
        result = data
    else:
        result.extend(data)

# Save file
with open("q53.xml", 'w') as output:
    output.write(Etree.tostring(result))
'''
# Now load the file
xml = Etree.parse("q53.xml").getroot()
for element in xml.getiterator("word"):
    print element.text

    
#54. 品詞タグ付け
#Stanford Core NLPの解析結果XMLを読み込み，単語，レンマ，品詞をタブ区切り形式で出力せよ．
print "\nQ54:"
for element in xml.getiterator("token"):
    print element.find("word").text + '\t' + element.find("lemma").text + '\t' + element.find("POS").text

#55. 固有表現抽出
#入力文中の人名をすべて抜き出せ．
print "\nQ55:"
for element in xml.getiterator("token"):
    if element.find("NER").text == "PERSON":
        print element.find("word").text

#56. 共参照解析
#Stanford Core NLPの共参照解析の結果に基づき，文中の参照表現（mention）を代表参照表現（representative mention）に置換せよ．ただし，置換するときは，「代表参照表現（参照表現）」のように，元の参照表現が分かるように配慮せよ．
print "\nQ56:"

properties={
    'timeout': '50000',
    'annotators': 'tokenize, ssplit, pos, lemma, ner, parse, dcoref',
    'outputFormat': 'xml'
}


import xml.dom.minidom

# Merge all outputs to one
for first, sentence in enumerate(sentences):
    data = nlp.annotate(sentence, properties)
    if len(re.findall("mention", data)) > 0:
        print '\n##################################################\n',first, sentence#, data

        #xml = xml.dom.minidom.parseString(data)
        #print xml.toprettyxml()
        data = Etree.fromstring(data)
        print data
    '''
    if not first:
        result = data
    else:
        result.extend(data)
# Save file
with open("q56.xml", 'w') as output:
    output.write(Etree.tostring(result))

    
xml = Etree.parse("q56.xml").getroot()
print xml.tag
for child in xml:
    print child.tag
for element in xml.findall("sentence"):
    print element.tag
'''
    
'''
print "\nQ56:"
xml = Etree.parse("q56.xml").getroot()
for element in xml.findall("sentence"):
    print element
# Now load the file
#for element in xml.getiterator("sentence"):
#for element in xml.iter("sentence"):
#for element in xml.find("sentence"):
#    print element.text

#57. 係り受け解析
#Stanford Core NLPの係り受け解析の結果（collapsed-dependencies）を有向グラフとして可視化せよ．可視化には，係り受け木をDOT言語に変換し，Graphvizを用いるとよい．また，Pythonから有向グラフを直接的に可視化するには，pydotを使うとよい．
print "\nQ57:"

#58. タプルの抽出
#Stanford Core NLPの係り受け解析の結果（collapsed-dependencies）に基づき，「主語 述語 目的語」の組をタブ区切り形式で出力せよ．ただし，主語，述語，目的語の定義は以下を参考にせよ．
print "\nQ58:"

#述語: nsubj関係とdobj関係の子（dependant）を持つ単語
#主語: 述語からnsubj関係にある子（dependent）
#目的語: 述語からdobj関係にある子（dependent）
#59. S式の解析
#Stanford Core NLPの句構造解析の結果（S式）を読み込み，文中のすべての名詞句（NP）を表示せよ．入れ子になっている名詞句もすべて表示すること．


print "\nQ59:"
'''
