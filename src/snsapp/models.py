from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Post(models.Model): #これで タイトル、本文、投稿者、投稿日時に関するフィールドを設定してテーブルを作成
   title = models.CharField(max_length=100)
   content = models.TextField()
   user = models.ForeignKey(User, on_delete=models.CASCADE) #当然だけど、Userは、Django標準のUserクラス
   #Many-to-Many relationship https://docs.djangoproject.com/en/3.2/topics/db/examples/many_to_many/
   like = models.ManyToManyField(User, related_name='related_post', blank=True) #https://docs.djangoproject.com/en/3.2/topics/db/models/#be-careful-with-related-name-and-related-query-name
   created_at = models.DateTimeField(auto_now_add=True)

   def __str__(self):
       return self.title

   class Meta:
       ordering = ["-created_at"] # create_atが作成されたのとは、反対順に表示=投稿順にクエリを取得

class Connection(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # one-to-one relationship https://docs.djangoproject.com/en/3.2/ref/models/fields/#django.db.models.OneToOneField
    following = models.ManyToManyField(User, related_name='following', blank=True) #https://docs.djangoproject.com/en/3.2/topics/db/models/#be-careful-with-related-name-and-related-query-name

    def __str__(self):
        return self.user.username