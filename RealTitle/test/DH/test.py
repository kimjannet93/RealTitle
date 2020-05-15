##### render_to_string을 이용해서 맹글어서 보내기. ### test.html과 article_keyword_table_contents.html 필요
# @csrf_exempt
# def renderToStringTest(request):
#     if request.method == 'GET':
#         return render(request, 'test.html')
#     elif request.is_ajax():
#         ### querry = r""" select * from article_article """
#         ### test01 = article.objects.raw(querry)
#         ### print(test01[0])
#         ### print(dir(article.objects.all()[0]))
#         ### print(article.objects.all()[0])
#         ### querry = r""" select * from article_article where article_category=%s """
#         ### test = article.objects.raw(querry,['사회'] )
#         ### print(test[0])
#         ### dishes = json.dumps([{"article_title":"기사제목1", "article_content":"내용1"},{"article_title":"기사제목2", "article_content":"내용2"}], ensure_ascii=False, )
#         ### dishes = [{"article_title":"기사제목1", "article_content":"내용1"},{"article_title":"기사제목2", "article_content":"내용2"}]
#         ### dishes = article.objects.all().values()[0];dishes = [dishes]
#         dishes = article.objects.all().values()[:10]
#         print(dishes, type(dishes))
#         ### print(dishes['word'])
#         html = render_to_string('article_keyword_table_contents.html', {'dishes': dishes})
#         ### html = None
#         return HttpResponse(html)
#         pass




@csrf_exempt
def test_sort(request):
    ### 다른 테이블과 조인 같은 경우
    # obj = Article.objects.extra( 
    #     select={
    #         'media_url':'SELECT media_url FROM article_media WHERE article_article.article_media = media_name'
    #     },
    # )
    # print(obj.values())

    # return render(request, 'test_sort.html')
    #### 게시글 정렬 테스트
    articles_data = Article.objects.all()
    ## queryset to json
    # data = serializers.serialize("json",articles_data[:10].values())
    ## queryset origin
    sample_data = articles_data[:2]
    data = serializers.serialize('json',sample_data)
    # data = articles_data[:2].values()
    return render(request, 'test_sort.html',{"data":data})


########################## 언론성향분석, 속도개선 #########
# https://docs.djangoproject.com/en/3.0/ref/models/querysets/
# https://simpleisbetterthancomplex.com/tutorial/2016/12/06/how-to-create-group-by-queries.html
def test_queryset(request):
    media = '연합뉴스'
    queryset = Article.objects.values('article_category').filter(article_media = media)
    categories = queryset.values('article_category').distinct().values_list('article_category', flat=True)
    # print("queryset.count > ",queryset.count())
    # print("queryset.distinct", category)
    # print("queryset.agg.IT과학", queryset.filter(article_category = 'IT과학').count())
    data = [ (queryset.filter(article_category = category).count()) for category in categories ]
    # print(categories)
    # print(data)
    return HttpResponse('test')





##################################게시글 페이지네이션 테스트#####################

@csrf_exempt
def test_page(request):
    # article_data = Article.objects.all() ## test01 query : ALL SELECT
    article_data = Article.objects.extra(select={'media_url':'SELECT media_url FROM article_media WHERE article_article.article_media = media_name'}).order_by('-article_date','article_id')
    data = article_data # queryset
    print(data)

    paginator = Paginator(data, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # return render( request, 'test_page.html',{ "queryset":data, "listQueryset":list(data), "page_obj":page_obj } )
    return render( request, 'test_page.html',{ "page_obj":page_obj } )




###############################################################
@csrf_exempt
def test_frequency(request):
    import time
    start_time = time.time()
    categories = ['사회','경제','정치','세계','IT과학','생활문화','오피니언']
    keywords = {}
    for category in categories:
        print(category)
        first_query = article_date=Article.objects.filter(article_category = category).aggregate(Max('article_date'))
        # print(first_query, first_query.keys(), first_query.get('article_date__max'))
        queryset = Article.objects.filter( article_category= category , article_date=first_query.get('article_date__max') ).values('article_category','article_title','article_date')
        # print(dir(queryset), queryset.values('article_title'), len(queryset))

        keywords[category] = keyword.text_preprocessing( queryset.values('article_title') )
    print("--- %s seconds ---" % (time.time() - start_time))
    # print(keywords[category])
    
    ### join with title
    # titles = ' '.join( title['article_title'] for title in queryset.values('article_title') )
    # print(titles)
    # print(keyword.nouns_frequency(titles))
    # return HttpResponse("blog-index")
    return HttpResponse(keywords)


    ############################ 달력 테스트 및 관련.

    def test_clob(request):
    search_keyword = '코로나'
    queryset = Article.objects.values('article_content').filter(article_content__icontains=search_keyword)
    # searchquery = queryset.filter(article_content__icontains=search_keyword)
    # searchquery = queryset.filter(article_content__icontains=search_keyword) | queryset.filter(article_title__icontains=search_keyword)
    # print(searchquery)
    #_text__search=
    # queryset = Article.objects.values('article_content').filter(article_content__search=search_keyword)
    # queryset = Article.objects.values('article_content').filter(article_content__contains=search_keyword)
    # print(queryset)
    return HttpResponse("index")

def test_datetime(request):
    return render(request, 'test_datetimepicker.html')