#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import codecs
import json 
import re

#第5章: 係り受け解析

#夏目漱石の小説『吾輩は猫である』の文章（neko.txt）をCaboChaを使って係り受け解析し，その結果をneko.txt.cabochaというファイルに保存せよ．このファイルを用いて，以下の問に対応するプログラムを実装せよ．
file = "neko.txt.cabocha"

#40. 係り受け解析結果の読み込み（形態素）
#形態素を表すクラスMorphを実装せよ．このクラスは表層形（surface），基本形（base），品詞（pos），品詞細分類1（pos1）をメンバ変数に持つこととする．さらに，CaboChaの解析結果（neko.txt.cabocha）を読み込み，各文をMorphオブジェクトのリストとして表現し，3文目の形態素列を表示せよ．
print "\nQ40: "
class Morph():
    def __init__(self, surface, base, pos, pos1):
        self.surface = surface
        self.base = base
        self.pos = pos
        self.pos1 = pos1
    def __str__(self):
        return "[ " + self.surface + ", " +  self.pos + ", " +  self.pos1 + ", " + self.base + " ]"

neko = []
sentence = []
with open(file,'r') as original:
    for line in original.readlines():
        if line == "EOS\n":
            neko.append(sentence)
            sentence = []
            continue
        elif line.count("\t") is 0:
            continue
        surface, morpheme = line.split('\t')
        morpheme = morpheme.split(',')
        sentence.append(Morph(surface, morpheme[-3], morpheme[0], morpheme[1]))

for morph in neko[2]:
    print morph
    
#41. 係り受け解析結果の読み込み（文節・係り受け）
#40に加えて，文節を表すクラスChunkを実装せよ．このクラスは形態素（Morphオブジェクト）のリスト（morphs），係り先文節インデックス番号（dst），係り元文節インデックス番号のリスト（srcs）をメンバ変数に持つこととする．さらに，入力テキストのCaboChaの解析結果を読み込み，１文をChunkオブジェクトのリストとして表現し，8文目の文節の文字列と係り先を表示せよ．第5章の残りの問題では，ここで作ったプログラムを活用せよ．
print "\nQ41: "
class Chunk():
    reference = {}
    def __init__(self):
        self.morphs = []
        self.dst = -1
        self.srcs = []
        self.index = -1
    def __str__(self):
        return "[ " + ''.join([ str(morph) for morph in self.morphs]) + ", " + str(self.index) + ", " +  str(self.dst) + ", " + str(self.srcs) + " ]"

neko = []
sentence = [] # Chunk will be thrown here.
with open(file,'r') as original:
    for line in original.readlines():
        if line == "EOS\n":
            [ target.srcs.append(origin.index) \
              for origin in sentence \
              for target in sentence \
              if origin.dst is target.index ]
            neko.append(sentence)
            sentence = []
        elif line.count("\t") is 0:
            chunk = Chunk()
            chunk.index = int(line.split()[1])
            chunk.dst = int(line.split()[2].replace('D',''))
            sentence.append(chunk)
        else:
            surface, morpheme = line.split('\t')
            morpheme = morpheme.split(',')
            sentence[-1].morphs.append(Morph(surface, morpheme[-3], morpheme[0], morpheme[1]))

for chunk in neko[7]:
        print chunk
        

#42. 係り元と係り先の文節の表示
#係り元の文節と係り先の文節のテキストをタブ区切り形式ですべて抽出せよ．ただし，句読点などの記号は出力しないようにせよ．
'''
neko (list)
 └ sentences (list)
   └ chunk (object)
      └ index
      └ dst
      └ srcs
      └ morphs (list)
         └ surface, base, pos, pos1
'''
print "\nQ42: "
for sentence in neko[7:8]:
    for chunk in sentence:
        join_surfaces = lambda tmp_chunk: ''.join([ tmp.surface for tmp in tmp_chunk.morphs if tmp.pos != "記号"])
        origin = join_surfaces(chunk)
        target = join_surfaces(sentence[chunk.dst])
        if origin != "" and target != "":
            print origin + '\t' + target

#43. 名詞を含む文節が動詞を含む文節に係るものを抽出
#名詞を含む文節が，動詞を含む文節に係るとき，これらをタブ区切り形式で抽出せよ．ただし，句読点などの記号は出力しないようにせよ．
print "\nQ43: "
def contain_postype(chunk, postype):
    for tmp in chunk.morphs:
        if tmp.pos == postype:
            return True
    else:
        return False
    
for sentence in neko[7:8]:
    for chunk in sentence:
        join_surfaces = lambda tmp_chunk: ''.join([ tmp.surface for tmp in tmp_chunk.morphs if tmp.pos != "記号"])
        origin = join_surfaces(chunk) if contain_postype(chunk, "名詞") else ""
        target = join_surfaces(sentence[chunk.dst]) if contain_postype(sentence[chunk.dst], "動詞") else ""
        if origin != "" and target != "":
            print origin + '\t' + target


#44. 係り受け木の可視化
#与えられた文の係り受け木を有向グラフとして可視化せよ．可視化には，係り受け木をDOT言語に変換し，Graphvizを用いるとよい．また，Pythonから有向グラフを直接的に可視化するには，pydotを使うとよい．
print "\nQ44: "

