#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import codecs

#第2章: UNIXコマンドの基礎

#hightemp.txtは，日本の最高気温の記録を「都道府県」「地点」「℃」「日」のタブ区切り形式で格納したファイルである．以下の処理を行うプログラムを作成し，hightemp.txtを入力ファイルとして実行せよ．さらに，同様の処理をUNIXコマンドでも実行し，プログラムの実行結果を確認せよ．
data = "hightemp.txt"

#10. 行数のカウント
#行数をカウントせよ．確認にはwcコマンドを用いよ．
import os
import sys
print "Q10: "
print sum(1 for line in open(data))
print "---- unix output -----"
os.system("wc " + data + " -l | cut -f 1 -d ' '")

#11. タブをスペースに置換
#タブ1文字につきスペース1文字に置換せよ．確認にはsedコマンド，trコマンド，もしくはexpandコマンドを用いよ．
import string
print "\nQ11: "
with open(data, 'r') as file:
    print file.read().translate(string.maketrans("\t",' '))
print "---- unix output -----"
os.system("tr '\t' ' ' <" + data)

#12. 1列目をcol1.txtに，2列目をcol2.txtに保存
#各行の1列目だけを抜き出したものをcol1.txtに，2列目だけを抜き出したものをcol2.txtとしてファイルに保存せよ．確認にはcutコマンドを用いよ．
print "\nQ12: "
with open(data, 'r') as file, open("col1.txt", 'w') as file1, open("col2.txt", 'w') as file2:
    lines = [line.split('\t') for line in file.readlines()]
    for line in lines:
        file1.write(line[0] + '\n')
        file2.write(line[1] + '\n')

with open("col1.txt", 'r') as result:
    print result.read()
with open("col2.txt", 'r') as result:
    print result.read()
print "---- unix output -----"
os.system("cut -f 1 -d '\t' " + data + " && echo '-----' && cut -f 2 -d '\t' " + data)

#13. col1.txtとcol2.txtをマージ
#12で作ったcol1.txtとcol2.txtを結合し，元のファイルの1列目と2列目をタブ区切りで並べたテキストファイルを作成せよ．確認にはpasteコマンドを用いよ．
print "\nQ13: "
with open("result.txt", 'w') as result, open("col1.txt", 'r') as file1, open("col2.txt", 'r') as file2:
    for line1, line2 in zip(file1.readlines(), file2.readlines()):
        result.write(line1.replace('\n', '\t') + line2.replace('\n','') + '\n')
with open("result.txt", 'r') as result:
    print result.read()
print "---- unix output -----"
os.system("paste -d '\t' col1.txt col2.txt")


#14. 先頭からN行を出力
#自然数Nをコマンドライン引数などの手段で受け取り，入力のうち先頭のN行だけを表示せよ．確認にはheadコマンドを用いよ．
print "\nQ14: "
N = 3
with open(data, 'r') as file:
    print ''.join(file.readlines()[0:N])
print "---- unix output -----"
os.system("head -" + str(N) + " " + data)

#15. 末尾のN行を出力
#自然数Nをコマンドライン引数などの手段で受け取り，入力のうち末尾のN行だけを表示せよ．確認にはtailコマンドを用いよ．
print "\nQ15: "
N = 7
#N = int(raw_input("Input: "))
with open(data, 'r') as file:
    print ''.join(file.readlines()[-N:])
print "---- unix output -----"
os.system("tail -" + str(N) + " " + data)


#16. ファイルをN分割する
#自然数Nをコマンドライン引数などの手段で受け取り，入力のファイルを行単位でN分割せよ．同様の処理をsplitコマンドで実現せよ．
print "\nQ16: "
N = 7
#N = int(raw_input("Input: "))
os.system("rm q16_*.txt && rm x*")
with open(data, 'r') as file:
    lines = file.readlines()
    total = sum(1 for line in open(data))
    for counter in list(enumerate(range(total), N))[0:total:N]:
        with open("q16_" + str(counter[1]) + ".txt", 'w') as output:
            output.write(''.join(lines[counter[1]:counter[0]]))

import glob
for file in glob.glob('q16_*.txt'):
    print "==>",file,"<=="
    with open(file) as temp:
        print temp.read()
print "---- unix output -----"
os.system("split -l " + str(N) + " " + data + " && tail -n +1  x*")


#17. １列目の文字列の異なり
#1列目の文字列の種類（異なる文字列の集合）を求めよ．確認にはsort, uniqコマンドを用いよ．
print "\nQ17: "
with open(data, 'r') as file:
    prefectures = [ line.split('\t')[0] for line in  file.readlines() ]
    for line in list(set(prefectures)):
        print line
print "---- unix output -----"
os.system("cut -f 1 -d '\t' " + data + "| sort | uniq ")


#18. 各行を3コラム目の数値の降順にソート
#各行を3コラム目の数値の逆順で整列せよ（注意: 各行の内容は変更せずに並び替えよ）．確認にはsortコマンドを用いよ（この問題はコマンドで実行した時の結果と合わなくてもよい）．
print "\nQ18: "
from operator import itemgetter
with open(data, 'r') as file:
    lines = [ tuple(line.split('\t')) for line in file.readlines() ]
    print ''.join([ '\t'.join(str(i) for i in tup) for tup in sorted(lines, key=itemgetter(2), reverse=True)])
print "---- unix output -----"
os.system("sort -rn -t '\t' -k3,3 " + data)


#19. 各行の1コラム目の文字列の出現頻度を求め，出現頻度の高い順に並べる
#各行の1列目の文字列の出現頻度を求め，その高い順に並べて表示せよ．確認にはcut, uniq, sortコマンドを用いよ．
print "\nQ19: "
from collections import Counter
with open(data, 'r') as file:
    prefectures = [ line.split('\t')[0] for line in  file.readlines() ]
    counter = Counter(prefectures)
    for key, count in counter.most_common():
        print key, count
print "---- unix output -----"
os.system("cut -f 1 -d '\t' " + data + "| sort | uniq -c | sort -nr")
