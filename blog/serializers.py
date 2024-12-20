from rest_framework import serializers
from .models import Blog, BlogImage, Comment, Category, Topic, UserInterest
from myaccount.models import User
from datetime import datetime

class AuthorSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'full_name']  

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


# category and comments start......................................
class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'name', 'slug']

class CategorySerializer(serializers.ModelSerializer):
    # topics = TopicSerializer(many=True)
    # topics = serializers.StringRelatedField(many=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'category_image']
# category and topics end...........................................


# comments start....................................................
class RecursiveCommentSerializer(serializers.Serializer):
    """Recursive serializer to handle nested comments."""
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data

class CommentSerializer(serializers.ModelSerializer):
    replies = RecursiveCommentSerializer(many=True, read_only=True)
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'blog', 'author', 'text', 'replies', 'created_at']
        read_only_fields = ['replies']
# comments end........................................................


# blogs serializer start..............................................
class BlogImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogImage
        fields = ['id', 'image', 'uploaded_at']

class BlogSerializer(serializers.ModelSerializer):
    images = BlogImageSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    views_count = serializers.IntegerField(source='views')
    author_full_name = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    topics = serializers.SerializerMethodField()
    
    # format datetime in readible format
    created_at = serializers.DateTimeField(format = "%B %d, %Y at %I:%M %p")
    updated_at = serializers.DateTimeField(format = "%B %d, %Y at %I:%M %p")

    class Meta:
        model = Blog
        fields = ['id', 'title', 'slug', 'content', 'author_full_name', 'category', 'topics', 'images', 'cover_image', 'comments', 'likes_count', 'views_count', 'created_at', 'updated_at']
        # fields = ['id', 'title', 'content', 'categories', 'topics', 'images', 'comments', 'created_at', 'updated_at']
        # read_only_fields = ['author', 'likes', 'views']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_author_full_name(self, obj):
        return f"{obj.author.first_name} {obj.author.last_name}" if obj.author else "No Author"

    def get_category(self, obj):
        return obj.categories.name 
        
    def get_topics(self, obj):
        return [topics.name for topics in obj.topics.all()] if obj.topics else []

class BlogCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )
    
    class Meta:
        model = Blog
        fields = ['id', 'title', 'content', 'categories', 'topics', 'images', 'cover_image', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        print('blog create serializer create method',validated_data)
        images_data = validated_data.pop('images', [])
        category = validated_data.pop('categories', [])
        topics = validated_data.pop('topics', [])
        
        print(validated_data, category, topics,'----validated_data')
        blog = Blog.objects.create(**validated_data, categories=category)

        # Set categories and topics after blog creation
        # blog.categories.set(categories)
        blog.topics.set(topics)

        for image_data in images_data:
            BlogImage.objects.create(blog=blog, image=image_data)
        return blog

    def update(self, instance, validated_data):
        # Update the blog instance fields
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)

        # Handle categories and topics if they exist in validated_data
        category = validated_data.get('categories')
        if category is not None:
           instance.categories = category
        # categories = validated_data.get('categories')
        # if categories is not None:
        #     instance.categories.set(categories)

        topics = validated_data.get('topics')
        if topics is not None:
            instance.topics.set(topics)

        instance.save()
        # Handle image uploads
        images_data = validated_data.pop('images', [])
        for image_data in images_data:
            BlogImage.objects.create(blog=instance, image=image_data)

        return instance
# blogs serializers end.................................................


# user interest or preference start.....................................
class UserInterestSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(many=True, queryset=Category.objects.all())
    topics = serializers.PrimaryKeyRelatedField(many=True, queryset=Topic.objects.all())

    class Meta:
        model = UserInterest
        fields = ['id', 'categories', 'topics']

class UserInterestDetailSerializer(serializers.ModelSerializer):

    category_names = serializers.SerializerMethodField()
    topic_names = serializers.SerializerMethodField()

    class Meta:
        model = UserInterest
        fields = ['category_names', 'topic_names']

    # Method to fetch category names instead of IDs
    def get_category_names(self, obj):
        return [category.name for category in obj.categories.all()]

    # Method to fetch topic names instead of IDs
    def get_topic_names(self, obj):
        return [topic.name for topic in obj.topics.all()]        
# user interest or preference end.......................................      