#45. 動詞の格パターンの抽出
#今回用いている文章をコーパスと見なし，日本語の述語が取りうる格を調査したい． 動詞を述語，動詞に係っている文節の助詞を格と考え，述語と格をタブ区切り形式で出力せよ． ただし，出力は以下の仕様を満たすようにせよ．
#動詞を含む文節において，最左の動詞の基本形を述語とする
#述語に係る助詞を格とする
#述語に係る助詞（文節）が複数あるときは，すべての助詞をスペース区切りで辞書順に並べる
#「吾輩はここで始めて人間というものを見た」という例文（neko.txt.cabochaの8文目）を考える． この文は「始める」と「見る」の２つの動詞を含み，「始める」に係る文節は「ここで」，「見る」に係る文節は「吾輩は」と「ものを」と解析された場合は，次のような出力になるはずである．
#
#始める  で
#見る    は を
#このプログラムの出力をファイルに保存し，以下の事項をUNIXコマンドを用いて確認せよ．
#コーパス中で頻出する述語と格パターンの組み合わせ
#「する」「見る」「与える」という動詞の格パターン（コーパス中で出現頻度の高い順に並べよ）
print "\nQ45: "

#46. 動詞の格フレーム情報の抽出
#45のプログラムを改変し，述語と格パターンに続けて項（述語に係っている文節そのもの）をタブ区切り形式で出力せよ．45の仕様に加えて，以下の仕様を満たすようにせよ．
#
#項は述語に係っている文節の単語列とする（末尾の助詞を取り除く必要はない）
#述語に係る文節が複数あるときは，助詞と同一の基準・順序でスペース区切りで並べる
#「吾輩はここで始めて人間というものを見た」という例文（neko.txt.cabochaの8文目）を考える． この文は「始める」と「見る」の２つの動詞を含み，「始める」に係る文節は「ここで」，「見る」に係る文節は「吾輩は」と「ものを」と解析された場合は，次のような出力になるはずである．
#
#始める  で      ここで
#見る    は を   吾輩は ものを
print "\nQ46: "
#47. 機能動詞構文のマイニング
#動詞のヲ格にサ変接続名詞が入っている場合のみに着目したい．46のプログラムを以下の仕様を満たすように改変せよ．
#
#「サ変接続名詞+を（助詞）」で構成される文節が動詞に係る場合のみを対象とする
#述語は「サ変接続名詞+を+動詞の基本形」とし，文節中に複数の動詞があるときは，最左の動詞を用いる
#述語に係る助詞（文節）が複数あるときは，すべての助詞をスペース区切りで辞書順に並べる
#述語に係る文節が複数ある場合は，すべての項をスペース区切りで並べる（助詞の並び順と揃えよ）
#例えば「別段くるにも及ばんさと、主人は手紙に返事をする。」という文から，以下の出力が得られるはずである．
#
#返事をする      と に は        及ばんさと 手紙に 主人は
#このプログラムの出力をファイルに保存し，以下の事項をUNIXコマンドを用いて確認せよ．
#
#コーパス中で頻出する述語（サ変接続名詞+を+動詞）
#コーパス中で頻出する述語と助詞パターン
print "\nQ47: "
#48. 名詞から根へのパスの抽出
#文中のすべての名詞を含む文節に対し，その文節から構文木の根に至るパスを抽出せよ． ただし，構文木上のパスは以下の仕様を満たすものとする．
#
#各文節は（表層形の）形態素列で表現する
#パスの開始文節から終了文節に至るまで，各文節の表現を"->"で連結する
#「吾輩はここで始めて人間というものを見た」という文（neko.txt.cabochaの8文目）から，次のような出力が得られるはずである．
#
#吾輩は -> 見た
#ここで -> 始めて -> 人間という -> ものを -> 見た
#人間という -> ものを -> 見た
#ものを -> 見た
print "\nQ48: "
#49. 名詞間の係り受けパスの抽出
#文中のすべての名詞句のペアを結ぶ最短係り受けパスを抽出せよ．ただし，名詞句ペアの文節番号がiiとjj（i<ji<j）のとき，係り受けパスは以下の仕様を満たすものとする．
#
#問題48と同様に，パスは開始文節から終了文節に至るまでの各文節の表現（表層形の形態素列）を"->"で連結して表現する
#文節iiとjjに含まれる名詞句はそれぞれ，XとYに置換する
#また，係り受けパスの形状は，以下の2通りが考えられる．
#
#文節iiから構文木の根に至る経路上に文節jjが存在する場合: 文節iiから文節jjのパスを表示
#上記以外で，文節iiと文節jjから構文木の根に至る経路上で共通の文節kkで交わる場合: 文節iiから文節kkに至る直前のパスと文節jjから文節kkに至る直前までのパス，文節kkの内容を"|"で連結して表示
#例えば，「吾輩はここで始めて人間というものを見た。」という文（neko.txt.cabochaの8文目）から，次のような出力が得られるはずである．
#
#Xは | Yで -> 始めて -> 人間という -> ものを | 見た
#Xは | Yという -> ものを | 見た
#Xは | Yを | 見た
#Xで -> 始めて -> Y
#Xで -> 始めて -> 人間という -> Y
#Xという -> Y
print "\nQ49: "
