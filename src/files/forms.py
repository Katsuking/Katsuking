#DjangoのFormクラスを継承することで、管理画面で追加・編集を行うチェンジを
#テンプレートファイルで表現できるようになる。

from django import forms
from .models import FileUpload

#今回はフィールドがfields属性にuploadの一つだけなので、('upload',)のみ
#https://docs.djangoproject.com/en/3.2/topics/forms/modelforms/ 公式
#fields = ['pub_date', 'headline', 'content', 'reporter']のように普通はタプルにしている。
class FileUploadForm(forms.ModelForm): #forms.ModelFormが大文字じゃないというくそミスでごみった。。？？
    class Meta:
        model = FileUpload
        fields = ('upload',)


