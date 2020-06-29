from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
from django.urls import reverse
from ckeditor.fields import RichTextField
import re


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    content = RichTextField()
    date_posted = models.DateTimeField(default=timezone.now)
    image = models.ImageField(
        default='default.jpg', upload_to="blog_images")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

    #     img = Image.open(self.image.path)

    #     if img.height > 730 or img.width > 487:
    #         output_size = (730, 487)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)

    @property
    def first_three_sentences(self):
        matched_sentences_list = re.findall(
            '.*?[a-z0-9][.?!](?= )', self.content)

        sentence_list = []
        i = 0
        while(i < len(matched_sentences_list)):
            if(i == 3):
                break
            else:
                sentence_list.append(matched_sentences_list[i])
                i += 1
        return "".join(sentence_list)

    @property
    def ordered_by_date_comments(self):
        return self.comment_set.all().filter(parent=None).order_by('-date_posted')

    @property
    def comments_num(self):
        return len(self.comment_set.all())

    @classmethod
    def post_categories_num(cls, category):
        category_post_list = cls.objects.filter(category=category)
        return len(category_post_list)

    @classmethod
    def most_popular_five_posts(cls):
        return sorted(cls.objects.all(), key=lambda post: post.comments_num, reverse=True)[:5]

    @classmethod
    def post_categories(cls):
        category_list = cls.objects.values_list(
            'category', flat=True).distinct()
        return category_list

    @classmethod
    def post_archive(cls):
        distinct_months_list = cls.objects.dates(
            'date_posted', 'month', order="DESC")
        return distinct_months_list


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    parent = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"comment by {self.author} with {self.id}"

    @property
    def replies(self):
        return Comment.objects.filter(parent=self).order_by('-date_posted')

    @property
    def is_replies(self):
        if self.parent is not None:
            return False
        return True
