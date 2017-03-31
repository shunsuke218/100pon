#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import codecs
import json 
import re
import copy

#第5章: 係り受け解析

#夏目漱石の小説『吾輩は猫である』の文章（neko.txt）をCaboChaを使って係り受け解析し，その結果をneko.txt.cabochaというファイルに保存せよ．このファイルを用いて，以下の問に対応するプログラムを実装せよ．
file = "neko.txt.cabocha"

#40. 係り受け解析結果の読み込み（形態素）
#形態素を表すクラスMorphを実装せよ．このクラスは表層形（surface），基本形（base），品詞（pos），品詞細分類1（pos1）をメンバ変数に持つこととする．さらに，CaboChaの解析結果（neko.txt.cabocha）を読み込み，各文をMorphオブジェクトのリストとして表現し，3文目の形態素列を表示せよ．
print "Q40: "
class Morph():
    def __init__(self, surface, base, pos, pos1):
        self.surface = surface
        self.base = base
        self.pos = pos
        self.pos1 = pos1
    def __str__(self):
        return "[ " + self.surface + ", " +  self.pos + ", " +  self.pos1 + ", " + self.base + " ]"
    def is_punct(self):
        return self.pos == "記号"

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

    # Join morphs to string
    def join_morphs(self, postype = None, skip_punct = True, type = "surface"):
        string = ""
        for morph in self.morphs:
            if skip_punct and morph.is_punct():
               continue
            if postype is not None and morph.pos != postype:
                continue
            if type == "surface":
                string += morph.surface
            elif type == "base":
                string += morph.base
        return string

    # Check if chunk contains postype
    def contain_postype(self, postype):
        if postype == None: return True
        for tmp in self.morphs:
            if tmp.pos == postype or tmp.pos1 == postype:
                return True
        else:
            return False

    # Check if chunk contains phrase
    def contain_phrase(self, phrase):
        if phrase == None: return True
        for tmp in self.morphs:
            if tmp.surface == phrase or tmp.base == phrase:
                return True
        else:
            return False

    def remove_unmatch_morphs(self, postype):
        for index, tmp in enumerate(self.morphs):
            if tmp.pos != postype or tmp.pos1 != postype:
                self.morphs.pop(index)

    def remove_match_morphs(self, postype):
        for index, tmp in enumerate(self.morphs):
            if tmp.pos == postype or tmp.pos1 == postype:
                self.morphs.pop(index)

    # Return a list of morph with certain postype
    def return_morphs(self, postype = None, string = True, skip_punct = True):
        result = []
        for tmp in self.morphs:
            if postype is None:
                if skip_punct and tmp.pos == "記号":
                    continue
                result.append(tmp)
            elif tmp.pos == postype or tmp.pos1 == postype:
                result.append(tmp)
        #return result
        return ''.join([tmp.surface for tmp in result]) if string else result

    # Return a list of origin morph with certain postype
    def return_origin_chunks(self, sentence, postype = None, string = True):
        chunk_list = []
        for origin_index in self.srcs:
            chunk = sentence[origin_index]
            if postype is not None:
                if chunk.contain_postype(postype):
                    chunk_copy = copy.deepcopy(chunk)
                    chunk_copy.remove_unmatch_morphs(postype)
                    chunk = chunk_copy
                    #chunk.remove_unmatch_morphs(postype)
                else:
                    continue
            chunk_list.append(chunk)
        return chunk_list if string is False \
            else ' '.join([ chunk.join_morphs() for chunk in chunk_list ])

    def return_target_chunk(self, sentence, postype = None, string = True):
        if self.dst is -1: return None
        chunk = sentence[self.dst]
        if postype is not None:
            if chunk.contain_postype(postype):
                chunk_copy = copy.deepcopy(chunk)
                chunk_copy.remove_unmatch_morphs(postype)
                chunk = chunk_copy
            else:
                chunk = None
        return chunk if string is False else chunk.join_morphs()

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

for chunk in neko[8]:
        print chunk
        

#42. 係り元と係り先の文節の表示
#係り元の文節と係り先の文節のテキストをタブ区切り形式ですべて抽出せよ．ただし，句読点などの記号は出力しないようにせよ．
print "\nQ42: "
for sentence in neko[0:10]:
    for chunk in sentence:
        origin = chunk.join_morphs()
        target = chunk.return_target_chunk(sentence)
        if origin != "" and target is not None:
            print origin + '\t' + target

