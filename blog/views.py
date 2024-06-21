from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Post, Tag
from django.core.paginator import Paginator
from .forms import EmailPostForm, CommentForm, SearchPostForm
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Count, Q
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity, TrigramWordSimilarity
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages

#
def post_list(request, slug=None):
    tags = Tag.objects.all()
    if slug is None: # запрос без тега
        posts = Post.published.all() 
        current_tag = ""
    else: # запрос с тегом
        posts = Post.published.filter(tags__slug__in=[slug])
        current_tag = Tag.objects.get(slug=slug)
        
    paginator_obj = Paginator(posts, per_page=4)
    
    page = int(request.GET.get("page", 1))
    if page > paginator_obj.num_pages:
        page = paginator_obj.num_pages
    elif page < 1:
        page = 1
    
    current_page = paginator_obj.get_page(page)
    return render(request, "blog/post_list.html", context={"current_page": current_page, "paginator": paginator_obj, "tags": tags, "current_tag": current_tag})


def post_detailed(request, slug):
    post = get_object_or_404(Post, slug=slug, status=Post.Status.PUBLISHED)
    tags = post.tags.all()
    
    comments_amount = post.comments.all().count()
    
    # recommendations
    similar_posts = Post.published.filter(tags__in=tags).exclude(slug=post.slug)
    similar_posts = similar_posts.annotate(same_tags = Count("tags")).order_by("-same_tags", "-publish")[:4]

    return render(request, "blog/post_detailed.html", context={"post": post, "comments_amount": comments_amount, "tags": tags, "similar_posts": similar_posts})


@login_required(login_url=reverse_lazy("users:user_login"))
def post_comments(request, slug):
    post = get_object_or_404(Post, slug=slug, status=Post.Status.PUBLISHED)
    tags = post.tags.all()
    comments = post.comments.all().order_by("-created")
    
    # recommendations
    similar_posts = Post.published.filter(tags__in=tags).exclude(slug=post.slug)
    similar_posts = similar_posts.annotate(same_tags = Count("tags")).order_by("-same_tags", "-publish")[:4]

    if request.method == "GET":
        form = CommentForm()
    elif request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_obj = form.save(commit=False)
            comment_obj.post = post
            comment_obj.author = request.user
            comment_obj.save() # добавление коммента в БД
            messages.success(request, message="Комментарий был успешно добавлен")
        
    return render(request, "blog/post_comments.html", context={"post": post, "comments": comments, "form": form, "tags": tags, "similar_posts": similar_posts})


#
def post_share(request, slug):
    post = get_object_or_404(Post, slug=slug, status=Post.Status.PUBLISHED)
        
    if request.method == "GET":
        form = EmailPostForm()   
        
    elif request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            
            #отправка письма
            subject = f"{data["name"]} рекомендует вам прочитать пост"
            
            message = f"""
            Почта отправителя:
            "{data["email"]}"
            Комментарий отправителя:
            "{data["comments"] if data["comments"] else 'Отсутствует'}"
            Тема поста:
            "{post.title}"
            Ссылка на пост:
            "{request.build_absolute_uri(post.get_absolute_url())}"
            """       
            
            recipient = data["to"]
            send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=[recipient])
            
            return render(request, "blog/post_share_success.html")
        
    return render(request, "blog/post_share.html", context={"form": form, "post": post}) 

#
def post_search(request):

    if request.GET.get("query"): # запрос с поиском
        form = SearchPostForm(request.GET)
        
        if form.is_valid():
            query = form.cleaned_data["query"]
            
            filtred_query = SearchQuery(query, config="russian") #ключевое слово с извлеченным корнем из лексемы
            vector_obj = SearchVector("body", "title", config="russian") #поля для поиска однокоренных слов
            rank_obj = SearchRank(vector_obj, filtred_query)
            
                    # однокоренной поиск по названию и содержанию статьи
                    # триграммный поиск по названию статьи
                    # подмножественный поиск по названию и содержанию статьи
            posts = Post.published.annotate(search=vector_obj, rank=rank_obj).filter(search=filtred_query).order_by("-rank") or \
                    Post.published.annotate(similarity=TrigramSimilarity("title", query)).filter(similarity__gt=0.1).order_by("-similarity") or \
                    Post.published.filter(Q(title__icontains=query) | Q(body__icontains=query))
                    
            return render(request, "blog/post_search_success.html", context={"posts": posts, "query": query})
         
    else: #запрос без поиска
        form = SearchPostForm()
        posts = []
    return render(request, "blog/post_search.html", context={"form": form, "posts": posts})