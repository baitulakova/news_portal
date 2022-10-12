from django.contrib import admin
from .models import News, Comment


class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'pub_date', 'author')
    list_filter = ('title', 'text', 'pub_date', 'author')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'comment_text', 'news')
    list_filter = ('author_name', 'comment_text', 'news')


admin.site.register(News, NewsAdmin)
admin.site.register(Comment, CommentAdmin)
