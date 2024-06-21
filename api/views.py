from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrReadOnly
from rest_framework import status
from blog.models import Post, Comment, Tag
from .serializers import PostListSerializer, PostDetailedSerializer, PostCommentSerializer, PostTagSerializer, PostShareSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from django.conf import settings
from django.core.mail import send_mail


"""
(self, instance=None, data=empty, **kwargs):
"""
#
class PostList(APIView):
    """Get published posts list"""
    
    def get(self, request):
        posts = Post.published.all().select_related("author").prefetch_related("tags").order_by("-publish")
        if posts:
            serializer = PostListSerializer(instance=posts, many=True)
            return Response(serializer.data)
        return Response({"detail": "No posts"})

#    
class PostTag(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    
    def get(self, request):
        """Get tags list"""
        tags = Tag.objects.all()
        if tags:
            serializer = PostTagSerializer(instance=tags, many=True)
            return Response(serializer.data)
        return Response({"detail": "No tags"})
    
    def post(self, request):
        """JSON {"name": "<tag_name>"} -> Add new tag"""
        
        serializer = PostTagSerializer(data=request.data)
        if serializer.is_valid():
            Tag.objects.create(name=serializer.validated_data.get("name"))
            return Response(serializer.validated_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
# 
class PostTagList(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    
    def get(self, request, slug):
        """Get published posts list by tag slug"""
        
        posts = Post.published.filter(tags__slug=slug).select_related("author").prefetch_related("tags").order_by("-publish")
        if posts:
            serializer = PostListSerializer(instance=posts, many=True)
            return Response(serializer.data)
        return Response({"detail": "No posts"})
    
    def delete(self, request, slug):
        """Delete tag by slug"""
        
        tag = get_object_or_404(Tag.objects, slug=slug)
        tag.delete()
        return Response({slug: "deleted"})

    
#   
class PostDetailed(APIView):
    def get(self, request, slug):
        """Get post info by slug"""
        post = get_object_or_404(Post.published.select_related("author"), slug=slug)
        serializer = PostDetailedSerializer(instance=post)
        return Response(serializer.data)
    
#    
class PostComments(APIView):  
    permission_classes = (IsAuthenticated,)
    
    def get(self, request, slug):
        """Get post comments by slug"""
        
        comments = get_object_or_404(Post.published, slug=slug).comments.all().select_related("author")
        serializer = PostCommentSerializer(instance=comments, many=True)
        return Response(serializer.data)
        
    def post(self, request, slug):
        """JSON {"body": "<comment_body>"} -> Add new comment by authenticated user"""
        
        post = get_object_or_404(Post.published, slug=slug)
        serializer = PostCommentSerializer(data=request.data)
        if serializer.is_valid():
            Comment.objects.create(post=post, author=request.user, body=serializer.validated_data.get("body"))
            return Response(serializer.validated_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#    
class PostSearch(APIView):
    def get(self, request, keyword):
        """Search posts by keyword"""
       
        filtred_query = SearchQuery(keyword, config="russian") #ключевое слово с извлеченным корнем из лексемы
        vector_obj = SearchVector("body", "title", config="russian") #поля для поиска однокоренных слов
        rank_obj = SearchRank(vector_obj, filtred_query)
        
                # однокоренной поиск по названию и содержанию статьи
                # триграммный поиск по названию статьи
                # подмножественный поиск по названию и содержанию статьи
        posts = Post.published.annotate(search=vector_obj, rank=rank_obj).filter(search=filtred_query).order_by("-rank") or \
                Post.published.annotate(similarity=TrigramSimilarity("title", keyword)).filter(similarity__gt=0.1).order_by("-similarity") or \
                Post.published.filter(Q(title__icontains=keyword) | Q(body__icontains=keyword))
                
        if posts: 
            serializer = PostListSerializer(instance=posts, many=True)
            return Response(serializer.data)
        
        return Response({"detail": "No posts"})

#    
class PostShare(APIView):
    def post(self, request, slug):
        """Send recommendation mail"""
        post = get_object_or_404(Post.published, slug=slug)
        
        serializer = PostShareSerializer(data=request.data)
        
        if serializer.is_valid():
            
            #отправка письма
            subject = f"{serializer.validated_data["name"]} рекомендует вам прочитать пост"
            
            message = f"""
            Почта отправителя:
            "{serializer.validated_data["email"]}"
            Комментарий отправителя:
            "{serializer.validated_data["comments"] if serializer.validated_data["comments"] else 'Отсутствует'}"
            Тема поста:
            "{post.title}"
            Ссылка на пост:
            "{request.build_absolute_uri(post.get_absolute_url())}"
            """       
            
            recipient = serializer.validated_data["to"]
            send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=[recipient])
            return Response(serializer.validated_data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
