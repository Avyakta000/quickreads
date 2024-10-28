from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Category, Topic, Blog, BlogView, Comment, UserInterest
from .serializers import BlogSerializer, BlogCreateSerializer, CommentSerializer, UserInterestSerializer, CategorySerializer, TopicSerializer, UserInterestDetailSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from django.utils import timezone
from datetime import timedelta
from django.db import models
from .services.s3_service import S3Service

# fetch all categories and tags
class FetchCategoriesAndTagsView(APIView):

    # permission_classes = [AllowAny]
    def get(self, request):
        try:
            categories = Category.objects.all()
            topics = Topic.objects.all()
            
            categories_serializer = CategorySerializer(categories, many=True)
            topics_serializer = TopicSerializer(topics, many=True)

            return Response({
                'categories': categories_serializer.data,
                'topics': topics_serializer.data,
            })
        except Exception as e:
            # Log the exception if needed
            return Response({
                'error': str(e),
                'message': 'Failed to retrieve categories and topics.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BlogViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Blog.objects.all()
    #  by default, DRF uses the primary key (usually the id field) as the lookup field, but we can customize this behavior.
    lookup_field = 'slug'
    # permission_classes = [IsAuthenticated]

    # serializer method
    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return BlogCreateSerializer
        return BlogSerializer
    
    # create instance
    def perform_create(self, serializer):
        print('perform create working, user',self.request.user, self.request.META)

        if self.request.user.is_anonymous:
            raise AuthenticationFailed({'detail': 'Unauthorized !!'})
            # raise ValidationError({'detail': 'Unauthorized !!'})
        try:
           serializer.save(author=self.request.user) # Save the blog instance
        except Exception as e: 
           print(f'Error occurred while saving: {e}') 
           raise ValidationError({'detail': f'An error occurred while saving the blog. {e}'})
    

    # Likes/Dislikes    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None, permission_classes=[IsAuthenticated]):
        blog = self.get_object()
        if request.user in blog.likes.all():
            blog.likes.remove(request.user)
            return Response({'status': 'unliked'})
        else:
            blog.likes.add(request.user)
            return Response({'status': 'liked'})
    
    # Views
    @action(detail=True, methods=['post'], permission_classes=[AllowAny])
    def increment_view(self, request, pk=None):
        blog = self.get_object()  # Get the blog post object
        ip_address = self.get_client_ip(request)  # Get client IP address
        
        print(ip_address, 'IP address')

        # Handle unique views (IP address viewed the blog for the first time)
        if not BlogView.objects.filter(blog=blog, ip_address=ip_address).exists():
            print('First time unique view')
            BlogView.objects.create(blog=blog, ip_address=ip_address)
            blog.unique_views += 1  # Increment unique views count

        # Increment regular views count
        blog.views += 1

        # Handle extended views (views that last for more than 30 seconds)
        threshold_time = timezone.now() - timedelta(seconds=30)

        # Check if a recent view from the same IP address exists within the threshold
        recent_view = BlogView.objects.filter(blog=blog, ip_address=ip_address, timestamp__gte=threshold_time).exists()
        
        # track user if the content viewed or not
        track_viewer = BlogView.objects.get(blog=blog, ip_address=ip_address)
        if not recent_view and not track_viewer.has_viewed_content:
    
            print('Extended view counted (view lasting more than 30 seconds)')

                # Create a new BlogView entry for the extended view
                # BlogView.objects.create(blog=blog, ip_address=ip_address, timestamp=timezone.now())
                # Increment extended views count only if the last view was more than 30 seconds ago

            blog.extended_views += 1
            track_viewer.has_viewed_content=True
            track_viewer.save()
            blog.save()
            
        else:
            print('either user has already viewed the given content or threshold requirements not met')

        blog.save()  

        return Response({
            'status': 'View incremented',
            'views': blog.views,
            'unique_views': blog.unique_views,
            'extended_views': blog.extended_views
        })

    def get_client_ip(self, request):
        """Get client IP address from request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
   
   
# comment viewset
class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = CommentSerializer

    def get_queryset(self):
        blog_id = self.request.query_params.get('blog_id')
    
        if blog_id:
           return Comment.objects.filter(blog_id=blog_id)
            # raise ValidationError({'detail': 'blog_id parameter is required to fetch comments.'})
        # Filter comments by blog_id if provided
        return Comment.objects.all()

    def perform_create(self, serializer):
        print('perform create')
        blog_id = self.request.data.get('blog')
        user = self.request.user
    
        # Check if the user has already commented on this blog
        print(Comment.objects.filter(blog_id=blog_id, author=user).exists(),'---exists')
        if Comment.objects.filter(blog_id=blog_id, author=user).exists():
           raise ValidationError({'detail': 'Response already received!'})
           # return Response({'detail': 'Response already recieved !!'}, status=status.HTTP_400_BAD_REQUEST)  this will not work use validationerror instead of sending custon response

        # Save the comment if the user hasn't commented yet
        print('doesnt exist')
        serializer.save(author=user)

    # extra check to prevent multiple comments with same user and blog
    def perform_update(self, serializer):
        print('perform update comment')
        # Get the current comment instance
        comment_instance = self.get_object()

        # Prevent updating the blog field
        validated_data = serializer.validated_data
        validated_data.pop('blog', None)  

        serializer.save(**validated_data)  


class BlogListView(generics.ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = BlogSerializer

    def get_queryset(self):
        queryset = Blog.objects.all()

        # Filter by category slug
        category_slug = self.request.query_params.get('category_slug')
        if category_slug:
            queryset = queryset.filter(categories__slug=category_slug)

        # Filter by topic slug
        topic_slug = self.request.query_params.get('topic_slug')
        if topic_slug:
            queryset = queryset.filter(topics__slug=topic_slug)

        # Filter by date range (created_at)
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            queryset = queryset.filter(created_at__range=[start_date, end_date])

        return queryset

class UserInterestViewSet(viewsets.ModelViewSet):
    serializer_class = UserInterestSerializer
    permission_classes = [IsAuthenticated]
    queryset = UserInterest.objects.all() 

    def get_serializer_class(self):
        # Use different serializers for read and write operations
        if self.action in ['list', 'retrieve']:
            return UserInterestDetailSerializer  # For fetching (GET)
        return UserInterestSerializer  # For posting/updating (POST, PUT, PATCH)

    def get_queryset(self):
        return UserInterest.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        categories = self.request.data.get('categories')
        topics = self.request.data.get('topics')
        if not (categories or topics):
            raise ValidationError({'detail': 'Either categories or Topics must be included!!'})
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        categories = request.data.get('categories', [])
        topics = request.data.get('topics', [])
        print(categories, topics, 'cat top ')
        if not (categories or topics):
            raise ValidationError({'detail': 'Either categories or topics must be included!'})
        return super().update(request, *args, **kwargs)    

    # perform_update vs update ?
    # def perform_update(self, serializer):
    #     user_interest = self.get_queryset().first()
    #     serializer.save(user=user_interest.user)

class RecommendedReadsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_interests = UserInterest.objects.filter(user=request.user).first()

        print(request.COOKIES.get('refresh'), ' refresh cookie')
        print(request.COOKIES.get('access'), ' access cookie')
        
        if not user_interests:
            return Response({"message": "No interests found for the user."}, status=404)

        categories = user_interests.categories.all()
        topics = user_interests.topics.all()

        recommended_blogs = Blog.objects.filter(
            models.Q(categories__in=categories) | models.Q(topics__in=topics)
        ).distinct()

        blog_data = BlogSerializer(recommended_blogs, many=True).data
        
        return Response(blog_data)


# in order to save media files directly from client to s3 we need to generate a presigned url which is more reliable and secure
class GeneratePresignedURLView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            print('Pre-signed URL request by client')

            # Extract file_name and file_type from the request data
            file_name = request.data.get('fileName')
            file_type = request.data.get('fileType')

            if not file_name or not file_type:
                return Response({'error': 'File name and file type are required'}, status=status.HTTP_400_BAD_REQUEST)

            # Call S3Service to generate the presigned URL
            presigned_url = S3Service.generate_presigned_url(file_name, file_type)

            # Return the data using DRF's Response
            return Response({
                'url': presigned_url,
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeleteFileView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            # Extract fileUrl from the request data
            file_url = request.data.get('imageUrl')
            print(file_url, "delete url")
            if not file_url:
                return Response({'error': 'File URL is required'}, status=status.HTTP_400_BAD_REQUEST)

            # Extract the file name (key) from the URL
            file_name = file_url.split('.com/')[-1]
            print("file name", file_name)
            # Call the delete method from S3Service
            S3Service.delete_file_from_s3(file_name)

            # Return a success response
            return Response({'message': 'File deleted successfully'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class GeneratePresignedURLView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         try:
#             # Extract file_name, action, and (optionally) file_type from the request data
#             file_name = request.data.get('fileName')
#             action = request.data.get('action')  # 'upload' or 'delete'
#             file_type = request.data.get('fileType') if action == 'upload' else None
#             print("line 1")
#             if not file_name or not action:
#                 return Response({'error': 'File name and action are required'}, status=status.HTTP_400_BAD_REQUEST)

#             # Generate the appropriate presigned URL based on the action
#             if action == 'upload':
#                 presigned_url = S3Service.generate_presigned_url(file_name, file_type)
#             elif action == 'delete':
#                 presigned_url = S3Service.generate_presigned_delete_url(file_name)
#             else:
#                 return Response({'error': 'Invalid action specified'}, status=status.HTTP_400_BAD_REQUEST)

#             # Return the presigned URL
#             return Response({
#                 'url': presigned_url,
#             }, status=status.HTTP_200_OK)

#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# View to get all categories
# class CategoryListView(generics.ListAPIView):
#     permission_classes = [AllowAny]
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer

# API view to get all topics under a specific category
# class TopicListView(generics.ListAPIView):
#     permission_classes = [AllowAny]
#     serializer_class = TopicSerializer

#     def get_queryset(self):
#         category_slug = self.kwargs.get('category_slug')
#         return Topic.objects.filter(category__slug=category_slug)
