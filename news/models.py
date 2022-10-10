from django.db import models


class News(models.Model):
    title = models.CharField("заголовок", max_length=250)
    text = models.TextField("текст новости")
    pub_date = models.DateTimeField("дата публикации")
    author = models.CharField("автор", max_length=100)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return self.title


class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    author_name = models.CharField("автор", max_length=50)
    comment_text = models.CharField("текст комментария", max_length=200)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.author_name


