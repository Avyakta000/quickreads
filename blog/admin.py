# blog/admin.py

from django.contrib import admin
from .models import Blog, BlogView, BlogImage, Category, Topic, Comment, UserInterest

# Register the Category model
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}  # Automatically populate slug based on name

admin.site.register(Category, CategoryAdmin)

# Register the Topic model
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    # prepopulated_fields = {'slug': ('name',)}  # Automatically populate slug based on name

admin.site.register(Topic, TopicAdmin)

# blog images
class BlogImageInline(admin.TabularInline):
    model = BlogImage
    extra = 1
# Register the Blog model
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    list_filter = ('categories', 'topics', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}  # Automatically populate slug based on title
    inlines = [BlogImageInline]


admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogView)
admin.site.register(UserInterest)

# Register the Comment model
class CommentAdmin(admin.ModelAdmin):
    list_display = ('blog', 'author', 'text', 'created_at')
    list_filter = ('author', 'created_at')
    search_fields = ('content',)

admin.site.register(Comment, CommentAdmin)
