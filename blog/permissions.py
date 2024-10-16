from rest_framework.permissions import BasePermission

# class IsAuthorOrHasBlogPermission(BasePermission):
#     """
#     Custom permission to only allow authors of a blog to edit it,
#     or users with specific permissions to create/edit blogs.
#     """

#     def has_permission(self, request, view):
#         print(request.user.get_all_permissions(), 'print permission')

#         # Check if user has the permission to add or change posts
#         if request.user.role == "author":
#             print('author')
#             return True
#         if request.method in ['POST'] and request.user.has_perm('blog.add_post'):
#             return True
#         if request.method in ['PUT', 'PATCH'] and request.user.has_perm('blog.change_post'):
#             return True
        
#         return False


class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of a blog post to edit or delete it.
    Others can only view the posts.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            print('not an owner')
            return True
        print('owner', obj.author == request.user)
        # Write permissions are only allowed to the author of the post.
        return obj.author == request.user
