from django.db import models
import os
import datetime
from django.core.validators import FileExtensionValidator #FileUpload()
# Create your models here.

#upload_toに渡すディレクトリ用の関数
def dir_path_name(instance, filename):
    date_time = datetime.datetime.now() #現在時刻の取得
    date_dir = date_time.strftime('%Y/%m/%d') #年/月/日のフォーマット作成
    time_stamp = date_time.strftime('%H-%M-%S') #時間-分-秒のフォーマット
    new_filename = time_stamp + filename #実際のファイル名と時間-分-秒フォーマットの現在時刻を結合
    dir_path = os.path.join('file', date_dir, new_filename) #階層構造にする
    
    return dir_path

"""
def dir_path_name(instance, filename):
    file_type = os.path.splitxet(filename) #ﾌｧｲﾙ名と拡張子を分ける
    date_time = datetime.datetime.now()
    date_dir = date_time.strftime('%Y/%m/%d')
    time_stamp = date_time.strftime('%H-%M-%S-')
    new_filename = time_stamp + filename

    if file_type[1] == '.csv':
        path = os.path.join('csv', date_dir, new_filename)
    elif file_type[1] == '.pdf':
        path = os.path.join('pdf', date_dir, new_filename)
    elif file_type[1] == '.txt':
        path = os.path.join('txt', date_dir, new_filename)
    elif file_type[1] == '.zip':
        path = os.path.join('zip', date_dir, new_filename)
    elif file_type[1] == '.jpg':
        path = os.path.join('jpg', date_dir, new_filename)
    elif file_type[1] == '.gif':
        path = os.path.join('gif', date_dir, new_filename)
    elif file_type[1] == '.png':
        path = os.path.join('png', date_dir, new_filename)
    elif file_type[1] == '.xlsx':
        path = os.path.join('xlsx', date_dir, new_filename)
    elif file_type[1] == '.xlsm':
        path = os.path.join('xlsm', date_dir, new_filename)
    elif file_type[1] == '.docx':
        path = os.path.join('docx', date_dir, new_filename)
    elif file_type[1] == '.py':
        path = os.path.join('py', date_dir, new_filename)
    
    return path
"""

#if you are using the default FileSystemStorage, the string value will be appended to your MEDIA_ROOT path to form the location
class FileUpload(models.Model):
    upload = models.FileField(upload_to=dir_path_name)
#dir_path_name()関数を使って、file/%Y/%m/%d/%H-%M-%Sファイルのように表示させる。
#拡張子ごとに分ける場合は、, validators=[FileExtensionValidator(['csv', 'pdf', 'txt', 'zip', 'jpg', 'gif', 'png', 'xlsx', 'xlsm', 'docx', 'py',])]で受け取るファイルの拡張子を限定

    #カスタムメソッドで、ディレクトリ構造を抜いたファイル名を取得 実際保存されているデータは、保存先のpathなので、ファイル名のみの取得には、独自の処理が必要です。
    def file_name(self):
        path = os.path.basename(self.upload.name) #ファイル名のみ取得 クラス.フィールド名.プロパティ？
        return path
    