from django.db.models import Q ,Max
from django.db import connection
import pandas as pd

from article.models import Article, Media, Category
from utils.visualize import keyword

# 언론사 리스트 조회
def getMediaList(order_type):
    # 언론사 리스트
    # media_list = Media.objects.raw('SELECT MEDIA_NAME FROM ARTICLE_MEDIA')
    media_list = Media.objects.values('media_name', 'media_acc').order_by(order_type)

    return media_list

# 카테고리 리스트 조회
def getCategoryList():
    # category_list = Category.objects.raw('SELECT CATEGORY_NAME FROM ARTICLE_CATEGORY')
    category_list = Category.objects.values('category_name')
    return category_list

# 기사 검색 조회
def searchArticle(search_keyword, media, category):
    if search_keyword != '':
        # 언론사, 검색어 둘 다 있을 때
        if media != '':
            # article_list = Article.objects.filter(article_media = media).filter(article_title__icontains=search_keyword).order_by('-article_date')
            article_list = Article.objects.extra(select={
                                                    'media_url':'SELECT media_url FROM article_media WHERE article_article.article_media = media_name', 
                                                    'result_newtitle':'SELECT result_newtitle FROM article_result WHERE article_article.article_id = article_result.result_id',
                                                    'result_acc':'SELECT result_acc FROM article_result WHERE article_article.article_id = article_result.result_id'
                                                }).filter(article_media = media).filter(article_title__icontains=search_keyword).order_by('-article_date', '-result_acc')

        # 카테고리, 검색어 둘 다 있을 때
        elif category != '':
            # article_list = Article.objects.filter(article_category = category).filter(article_title__icontains=search_keyword).order_by('-article_date')
            article_list = Article.objects.extra(select={
                                                    'media_url':'SELECT media_url FROM article_media WHERE article_article.article_media = media_name', 
                                                    'result_newtitle':'SELECT result_newtitle FROM article_result WHERE article_article.article_id = article_result.result_id',
                                                    'result_acc':'SELECT result_acc FROM article_result WHERE article_article.article_id = article_result.result_id'
                                                }).filter(article_category = category).filter(article_title__icontains=search_keyword).order_by('-article_date', '-result_acc')

        # 검색어만 있을 때
        else:
            # article_list = Article.objects.filter(Q(article_title__icontains=search_keyword) | Q(article_content__icontains=search_keyword)).order_by('-article_date')
            # article_list = Article.objects.filter(article_title__icontains=search_keyword).order_by('-article_date')
            article_list = Article.objects.extra(select={
                                                    'media_url':'SELECT media_url FROM article_media WHERE article_article.article_media = media_name', 
                                                    'result_newtitle':'SELECT result_newtitle FROM article_result WHERE article_article.article_id = article_result.result_id',
                                                    'result_acc':'SELECT result_acc FROM article_result WHERE article_article.article_id = article_result.result_id'
                                                }).filter(article_title__icontains=search_keyword).order_by('-article_date', '-result_acc')

    else:
        # 언론사만 있을 때
        if media != '':
            # article_list = Article.objects.filter(article_media = media).order_by('-article_date')
            article_list = Article.objects.extra(select={
                                                    'media_url':'SELECT media_url FROM article_media WHERE article_article.article_media = media_name', 
                                                    'result_newtitle':'SELECT result_newtitle FROM article_result WHERE article_article.article_id = article_result.result_id',
                                                    'result_acc':'SELECT result_acc FROM article_result WHERE article_article.article_id = article_result.result_id'
                                                }).filter(article_media = media).order_by('-article_date', '-result_acc')

        # 카테고리만 있을 때
        elif category != '':
            # article_list = Article.objects.filter(article_category = category).order_by('-article_date')
            article_list = Article.objects.extra(select={
                                                    'media_url':'SELECT media_url FROM article_media WHERE article_article.article_media = media_name', 
                                                    'result_newtitle':'SELECT result_newtitle FROM article_result WHERE article_article.article_id = article_result.result_id',
                                                    'result_acc':'SELECT result_acc FROM article_result WHERE article_article.article_id = article_result.result_id'
                                                }).filter(article_category = category).order_by('-article_date', '-result_acc')

        # 전체 리스트
        else:
            # article_list = Article.objects.raw('SELECT * FROM ARTICLE_ARTICLE ORDER BY ARTICLE_DATE DESC')
            # article_list = Article.objects.all().order_by('-article_date')

            # extra 사용 -> media_url 출력 안됨
            # article_list = Article.objects.extra(tables=['article_media'], where=['article_media.media_name=article_article.article_media'])
            
            # sql query 사용 -> 무한로딩..
            # article_list = Article.objects.raw('SELECT article.*, media.media_url FROM article_article article, article_media media WHERE media.media_name = article.article_media')

            article_list = Article.objects.extra(select={
                                                    'media_url':'SELECT media_url FROM article_media WHERE article_article.article_media = media_name', 
                                                    'result_newtitle':'SELECT result_newtitle FROM article_result WHERE article_article.article_id = article_result.result_id',
                                                    'result_acc':'SELECT result_acc FROM article_result WHERE article_article.article_id = article_result.result_id'
                                                }).order_by('-article_date', '-result_acc')
            
    return article_list

