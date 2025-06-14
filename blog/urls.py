# blog/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlogViewSet, CommentViewSet, BlogListView, UserInterestViewSet, RecommendedReadsView, GeneratePresignedURLView, DeleteFileView, FetchCategoriesAndTagsView
# CategoryListView, TopicListView,
router = DefaultRouter()
router.register(r'blogs', BlogViewSet)
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'preferences', UserInterestViewSet)

urlpatterns = [
    path('', include(router.urls)), 

    # list categories and pags
    path('categories-tags/', FetchCategoriesAndTagsView.as_view(), name='fetch_categories_and_tags'),
    
    # list reads using query string
    path('reads/', BlogListView.as_view(), name='blog_list'),
    path('recommended-reads/', RecommendedReadsView.as_view(), name='recommended-blogs'),

    # presigned url for client to upload files directly in s3
    path('generate_presigned_url/', GeneratePresignedURLView.as_view(), name='generate_presigned_url'),

    # this needs to be done from fronted however hybrid approach have taken in use to put an obj in s3 after pressigned url is recieved from backend server and to delete an object by directly making a request on server
    path('generate_delete_presigned_url/', DeleteFileView.as_view(), name='generate_delete_presigned_url'),

    # path('categories/', CategoryListView.as_view(), name='category-list'),
    # path('categories/<slug:category_slug>/topics/', TopicListView.as_view(), name='topic-list'),

]
