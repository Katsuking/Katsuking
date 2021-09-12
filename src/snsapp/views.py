from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User

from .models import Post, Connection


class Home(LoginRequiredMixin, ListView): #LoginRequiredMixinを継承することで、ログインしていなければログイン画面にリダイレクトします。
    """HOMEページで、自分以外のユーザー投稿をリスト表示"""
    model = Post
    template_name = 'list.html'

    def get_queryset(self):
        #リクエストユーザーのみ除外
        return Post.objects.exclude(user=self.request.user)
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        #get_or_createにしないとサインアップ時オブジェクトがないためエラーになる
        context['connection'] = Connection.objects.get_or_create(user=self.request.user)
        return context
      
   
class MyPost(LoginRequiredMixin, ListView):
    """自分の投稿のみ表示"""
    model = Post
    template_name = 'list.html'
    
    def get_queryset(self):#自分の投稿に限定
        return Post.objects.filter(user=self.request.user)


class DetailPost(LoginRequiredMixin, DetailView):
    """投稿詳細ページ"""
    model = Post
    template_name = 'detail.html'


class CreatePost(LoginRequiredMixin, CreateView):
    """投稿フォーム"""
    model = Post
    template_name = 'create.html'
    fields = ['title', 'content'] #投稿フォームの入力項目を決めるfields
    success_url = reverse_lazy('mypost') #https://docs.djangoproject.com/en/3.2/ref/class-based-views/mixins-editing/#django.views.generic.edit.FormMixin.success_url
    #投稿後の遷移先を決めるsuccess_url（またはget_success_urlメソッド）


    def form_valid(self, form):
        """投稿ユーザーをリクエストユーザーと紐付け"""
        form.instance.user = self.request.user # request.user = ログイン中のユーザー
        #form.instance.(フィールド名)でデータベースのテーブルにアクセス。
        return super().form_valid(form) #親のメソッドを使うsuper(子クラス名, インスタンス) クラス内であれば、引数はいらない。
        #super()で、基底classのメソッドをまるまる呼び出している。


class UpdatePost(LoginRequiredMixin, UserPassesTestMixin, UpdateView): #https://docs.djangoproject.com/en/3.2/ref/class-based-views/generic-editing/#django.views.generic.edit.UpdateView
    """投稿編集ページ"""
    model = Post
    template_name = 'update.html' 
    fields = ['title', 'content'] #Postクラスの使うフィールドを選択

    def get_success_url(self,  **kwargs): #https://docs.djangoproject.com/en/3.2/ref/class-based-views/mixins-editing/#django.views.generic.edit.FormMixin.get_success_url
        """編集完了後の遷移先"""
        pk = self.kwargs["pk"]
        return reverse_lazy('detail', kwargs={"pk": pk}) 
        #get_success_urlは pkなどの変数をしていできる

    def test_func(self, **kwargs): #https://docs.djangoproject.com/en/3.2/topics/auth/default/#django.contrib.auth.mixins.UserPassesTestMixin
        """アクセスできるユーザーを制限""" #test_funcは、UserPassesTestMixinクラスのメソッド
        pk = self.kwargs["pk"]
        post = Post.objects.get(pk=pk)
        return (post.user == self.request.user)


class DeletePost(LoginRequiredMixin, UserPassesTestMixin, DeleteView): #https://docs.djangoproject.com/en/3.2/ref/class-based-views/generic-editing/#django.views.generic.edit.DeleteView
    """投稿編集ページ"""
    model = Post
    template_name = 'delete.html'
    success_url = reverse_lazy('mypost')

    def test_func(self, **kwargs): #class UserPassesTestMixin
        """アクセスできるユーザーを制限"""
        pk = self.kwargs["pk"]
        post = Post.objects.get(pk=pk)
        return (post.user == self.request.user)

class LikeBase(LoginRequiredMixin, View):
    """いいねのベース。リダイレクト先を以降で継承先で設定"""
    def get(self, request, *args, **kwargs):
        #記事の特定
        pk = self.kwargs['pk']
        related_post = Post.objects.get(pk=pk)

        #いいねテーブル内にすでにユーザーが存在する場合   # models.pyのManyToManyFieldでunique reverse nameがrelated_post 勝手につけた逆引き名 https://docs.djangoproject.com/en/3.2/topics/db/models/#be-careful-with-related-name-and-related-query-name
        if self.request.user in related_post.like.all(): #like = models.ManyToManyField(User, related_name='related_post', blank=True)
            #テーブルからユーザーを削除 
            obj = related_post.like.remove(self.request.user)#いいねテーブル内にすでにユーザーが存在しない場合
        else:
            #テーブルにユーザーを追加                           
            obj = related_post.like.add(self.request.user)  
        return obj

