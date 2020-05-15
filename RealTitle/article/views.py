from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q 
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
# from django.core import serializers
from rest_framework import serializers
from .Aritcle_Serializers import ArticleSerializer
import json
from .models import Article
from utils.oracleDB import get_data, pagination
from utils.visualize import wordcloud01, keyword
import os
import pickle
import time


# Create your views here.

def index(request):
    if request.method == 'GET':
        # file_name = 'total_article_ver1_20200427'
    
        # get_data.insertArticle(file_name)
        media_list = get_data.getMediaList(order_type='-media_acc')
        # category_list = get_data.getCategoryList()
        # keyword_list = get_data.getKeywordsPerCategory()
        
        # category_list = {'IT과학':['a','b','c','d','e'], '경제':['a','b','c','d','e'], '사회':['a','b','c','d','e'], '생활문화':['a','b','c','d','e'], '세계':['a','b','c','d','e'], '오피니언':['a','b','c','d','e'], '정치':['a','b','c','d','e']}
        # dirPath = './output/keyword_logs/'
        # fileName_keywordlist = 'category_list_'+time.strftime("%Y%m%d")+'.pickle'
        # if os.path.exists(dirPath):
        #     print('폴더가 있음')
        # else :
        #     os.mkdir(dirPath)
        # if os.path.exists(dirPath + fileName_keywordlist):
        #     with open(dirPath+fileName_keywordlist, 'rb') as f :
        #         category_list = pickle.load(f)
        # else :
        #     category_list = get_data.getKeywordsPerCategory()
        #     with open(dirPath+fileName_keywordlist, 'wb') as f:
        #         pickle.dump(category_list, f, protocol=pickle.HIGHEST_PROTOCOL)

        with open('./output/keyword_logs/category_list.pickle', 'rb') as f :
            category_list = pickle.load(f)

        media_list_arr = []
        media_rm_list = ['KBS 연예', 'MBC연예', 'AP연합뉴스', 'EPA연합뉴스', '일다', '참세상', '헤럴드POP']

        for media in media_list:
            media_list_arr.append((media['media_name'], media['media_acc']))

        for idx, value in enumerate(media_list_arr):
            if value[0] in media_rm_list:
                media_list_arr.remove(value)    

        # return render(request, 'index.html')
        return render(request, 'index.html', {'media_list': media_list_arr, 'category_list': category_list})
        # return render(request, 'index.html', {'media_list': media_list_arr, 'category_list': category_list, 'keyword_list':keyword_list})

@csrf_exempt
def article_list(request):
    if request.method == 'GET':
        search_keyword = request.GET.get('search_keyword', '')
        media = request.GET.get('media', '')
        category = request.GET.get('category', '')
        page = request.GET.get('page', 1)

        article_list = get_data.searchArticle(search_keyword=search_keyword, media=media, category=category)

        posts, total_count, p_range = pagination.get_pagination(data=article_list, page=page)

        media_list = get_data.getMediaList(order_type='media_name')
        category_list = get_data.getCategoryList()
        keyword_list = ['딥러닝맨', 'Real Title', '코로나', '날씨']

        serializers = ArticleSerializer(posts, many=True)
        data = json.dumps(serializers.data)

        return render(request, 'article_list.html', {'search_keyword': search_keyword,
                                                    'media': media,
                                                    'category': category,
                                                    'posts': posts,
                                                    # 'data': serializers.serialize('json', posts),
                                                    'data': data,
                                                    'total_count': total_count,
                                                    'p_range': p_range,
                                                    'media_list': media_list,
                                                    'category_list': category_list,
                                                    'keyword_list': keyword_list})

@csrf_exempt
def article_analysis(request):
    if request.method == 'GET':
        ### 넘어온 id를 받아서 사용.
        art_id = request.GET.get('article_id','') #; print(" article_id >",art_id)
        
        ## raw 쿼리도 가능.
        # theArticle = article.objects.raw('select * from article_article where article_id = %s', [art_id])
        theArticle = Article.objects.filter(article_id = art_id)

        url = theArticle[0].article_url
        content = theArticle[0].article_content
        # print(content)
        wc, bar, count = wordcloud01.generate_wordCloud(content, wordcloud01.setFontPath())
        # print("count >",count)
        tr_object = keyword.tr(content)
        nx_uri = keyword.draw_keyword(tr_object)
        return render(request, 'article_analysis.html', { "wordcloud":wc, "barchart":bar,"count":count, "article_url":url, "networkx":nx_uri })
    
@csrf_exempt
def aritcle_keyword_visualization(request): # 키워드 시각화 페이지
    if request.method == 'GET':
        return render(request, 'aritcle_keyword_visualization.html')
    elif request.is_ajax():
        # print('POST key 값 >', request.POST)
        content = request.POST['article_content']
        # print('받은 텍스트 >', contents)
        wcURI, barURI, count = wordcloud01.generate_wordCloud( content, wordcloud01.setFontPath() )
        tr_object = keyword.tr(content)
        nx_uri = keyword.draw_keyword(tr_object)
        return HttpResponse(json.dumps({"wordcloudURI":wcURI, "barURI":barURI, "wordCount":count, "networkx":nx_uri}), "application/json")

@csrf_exempt
def article_keyword_trend(request):
    if request.method == 'GET':
        return render(request, 'article_keyword_trend.html')

    elif request.method == 'POST':
        search_keyword = request.POST.get('search_keyword', '')
        search_keyword2 = request.POST.get('search_keyword2', '')
        start_date = request.POST.get('start_date', 0)
        end_date = request.POST.get('end_date', 99999999)

        data = get_data.keywordTrend(search_keyword, search_keyword2, start_date, end_date)

        return HttpResponse(json.dumps(data), 'application/json')

@csrf_exempt
def article_media_analysis(request):
    if request.method == 'GET':
        media_list = get_data.getMediaList(order_type='media_name')
        return render(request, 'article_media_analysis.html', {'media_list': media_list})

    elif request.method == 'POST':
        media_name = request.POST.get('media_name', '')
        media_name2 = request.POST.get('media_name2', '')
        # data = get_data.mediaAnalysis(media_name=media_name)
        data = get_data.test_mediaAnalysis(media_name=media_name,media_name2=media_name2)

        return HttpResponse(json.dumps(data), 'application/json')