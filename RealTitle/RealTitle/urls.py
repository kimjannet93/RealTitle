"""RealTitle URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import article.views
from django.http import HttpResponseRedirect

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('article/', include('article.urls')),
    # path('', lambda r: HttpResponseRedirect('article/')),
    path('', article.views.index, name='index'),
    path('index/', article.views.index, name='index'),
    path('article_list/', article.views.article_list, name='article_list'),
    path('article_analysis/', article.views.article_analysis, name='article_analysis'),
    path('aritcle_keyword_visualization/', article.views.aritcle_keyword_visualization, name='aritcle_keyword_visualization'),
    path('article_keyword_trend/', article.views.article_keyword_trend, name='article_keyword_trend'),
    path('article_media_analysis/', article.views.article_media_analysis, name='article_media_analysis'),
]
