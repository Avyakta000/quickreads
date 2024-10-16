# blog/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlogViewSet, CommentViewSet, BlogListView, UserInterestViewSet, RecommendedReadsView

router = DefaultRouter()
router.register(r'blogs', BlogViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'preferences', UserInterestViewSet)

urlpatterns = [
    path('', include(router.urls)), 
    path('reads/', BlogListView.as_view(), name='blog_list'),
    path('recommended-reads/', RecommendedReadsView.as_view(), name='recommended-blogs'),

]
