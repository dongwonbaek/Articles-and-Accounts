from django.shortcuts import render, redirect
from django.contrib import messages
from articles.forms import ArticleForm, CommentForm
from articles.models import Article, Comment
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    context = {
        'articles':Article.objects.all()
    }
    return render(request, 'articles/index.html', context)

@login_required
def create(request):
    if request.method == 'POST':
        article_form = ArticleForm(request.POST, request.FILES)
        if article_form.is_valid():
            form = article_form.save(commit=False)
            form.user = request.user
            form.save()
            return redirect ('articles:index')
    else:
        article_form = ArticleForm()
    context = {
        'article_form':article_form,
    }
    return render(request, 'articles/create.html', context)

@login_required
def detail(request, pk):
    article = Article.objects.get(pk=pk)
    comment_form = CommentForm()
    context = {
        'article':article,
        'comment_form':comment_form,
        'comments': article.comment_set.all(),
    }
    return render(request, 'articles/detail.html', context)

@login_required
def update(request, pk):
    article = Article.objects.get(pk=pk)
    if article.user == request.user:
        if request.method == 'POST':
            form = ArticleForm(request.POST, request.FILES, instance=article)
            if form.is_valid():
                form.save()
                messages.success(request, '성공적으로 수정되었습니다.')
                return redirect('articles:detail', article.pk)
        else:
            form = ArticleForm(instance=article)
        context = {
            'form':form,
        }
        return render(request, 'articles/update.html', context)
    else:
        messages.warning(request, '잘못된 접근입니다.')
        return redirect('articles:detail', article.pk)

@login_required
def create_comment(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.article = article
            comment.save()
    else:
        messages.warning(request, '잘못된 접근입니다.')    
    return redirect('articles:detail', article.pk)

@login_required
def delete(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method == 'POST' and article.user == request.user:
        article.delete()
        return redirect('articles:index')

@login_required
def delete_comment(request, article_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.method == 'POST' and (comment.user == request.user):
        comment.delete()
    else:
        messages.warning(request, '잘못된 접근입니다.')
    return redirect('articles:detail', article_pk)

