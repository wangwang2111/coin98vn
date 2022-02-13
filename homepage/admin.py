from django.contrib import admin
from .models import *
# Register your models here.

class AdminNews(admin.ModelAdmin):
    filter_horizontal = ("tag",)
    list_display = ('id', 'headlines', 'main_category', 'tag_titles', 'add_time', 'author', 'views', 'cmt_count')

class AdminComment(admin.ModelAdmin):
    list_display = ('name','email', 'comment', 'cmt_time')

class AdminCategory(admin.ModelAdmin):
    list_display = ('id','title')

class AdminAuthor(admin.ModelAdmin):
    list_display = ('id','name')

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Author)
admin.site.register(Comment, AdminComment)
admin.site.register(News, AdminNews)