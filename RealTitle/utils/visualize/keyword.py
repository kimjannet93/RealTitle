from konlpy.tag import Hannanum
from collections import Counter

from . import wordcloud01, textrank
import networkx
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

import numpy as np
import pandas as pd
import os

from base64 import b64encode
import io
import urllib
import re

## 
def text_preprocessing(queryset):
    # print(queryset,len(queryset))
    hannanum = Hannanum()
    getNum = 5
    stopword = ['등','코','만','속보','최초','4억', '월요일']
    df = pd.DataFrame.from_records( queryset )
    # print(df, type(df))
    # df['title_nouns'] = df['article_title'].apply( lambda x : hannanum.nouns( wordcloud01.clean_text( x ) ) ); print(df['title_nouns']); print(df['title_nouns'].sum())
    # print('apply시작')
    df['title_nouns'] = df['article_title'].apply( lambda x : Counter( hannanum.nouns( wordcloud01.clean_text( x ) ) ) )
    # print('sum시작')
    total_counter = df['title_nouns'].sum()
    # print('stopword')
    for word in stopword:
        del total_counter[word] 
    # print(type(total_counter), total_counter.most_common( getNum ))
    result = total_counter.most_common( getNum )
    return result


## 키워드 추출 관련.
def tr(text):
    # print( text)
    text = ''.join( text.split() )
    # print( text)
    # print("clean text >",wordcloud01.clean_text(text).strip())
    tr = textrank.TextRank(window=5, coef=1)
    # print('Load...')
    # stopword = set( [('있', 'VV'), ('하', 'VV'), ('되', 'VV'), ('없', 'VV') ] )
    # tr.load( textrank.RawTaggerReader(text), lambda w : w not in stopword and ( w[1] in ('NNG', 'NNP') ) )
    stopword = set( ['있', '하', '되', '없', '은', '태', '을', '도', '라고', '것', '리', '내니', '있다', '과', '수', '오', '이제', '히먄', '내', '의', '데', '셈', '명','두','등','이상의','최','가', '이어', '지금', '결국', '에', '식', '가운데', '대', '위', '이', '게', '보면', '위해', '본', '관련' ] )
    tr.load( textrank.RawTaggerReader(text) , lambda w : w not in stopword)
    # print('Build...')
    tr.build()
    return tr

def extract_keyword(tr_object, extract_num=0.1):
    kw = tr_object.extract( extract_num )
    return kw

def draw_keyword(tr_object):
    wordcloud01.setFont( wordcloud01.setFontPath() )
    fig = plt.figure(figsize=(10,10))
    plt.axis('off') 
    pos = networkx.random_layout(tr_object.graph)
    pr = tr_object.rank()
    nsize = np.array([v for v in pr.values()])
    nsize = 2000 * (nsize - min(nsize)) / (max(nsize) - min(nsize))
    networkx.draw_networkx( 
         tr_object.graph
        ,pos=pos
        ,font_family= fm.FontProperties(fname=wordcloud01.setFontPath(), size=50).get_name() 
        ,alpha=0.7
        ,node_color=list(pr.values())
        ,node_size=nsize
        ,edge_color='.5' 
        ,cmap=plt.cm.YlGn)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = b64encode(buf.read())
    IMAGEURI = 'data:image/png;base64,' + urllib.parse.quote(string)
    return IMAGEURI

################################
## 개선진행중
def text_preprocessing_after(lists):
    hannanum = Hannanum()
    getNum = 5
    stopword = ['등','코','만','속보','최초','4억', '월요일']
    cleaning = lambda x: hannanum.nouns( wordcloud01.clean_text( x ) )
    nouns_list = list(map( cleaning, lists ))

    # print(nouns_list)

    texts = [ value for nouns in nouns_list for value in nouns ]
    total_counter = Counter( texts )
    for word in stopword:
        del total_counter[word] 
    result = total_counter.most_common( getNum )
    return result

## 명사 빈도 추출. ##################################################
# def nouns_frequency(text):
#     print('Kkma 객체 생성')
#     hannanum = Kkma()
#     print('텍스트 처리중')
#     clean_text = wordcloud01.clean_text(text)
#     print('텍스트 명사 처리중')
#     words = hannanum.nouns(clean_text)
#     print('평평하게 만들기')
#     word_list = wordcloud01.flatten(words)
#     print('판다스 변환중')
#     word_list = pd.Series([x for x in word_list if len(x)>1])
#     print('result Counter 중')
#     result = Counter(word_list)
#     return result