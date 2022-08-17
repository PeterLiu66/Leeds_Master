
from django.db import models
from django.db.models import Avg


class User(models.Model):
    username = models.CharField(max_length=255, unique=True, verbose_name="账号")
    password = models.CharField(max_length=255, verbose_name="密码")
    email = models.EmailField(verbose_name="邮箱")

    class Meta:
        verbose_name_plural = "用户"
        verbose_name = "用户"

    def __str__(self):
        return self.username


class Tags(models.Model):
    name = models.CharField(max_length=255, verbose_name="标签", unique=True)

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = "标签"

    def __str__(self):
        return self.name


class UserTagPrefer(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, verbose_name="用户id",
    )
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE, verbose_name='标签名')
    score = models.FloatField(default=0)

    class Meta:
        verbose_name = "用户偏好"
        verbose_name_plural = "偏好"

    def __str__(self):
        return self.user.username + str(self.score)


class Movie(models.Model):
    tags = models.ManyToManyField(Tags, verbose_name='标签', blank=True)
    collect = models.ManyToManyField(User, verbose_name="收藏者", blank=True)
    name = models.CharField(verbose_name="电影名称", max_length=255, unique=True)
    director = models.CharField(verbose_name="导演名称", max_length=255)
    country = models.CharField(verbose_name="国家", max_length=255)
    years = models.DateField(verbose_name='上映日期')
    leader = models.CharField(verbose_name="主演", max_length=1024)
    d_rate_nums = models.IntegerField(verbose_name="豆瓣评价数")
    d_rate = models.CharField(verbose_name="豆瓣评分", max_length=255)
    intro = models.TextField(verbose_name="描述")
    num = models.IntegerField(verbose_name="浏览量", default=0)
    origin_image_link = models.URLField(verbose_name='豆瓣图片地址', max_length=255, null=True)
    image_link = models.FileField(verbose_name="封面图片", max_length=255, upload_to='movie_cover')
    imdb_link = models.URLField(null=True)
    douban_link = models.URLField(verbose_name='豆瓣初始链接')

    @property
    def movie_rate(self):
        movie_rate = Rate.objects.filter(movie_id=self.id).aggregate(Avg('mark'))['mark__avg']
        return movie_rate or '无'

    class Meta:
        verbose_name = "电影"
        verbose_name_plural = "电影"

    def __str__(self):
        return self.name


class Rate(models.Model):
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, blank=True, null=True, verbose_name="电影id"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="用户id",
    )
    mark = models.FloatField(verbose_name="评分")
    create_time = models.DateTimeField(verbose_name="发布时间", auto_now_add=True)

    @property
    def avg_mark(self):
        average = Rate.objects.all().aggregate(Avg('mark'))['mark__avg']
        return average

    class Meta:
        verbose_name = "评分信息"
        verbose_name_plural = verbose_name


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    content = models.CharField(max_length=255, verbose_name="内容")
    create_time = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="电影")

    # def a(self):
    #     self.likecomment_set.count()
    class Meta:
        verbose_name = "评论"
        verbose_name_plural = verbose_name


class LikeComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name='评论')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')

    class Meta:
        verbose_name = "评论点赞"
        verbose_name_plural = verbose_name
