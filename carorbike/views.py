from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .forms import PhotoForm
from .models import Photo

def index(request):
    template = loader.get_template('carorbike/index.html')
    context = {'form': PhotoForm()}
    return HttpResponse(template.render(context, request))

def predict(request):
    # post以外のアクセス(不正)は戻す
    if not request.method == 'POST':
        return
        redirect('carorbike:index')
    
    form = PhotoForm(request.POST, request.FILES)

    # 画像が適切でなければ戻す
    if not form.is_valid():
        raise ValueError('Image file is incorrect')

    photo = Photo(image=form.cleaned_data['image'])
    predicted, percentage = photo.predict()

    template = loader.get_template('carorbike/result.html')

    context = {
        'photo_name': photo.image.name,
        'photo_data': photo.image_src(),
        'predicted': predicted,
        'percentage': percentage,
    }

    return HttpResponse(template.render(context, request))

