from django.shortcuts import render, redirect
from .models import FileUpload
from .forms import FileUploadForm

# Create your views here.

def index(request):
    file_obj = FileUpload.objects.all()
    return render(request, 'files/index.html', {'file_obj': file_obj})

def new_file(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES) #ファイルをアップロードする場合は、FileUploadFormの引数にrequest.FILESを設定
        if form.is_valid(): #ファイルの保存が成功した場合、
            form.save()
            return redirect('files:index') #('files:index') <- アップロード画面 で指定のhtmlを表示
            #redirect(to, *args, permanent=False, **kwargs)
            #ちなみに, reverse('new_file')のようにurls.pyで名前を指定したURLも使える。

    else:
        form = FileUploadForm()
    context = {
        'form':form,
    }
    return render(request, 'files/new_file.html', context) #render(request, template_name, context=None, content_type=None, status=None, using=None)
    #urls.pyにしているように、/files/new_fileでこのページに
 
"""def delete_file(request, pk):
    if request.method == 'POST':
        selected_file = FileUpload.objects.get(pk=pk)
        selected_file.delete()
    return redirect('files:index') """
