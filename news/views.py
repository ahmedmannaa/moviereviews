from django.shortcuts import render
from .models import News
# Create your views here.
def news(req):
    news = News.objects.all().order_by('-date')
    return render(req,'news.html',{
        'news': news
    })