#43. 名詞を含む文節が動詞を含む文節に係るものを抽出
#名詞を含む文節が，動詞を含む文節に係るとき，これらをタブ区切り形式で抽出せよ．ただし，句読点などの記号は出力しないようにせよ．
print "\nQ43: "
    
for sentence in neko[0:10]:
    for origin_chunk in sentence:
        target_chunk =  origin_chunk.return_target_chunk(sentence, None, False)
        if target_chunk is None: continue
        string_if_contain_pos = lambda chunk, type: chunk.join_morphs() if chunk.contain_postype(type) else ""
        origin = string_if_contain_pos(origin_chunk, "名詞")
        target = string_if_contain_pos(target_chunk, "動詞")
        if origin != "" and target != "":
            print origin + '\t' + target


#44. 係り受け木の可視化
#与えられた文の係り受け木を有向グラフとして可視化せよ．可視化には，係り受け木をDOT言語に変換し，Graphvizを用いるとよい．また，Pythonから有向グラフを直接的に可視化するには，pydotを使うとよい．
print "\nQ44: "
import pydot

graph = pydot.Dot(graph_type='digraph')
for sentence in neko[0:1]:
    for chunk in sentence:
        target_chunk = sentence[chunk.dst]
        origin = chunk.join_morphs()
        target = target_chunk.join_morphs()
        if origin != "" and target != "":
            edge = pydot.Edge(origin.decode('utf-8'), target.decode('utf-8'))
            graph.add_edge(edge)

#graph.write_png('q44_graph.png')
graph.write('q44_graph.png')


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
with open('q45.txt','w') as output:
    for sentence in neko:
        for chunk in sentence:
            for verb_morph in chunk.return_morphs("動詞",False):
                origin = verb_morph.base
                target = chunk.return_origin_chunks(sentence, "助詞")
                if origin != "" and target != "":
                    output.write(origin + '\t' + target + '\n')
os.system("for key in する 見る 与える; do echo \"==>$key<==\";grep \"^$key\" q45.txt | sort | uniq -c | sort -nr; done")


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
with open('q46.txt','w') as output:
    for sentence in neko[0:10]:
        for chunk in sentence:
            for verb_morph in chunk.return_morphs("動詞",False):
                origin = verb_morph.base
                target = chunk.return_origin_chunks(sentence, "助詞")
                term = chunk.return_origin_chunks(sentence, None)
                if origin != "" and target != "" and term != "":
                    output.write(origin + '\t' + target + '\t' + term + '\n')
os.system("cat q46.txt")

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
with open('q47.txt','w') as output:
    for sentence in neko:
        for sahen_chunk in sentence:
            # For all chunks which contain sahen
            if sahen_chunk.contain_postype("サ変接続") \
               and sahen_chunk.contain_postype("格助詞") \
               and sahen_chunk.contain_phrase("を"):
                
                verb_chunk = sahen_chunk.return_target_chunk(sentence, None, False)
                if verb_chunk is None: continue
                origin_chunk = verb_chunk.return_origin_chunks(sentence, None, False)

                # If target chunk contain verb
                if verb_chunk is None \
                   or verb_chunk.contain_postype("動詞") is False: 
                    continue

                # Get sahen and verb, and join together
                sahen_morph = sahen_chunk.return_morphs("サ変接続", False)[0]
                verb_morph = verb_chunk.return_morphs("動詞", False)[0]
                predicate = sahen_morph.surface + "を" + verb_morph.base

                # Extract joshi and phrases which contains joshi and make a dictionary
                dictionary = {}
                for chunk in origin_chunk:
                    if chunk.index == sahen_chunk.index \
                         or not (chunk.contain_postype("係助詞") or chunk.contain_postype("格助詞")): continue
                    text = chunk.join_morphs()
                    for index, morph in enumerate(chunk.morphs):
                        if morph.pos1 != "係助詞" or morph.pos1 != "格助詞":
                            chunk.morphs.pop(index)
                    key = chunk.join_morphs("助詞")
                    if len(key) is 0 or len(text) is 0: continue
                    dictionary[key] = text

                # Sort dictionary and save it to a file
                if bool(dictionary) is False: continue
                keys = []; values = []
                for (key, value) in sorted(dictionary.items()):
                    keys.append(key); values.append(value)
                output.write(predicate + '\t' + ' '.join(keys) + '\t' + ' '.join(values) + '\n')