# DB에 기사 데이터 insert
def insertArticle(file_name):
    df = pd.read_sql('select article_id from article_article group by article_id', connection)

    df.columns = ['article_id']
    df['check'] = 1

    df2 = pd.read_csv('data/' + file_name + '.csv')

    df_merge = pd.merge(df, df2, how='outer')

    df_result = df_merge[df_merge['check'].isna()]
    df_result.drop('check', axis=1, inplace=True)

    print(df_result.head())
    print(df_result.columns)
    print(df_result.shape)

    df1 = df_result[['article_id', 'article_url', 'article_category', 'article_media', 'article_date', 'article_title', 'article_content']]
    rows = [tuple(x) for x in df1.to_records(index=False)]

    for line in rows:
        # print(line)
        article_id = line[0]
        article_url = line[1]
        article_category = line[2]
        article_media = line[3]
        article_date = line[4]
        article_title = line[5]
        article_content = line[6]

        article = Article(article_id=article_id, 
                        article_url=article_url, 
                        article_category=article_category, 
                        article_media=article_media, 
                        article_date=article_date, 
                        article_title=article_title, 
                        article_content=article_content)
        article.save()

        print(article_id, 'insert complete')

# Main 페이지 - 카테고리별로 5개 keyword 
def getKeywordsPerCategory():
    # print("category_list > ",list(Category.objects.values_list('category_name', flat=True)))
    categories = list(Category.objects.values_list('category_name', flat=True))
    keywords = {}
    for category in categories:
        print(category)
        first_query = Article.objects.filter(article_category = category).aggregate(Max('article_date'))
        # print(first_query, first_query.keys(), first_query.get('article_date__max'))
        queryset = Article.objects.values('article_category','article_title','article_date').filter( article_category= category , article_date=first_query.get('article_date__max') )
        # print(dir(queryset), queryset.values('article_title'), len(queryset))

        ### 개선전
        if len(queryset) > 20:
            data = queryset.values('article_title')[:20]
        else :
            data = queryset.values('article_title')
        keywords[category] = keyword.text_preprocessing( data )

        ### 개선선
        # print('data 시작')
        # if len(queryset) > 20:
        #     print('if임')
        #     data = list(queryset.values('article_title', flat=True))[0:20]
        # else :
        #     data = list(queryset.values_list('article_title', flat=True))
        # print(data)
        # keywords[category] = keyword.text_preprocessing_after( data )
    return keywords

