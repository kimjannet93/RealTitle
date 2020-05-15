from django.db import models

# Create your models here.
class Article(models.Model):
    objects = models.Manager()  # VS code오류 제거용
    article_id = models.CharField(primary_key=True, max_length=20)
    article_url	= models.CharField(max_length=100)
    article_category = models.CharField(max_length=50)
    article_media = models.CharField(max_length=50)
    article_date = models.CharField(max_length=20)
    article_title = models.CharField(max_length=200)
    article_content = models.TextField()

    def __str__(self):
        return (self.article_id) # 문자만 가능

class Result(models.Model):
    objects = models.Manager()
    result_id = models.CharField(primary_key=True, max_length=20)
    result_newtitle = models.CharField(max_length=200)
    result_acc = models.FloatField(null=True)

    def __str__(self):
        return (self.result_id)

class Media(models.Model):
    objects = models.Manager()
    media_id = models.AutoField(primary_key=True)
    media_name = models.CharField(max_length=50)
    media_url = models.CharField(max_length=100)
    media_acc = models.FloatField(null=True)

    def __str__(self):
        return (self.media_name)

class Category(models.Model):
    objects = models.Manager()
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=50)

    def __str__(self):
        return (self.category_name)