class LikeHome(LikeBase):
    """HOMEページでいいねした場合"""
    def get(self, request, *args, **kwargs):
        #LikeBaseでリターンしたobj情報を継承
        super().get(request, *args, **kwargs)
        #homeにリダイレクト
        return redirect('home')


class LikeDetail(LikeBase):
    """詳細ページでいいねした場合"""
    def get(self, request, *args, **kwargs):
        #LikeBaseでリターンしたobj情報を継承
        super().get(request, *args, **kwargs)
        pk = self.kwargs['pk'] 
        #detailにリダイレクト
        return redirect('detail', pk)

class FollowBase(LoginRequiredMixin, View):
    """フォローのベース。リダイレクト先を以降で継承先で設定"""
    def get(self, request, *args, **kwargs):
        #ユーザーの特定
        pk = self.kwargs['pk']
        target_user = Post.objects.get(pk=pk).user
       
        #ユーザー情報よりコネクション情報を取得。存在しなければ作成
        #get_or_create()の戻り値は、タプル型(object, created)オブジェクトとboolean型    参照公式https://docs.djangoproject.com/en/3.2/ref/models/querysets/#django.db.models.query.QuerySet.get_or_create
        my_connection = Connection.objects.get_or_create(user=self.request.user) #get_or_create QuerySet API reference https://docs.djangoproject.com/en/3.2/ref/models/querysets/#get-or-create
        
        #フォローテーブル内にすでにユーザーが存在する場合
        if target_user in my_connection[0].following.all(): #get_or_create()の戻り値は、タプル型(object, created)オブジェクトとboolean型 だから[0]でオブジェクトのみ取得
           #テーブルからユーザーを削除
           obj = my_connection[0].following.remove(target_user)
        #フォローテーブル内にすでにユーザーが存在しない場合
        else:
           #テーブルにユーザーを追加
            obj = my_connection[0].following.add(target_user)
        return obj
#######################################################################
#フォロー処理

class FollowHome(FollowBase):
    """HOMEページでフォローした場合"""
    def get(self, request, *args, **kwargs):
        #FollowBaseでリターンしたobj情報を継承
        super().get(request, *args, **kwargs)
        #homeにリダイレクト
        return redirect('home')

class FollowDetail(FollowBase):
    """詳細ページでフォローした場合"""
    def get(self, request, *args, **kwargs):
        #FollowBaseでリターンしたobj情報を継承
        super().get(request, *args, **kwargs)
        pk = self.kwargs['pk'] 
        #detailにリダイレクト
        return redirect('detail', pk)

class FollowList(LoginRequiredMixin, ListView):
    """フォローしたユーザーの投稿をリスト表示"""
    model = Post
    template_name = 'list.html'

    def get_queryset(self): #公式 https://docs.djangoproject.com/en/3.2/topics/db/managers/#modifying-a-manager-s-initial-queryset
        """フォローリスト内にユーザーが含まれている場合のみクエリセット返す"""
        my_connection = Connection.objects.get_or_create(user=self.request.user) #https://docs.djangoproject.com/en/3.2/ref/models/querysets/#get-or-create
        all_follow = my_connection[0].following.all() #models.pyのConnectionクラスをチェック
        #投稿ユーザーがフォローしているユーザーに含まれている場合オブジェクトを返す。
        
        #公式 https://docs.djangoproject.com/en/3.2/ref/models/querysets/#in
        return Post.objects.filter(user__in=all_follow) #投稿ユーザーがフォローしているユーザーに含めれる条件

    def get_context_data(self, *args, **kwargs): #get_context_data 公式 https://docs.djangoproject.com/en/3.2/topics/class-based-views/generic-display/#adding-extra-context
        """コネクションに関するオブジェクト情報をコンテクストに追加"""
        #get_context_data()によって、Connectionクラスそのものに追加する機能が無くても、親クラスであるPostのメソッドをsuper()で使うことができる。
        context = super().get_context_data(*args, **kwargs) #get_context_data https://docs.djangoproject.com/en/3.2/ref/class-based-views/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.get_context_data
        #コンテクストに追加
        context['connection'] = Connection.objects.get_or_create(user=self.request.user)
        return context