os.system("cut q47.txt -f 1 | sort | uniq -c | sort -nr; echo '---'; cut q47.txt -f 1,2 | sort | uniq -c | sort -nr")


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
def print_all_targets(chunk, sentence):
    target = sentence[chunk.dst]
    print " -> ", target.join_morphs(),
    if target.dst is -1: return
    print_all_targets(target, sentence)


for sentence in neko[0:10]:
    for meishi_chunk in [ chunk for chunk in sentence if chunk.contain_postype("名詞") ]:
        target = meishi_chunk.return_target_chunk(sentence, None, False)
        if target is not None \
           and (target.dst is not -1\
                or len(target.join_morphs()) is not 0 ):
            print meishi_chunk.join_morphs(),
            print_all_targets(meishi_chunk, sentence)
            print ""


#49. 名詞間の係り受けパスの抽出
#文中のすべての名詞句のペアを結ぶ最短係り受けパスを抽出せよ．ただし，名詞句ペアの文節番号がiとj（i<j）のとき，係り受けパスは以下の仕様を満たすものとする．
#
#問題48と同様に，パスは開始文節から終了文節に至るまでの各文節の表現（表層形の形態素列）を"->"で連結して表現する
#文節iとjに含まれる名詞句はそれぞれ，XとYに置換する
#また，係り受けパスの形状は，以下の2通りが考えられる．
#
#文節iから構文木の根に至る経路上に文節jが存在する場合: 文節iから文節jのパスを表示
#上記以外で，文節iと文節jから構文木の根に至る経路上で共通の文節kで交わる場合: 文節iから文節kに至る直前のパスと文節jから文節kに至る直前までのパス，文節kの内容を"|"で連結して表示
#例えば，「吾輩はここで始めて人間というものを見た。」という文（neko.txt.cabochaの8文目）から，次のような出力が得られるはずである．
#
#Xは | Yで -> 始めて -> 人間という -> ものを | 見た
#Xは | Yという -> ものを | 見た
#Xは | Yを | 見た
#Xで -> 始めて -> Y
#Xで -> 始めて -> 人間という -> Y
#Xという -> Y
print "\nQ49: "
import itertools

def print_all_targets(chunk, chunk2, sentence, beginning = True):
    target = sentence[chunk.dst]
    target2 = sentence[chunk2.dst]
    chunk_dst = " chunk dst: (" + str(chunk.dst) + ", " + str(chunk2.dst) + ")"
    # End of the sentence A
    if chunk.dst is -1 and chunk2.dst is -1: 
        print "|", target.join_morphs()
        return
    # End of the sentence B
    elif chunk.index is chunk2.index and chunk.dst is not -1: 
        print "-> Y"
        return

    # Beginning of the sentence A
    elif chunk.dst is not -1 and target.dst is -1 and beginning:
        print chunk.join_morphs()," | " + chunk2.join_morphs(),
        print_all_targets(target, target2, sentence, False)
    # Beginning of the sentence B
    elif beginning:
        print chunk.join_morphs(),
        print_all_targets(target, chunk2, sentence, False)

    # Middle of the sentence
    elif chunk.index < chunk2.index:
        print "->", chunk.join_morphs(),
        print_all_targets(target, chunk2, sentence, False)
    else:
        print "->", chunk2.join_morphs(),
        print_all_targets(chunk, target2, sentence, False)


for sentence in neko[7:9]:
    meishi_list = [ chunk for chunk in sentence if chunk.contain_postype("名詞") ]
    for pair in list(itertools.combinations(meishi_list,2)):
        X = copy.deepcopy(pair[0])
        Y = copy.deepcopy(pair[1])

        # Replace noun with X,Y
        X.remove_match_morphs("名詞")
        X.morphs.insert(0, Morph("X","名詞","",""))
        Y.remove_match_morphs("名詞")
        Y.morphs.insert(0, Morph("Y","名詞","",""))
        
        # Print all targets
        print_all_targets(X, Y, sentence)