# 상세 기사 검색
def keywordTrend(keyword1, keyword2, start_date, end_date):
    # dataset = Article.objects.filter(article_title__icontains=keyword)
    queryset = Article.objects.values('article_id', 'article_date').filter(article_title__icontains=keyword1, article_date__gte=start_date, article_date__lte=end_date)
    queryset2 = Article.objects.values('article_id', 'article_date').filter(article_title__icontains=keyword2, article_date__gte=start_date, article_date__lte=end_date)
    
    df = pd.DataFrame.from_records(queryset)

    df['timestamp'] = pd.to_datetime(df["article_date"],format='%Y%m%d', errors='ignore')
    df['year'] = df["timestamp"].dt.year
    df['month'] = df["timestamp"].dt.month
    df['day'] = df["timestamp"].dt.day

    result_df = df[['article_id', 'day', 'month', 'year']]
    month_count_df = result_df.groupby('month').count()

    df2 = pd.DataFrame.from_records(queryset2)

    df2['timestamp'] = pd.to_datetime(df2["article_date"],format='%Y%m%d', errors='ignore')
    df2['year'] = df2["timestamp"].dt.year
    df2['month'] = df2["timestamp"].dt.month
    df2['day'] = df2["timestamp"].dt.day

    result_df2 = df2[['article_id', 'day', 'month', 'year']]
    month_count_df2 = result_df2.groupby('month').count()

    # convert_date = datetime.strftime(date, "%Y-%m-%d").date()
    # day = convert_date['day']
    # month = convert_date['month']
    # year = convert_date['year']

    data = {
        'labels': month_count_df.index.to_list(),
        'datasets': [{
            'label': keyword1,
            'data': month_count_df['article_id'].tolist(),
            'backgroundColor': 'rgba(255, 99, 132, 0.2)',
            'borderColor': 'rgba(255, 99, 132, 1)',
            'borderWidth': 1,
            'fill': False,
            'pointRadius': 5
        },
        {
            'label': keyword2,
            'data': month_count_df2['article_id'].tolist(),
            'backgroundColor': 'rgba(54, 162, 235, 0.2)',
            'borderColor': 'rgba(54, 162, 235, 1)',
            'borderWidth': 1,
            'fill': False,
            'pointRadius': 5
        }]
    }

    return data

def mediaAnalysis(media_name='',media_name2=''):
    queryset = Article.objects.values('article_id', 'article_category').filter(article_media = media_name)
    category_q = Category.objects.values('category_name')
    df = pd.DataFrame.from_records(queryset)
    category_df = pd.DataFrame.from_records(category_q)
    media_count_df = df.groupby(['article_category']).count()

    queryset2 = Article.objects.values('article_id', 'article_category').filter(article_media = media_name2)
    category_q2 = Category.objects.values('category_name')
    df2 = pd.DataFrame.from_records(queryset2)
    category_df = pd.DataFrame.from_records(category_q2)
    media_count_df2 = df2.groupby(['article_category']).count()
    
    data = {
        'labels': category_df['category_name'].tolist(),
        'datasets': [{
            'label': media_name,
            'data': media_count_df['article_id'].tolist(),
            'backgroundColor': 'rgba(255, 99, 132, 0.2)',
            'borderColor': 'rgba(255, 99, 132, 1)',
            'borderWidth': 1,
            'fill': True
        },
        {
            'label': media_name2,
            'data': media_count_df2['article_id'].tolist(),
            'backgroundColor': 'rgba(54, 162, 235, 0.2)',
            'borderColor': 'rgba(54, 162, 235, 1)',
            'borderWidth': 1,
            'fill': True
        }]

    }

    return data



def test_mediaAnalysis(media_name='',media_name2=''):
    # print(media_name)
    queryset = Article.objects.values('article_category').filter(article_media = media_name)
    queryset2 = Article.objects.values('article_category').filter(article_media = media_name2)
    # print("queryset.count > ",queryset.count())

    # categories = queryset.values('article_category').distinct().values_list('article_category', flat=True)
    categories = Category.objects.values_list('category_name', flat=True)
    # categories = ['IT과학', '경제', '사회', '생활문화', '세계', '오피니언', '정치']
    
    values = [ (queryset.filter(article_media= media_name).filter(article_category = category).count()) for category in categories ]
    #df2 = pd.DataFrame.from_records(queryset2)
    # category_df = pd.DataFrame.from_records(category_q2)
    # media_count_df2 = df2.groupby(['article_category']).count()
    values2 = [ (queryset2.filter(article_media= media_name2).filter(article_category = category).count()) for category in categories ]


    data = {
        'labels': list(categories),
        # 'labels': categories,
        'datasets': [{
            'label': media_name,
            'data': values,
            'backgroundColor': 'rgba(255, 99, 132, 0.2)',
            'borderColor': 'rgba(255, 99, 132, 1)',
            'borderWidth': 1,
            'fill': True
        },
            {
            'label': media_name2,
            'data': values2,
            # 'data': media_count_df2['article_id'].tolist(),
            'backgroundColor': 'rgba(54, 162, 235, 0.2)',
            'borderColor': 'rgba(54, 162, 235, 1)',
            'borderWidth': 1,
            'fill': True
        }]    
    }
    return data