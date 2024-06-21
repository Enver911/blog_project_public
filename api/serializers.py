from rest_framework import serializers
from blog.models import Post, Tag, Comment
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.urls import reverse_lazy
from rest_framework.validators import UniqueValidator


#       
class PostListSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(slug_field="name", many=True, read_only=True)
    author = serializers.SlugRelatedField(slug_field="username", read_only=True)
    url = serializers.URLField(source='get_absolute_url', read_only=True) 
    class Meta:
        model = Post
        fields = ("title", "slug", "body", "publish", "updated", "author", "tags", "url")   

#
class PostDetailedSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(slug_field="name", many=True, read_only=True)
    author = serializers.SlugRelatedField(slug_field="username", read_only=True)
    similar_posts = serializers.SerializerMethodField()
    
    def get_similar_posts(self, obj):
        tags = obj.tags.all()
        similar_posts = Post.published.filter(tags__in=tags).exclude(slug=obj.slug)
        similar_posts = similar_posts.annotate(same_tags = Count("tags")).order_by("-same_tags", "-publish")[:4]
        return PostListSerializer(instance=similar_posts, many=True).data
    
    class Meta:
        model = Post
        fields = ("title", "slug", "body", "publish", "updated", "author", "tags", "similar_posts")

#
class PostCommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field="username", read_only=True)
    body = serializers.CharField(style={'base_template': 'textarea.html'})
    created = serializers.DateTimeField(read_only=True, required=False)

    class Meta:
        model = Comment
        fields = ("body", "created", "updated", "author")

#        
class PostTagSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=30)
    slug = serializers.SlugField(allow_unicode=False, max_length=50, validators=[UniqueValidator(queryset=Tag.objects.all())], required=False)
    url = serializers.SerializerMethodField(required=False)
    
    def get_url(self, obj):
        print(repr(self))
        return reverse_lazy("api:PostTagList", kwargs={"slug": obj.slug})
    
    class Meta:
        model = Tag
        fields = ("name", "slug", "url")
        
#       
class PostShareSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=25)
    email = serializers.EmailField()
    to = serializers.EmailField()
    comments = serializers.CharField()
