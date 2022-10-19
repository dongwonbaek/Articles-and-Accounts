from django.db import models
from django.forms import DateField
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.contrib.auth import get_user_model

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    image = ProcessedImageField(blank=True, upload_to='images/', processors=[ResizeToFill(400, 300)], format='JPEG', options={'quality':80})
    created_at = models.DateField(auto_now_add=True)
    upload_at = models.DateField(auto_now=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

class Comment(models.Model):
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)