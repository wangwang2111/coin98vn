from markdown2 import Markdown
from django import forms
from secrets import choice
from django.shortcuts import render
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import *
from datetime import date, datetime
import requests

def get_by_headlines(hl):
    try:
        f = News.objects.get(headlines=hl)
        return f
    except:
        return None


def get_by_titles(tt):
    try:
        f = News.objects.get(title=tt)
        return f
    except:
        return None


# Enter your API key here
api_key = "8dbb9d221f0573481a868d614b744b8b"
base_url = "http://api.openweathermap.org/data/2.5/weather?"
city_name = "Hanoi"
complete_url = base_url + "appid=" + api_key + "&q=" + city_name

try:
    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] != "404":
        y = x["main"]
        # key in variable z
        z = x["weather"]
        weather_description = z[0]["description"]
        # to the "temp" key of y
        tempInc = str(round(y["temp"] - 273.15)) + u"\N{DEGREE SIGN}C"
        current_temp = tempInc + "," + city_name
    else:
        current_temp = "Hanoi,Vietnam"
except:
    current_temp = "Hanoi,Vietnam"

# Create your views here.
current_date = date.today().strftime("%a, %B %d, %Y")
now = datetime.now()


def index(request):
    # banner
    four_news = News.objects.all().order_by('-add_time')[0:4]
    categories = Category.objects.all()[0:4]

    # authors
    author_news = []
    if len(Author.objects.all()) < 6:
        authors = Author.objects.all()[:3]
        for author in authors:
            if len(author.author_news.all()) > 1:
                author_news += [author.author_news.all().order_by('-views')[:2]]
    else:
        authors = Author.objects.all()[:6]
        for author in authors:
            if len(author.author_news.all()) > 0:
                author_news += choice(author.author_news.all())

    # general
    category_news = []
    for category in categories:
        if len(category.category_news.all()) > 2:
            category_news.append(
                category.category_news.all().order_by('-views')[2])

    # Hottest
    views_order = News.objects.all().order_by('-views')
    firsttrendingnews = views_order[0]
    banner_of_hottest = firsttrendingnews.main_category.category_image
    next2trendingnews = views_order[1:3]
    last2trendingnews = views_order[3:5]

    # editor choice
    if len(views_order) >= 17:
        left = News.objects.all().order_by('views')[0:6]
    elif len(views_order) >= 12 and len(views_order) < 17:
        left = News.objects.all().order_by('views')[0:3]
    recommended = [[], []]
    views_order = []
    for i in range(len(left)):
        j = i // 3
        recommended[j].append(left[i])

    five_latest = News.objects.all().order_by('-add_time')[:5]

    return render(request, 'homepage/index.html', {
        "current_date": current_date, "current_temp": current_temp,
        "four_news": four_news,
        "category_news": category_news,
        "author_news": author_news,
        "firsttrendingnews": firsttrendingnews, "banner_of_hottest": banner_of_hottest,
        "next2trendingnews": next2trendingnews,
        "last2trendingnews": last2trendingnews,
        "recommended": recommended,
        "five_latest": five_latest,
    })


def category(request, categorytitle):
    try:
        thiscategory = Category.objects.get(title=categorytitle)
    except:
        message = "Chủ đề " + categorytitle + " không tồn tại"
        return render(request, 'homepage/error.html', {
            "code": 404,
            "suggestion": False,
            "message": message,
        })
    primary_choice = choice(thiscategory.category_news.all()[:3])
    all_news = thiscategory.category_news.exclude(
        headlines=primary_choice.headlines)
    firttwos = all_news[:2]
    nexttwos = all_news[2:4]
    left = all_news[4:]
    if len(left) > 16:
        left = all_news[4:20]
    next_news = [[], [], [], []]
    if left:
        for i in range(len(left)):
            j = i // 4
            next_news[j].append(left[i])

    return render(request, 'homepage/secondary.html', {
        "current_date": current_date, "current_temp": current_temp,
        "primary_choice": primary_choice, "firttwos": firttwos, "nexttwos": nexttwos,
        "next_news": next_news,
        "category": thiscategory,
    })

