from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    media_url = serializers.CharField()
    result_acc = serializers.FloatField()
    result_newtitle = serializers.CharField()
    class Meta:
        model = Article
        fields = ('article_id','article_url','article_category','article_media','article_date','article_title','media_url','result_acc','result_newtitle')