def read_news(request, headlines):
    markdowner = Markdown()
    news = get_by_headlines(headlines)
    if news is None:
        message = "Không có bài đăng nào với tiêu đề: " + headlines
        return render(request, 'homepage/error.html', {
            "code": 404,
            "suggestion": False,
            "message": message
        })
    content = news.article
    author = news.author
    newest = News.objects.all().order_by('-add_time').first()
    trendingnews = []
    for tnews in News.objects.all().order_by('-views'):
        if tnews.add_time.day == newest.add_time.day or tnews.add_time.day == newest.add_time.day - 1:
            trendingnews.append(tnews)
        if len(trendingnews) >= 4:
            break
    news_tags = news.tag.all()

    # Comments
    comments = Comment.objects.filter(news=news).filter(status=True)
    for comment in comments:
        comment.day_time = comment.cmt_time.strftime('%d %B %Y')
    # Related news
    related_news = []
    for tag in news_tags:
        for n in Tag.objects.get(title=tag).newsTag.all().exclude(headlines=news.headlines):
            if n not in related_news:
                related_news.append(n)
        if len(related_news) >= 6:
            break
    message = ""
    # Post a comment
    if request.method == "POST":
        news.cmt_count += 1
        news.save()
        if not request.POST['name'] or not request.POST['email'] or not request.POST['message']:
            return render(request, 'homepage/error.html', {'code': 401, "message": "Bạn phải nhập tên, email và nội dung bình luận!"})
        name = request.POST['name']
        email = request.POST['email']
        comment = request.POST['message']
        try:
            avatar = request.FILES["user_ava"]
        except:
            avatar = ""
        Comment.objects.create(name=name, email=email, comment=comment, news=news, avatar=avatar)
        message = "Bình luận đã được gửi đi, trong quá trình cần kiểm duyệt"
        return HttpResponseRedirect(reverse("homepage:read_news", args=(headlines,)))
    
    # Recent
    recent_news = News.objects.all().order_by('-add_time')[:4]
    # Popular
    popular_news = News.objects.all().order_by('-views')[:4]
    # Tags
    tags = Tag.objects.annotate(news_count=Count('newsTag')).order_by('-news_count')[:11]
    news.views += 1
    news.save()
    return render(request, 'homepage/newsdetails.html', {
        "current_date": current_date, "current_temp": current_temp,
        "trendingnews": trendingnews,
        "news": news,
        "content": markdowner.convert(content),
        "author": author,
        "message": message,
        "news_tags": news_tags,
        "comments": comments,
        "related_news": related_news,
        "recent_news": recent_news,
        "popular_news": popular_news,
        "tags": tags
    })


def search(request):
    r = request.GET.get("r", "")
    subStringEntries = []
    for entry in News.objects.all():
        if r.upper() in entry.headlines.upper() or r.upper() in entry.title.upper() or r.upper() in entry.main_category.title.upper() or r.upper() in entry.author.name.upper():
            subStringEntries.append(entry)

    if get_by_headlines(r) is not None:
        return HttpResponseRedirect("read/" + r)
    if get_by_titles(r) is not None:
        return HttpResponseRedirect("read/" + get_by_titles(r).headlines)
    elif subStringEntries:
        first_result = subStringEntries.pop(0)
        message = "Kết quả tìm kiếm cho " + r
        return render(request, "homepage/results.html", {
            "current_date": current_date, "current_temp": current_temp,
            "first_result": first_result,
            "results": subStringEntries,
            "message": message,
        })
    else:
        message = "Không kết quả tìm kiếm nào phù hợp với " + r + " !"
        return render(request, 'homepage/error.html', {
            "current_date": current_date, "current_temp": current_temp,
            "code": "",
            "suggestion": True,
            "message": message,
        })


def aboutus(request):
    return render(request, 'homepage/aboutus.html')


def tag_news(request, tagtitle):
    found = False
    for tag in Tag.objects.all():
        if tagtitle.upper() in tag.title.upper():
            tagtitle = tag.title
            found = True
    tagnews = Tag.objects.get(title=tagtitle).newsTag.all()
    if not found or not tagnews:
        message = "Không có kết quả tìm kiếm nào phù hợp với Tag: " + tagtitle + " !"
        return render(request, 'homepage/error.html', {
            "current_date": current_date, "current_temp": current_temp,
            "code": "",
            "suggestion": True,
            "message": message,
        })
    else:
        first_result = tagnews.first()
        results_left = tagnews[1:]
        message = "Kết quả với Tag: " + tagtitle
        return render(request, 'homepage/results.html', {
            "current_date": current_date, "current_temp": current_temp,
            "first_result": first_result,
            "results": results_left,
            "message": message,
        })
