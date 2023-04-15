
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status,generics
from .models import BlogPost,Comment
from .serializers import BlogPostSerializer,CommentSerializer
from django.db.models import Q
from rest_framework.filters import SearchFilter
from django.utils import timezone
from rest_framework.exceptions import PermissionDenied



logger = logging.getLogger(__name__)


#===================================================#
# Blog post create, view, update, delete starts     #                
#===================================================#


class BlogPostAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        try:
            blog_posts = BlogPost.objects.all()
            serializer = BlogPostSerializer(blog_posts, many=True)
            return Response({'status': 'success', 'message': 'Blog posts fetched successfully', 'data': serializer.data})
        except Exception as e:
            logger.error(f"Error fetching blog posts: {str(e)}")
            return Response({'status': 'error', 'message': 'Failed to fetch blog posts', 'data': None},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = BlogPostSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response({ 'data': serializer.data, 'message': 'Blog post created successfully','status': 'success',},
                                status=status.HTTP_201_CREATED)
            return Response({ 'data': serializer.errors,'message': 'Failed to create blog post','status': 'error',},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating blog post: {str(e)}")
            return Response({ 'data': None,'message': 'Failed to create blog post','status': 'error',},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    def put(self, request, pk):
        try:
            blog_post = BlogPost.objects.get(pk=pk)
            if request.user != blog_post.user:
                raise PermissionDenied("You do not have permission to edit this blog post.")
            serializer = BlogPostSerializer(blog_post, data=request.data)
            updated_at = timezone.now()
            if serializer.is_valid():
                serializer.save()
                return Response({'status': 'success', 'message': 'Blog post updated successfully', 'data': serializer.data})
            return Response({'message': 'Failed to update blog post', 'data': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        except BlogPost.DoesNotExist:
            return Response({'status': 'error', 'message': 'Blog post not found', 'data': None},
                            status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied as e:
            return Response({'status': 'error', 'message': str(e), 'data': None},
                            status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            logger.error(f"Error updating blog post: {str(e)}")
            return Response({'status': 'error', 'message': 'Failed to update blog post', 'data': None},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            blog_post = BlogPost.objects.get(pk=pk)
            if request.user != blog_post.user:
                raise PermissionDenied("You do not have permission to delete this blog post.")
            blog_post.delete()
            return Response({'status': 'success', 'message': 'Blog post deleted successfully'},
                            status=status.HTTP_204_NO_CONTENT)
        except BlogPost.DoesNotExist:
            return Response({'status': 'error', 'message': 'Blog post not found'},
                            status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied as e:
            return Response({'status': 'error', 'message': str(e)},
                            status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            logger.error(f"Error deleting blog post: {str(e)}")
            return Response({'status': 'error', 'message': 'Failed to delete blog post'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#================================================#
# Blog post create, view, update, delete ends    #                
#================================================#

#================================================#
# Blog post comment creation and view starts     #                
#================================================#

class CommentCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = CommentSerializer

    def get(self, request):
        try:
            comment_obj = Comment.objects.all()
            blog_post_id = request.query_params.get('blog_post', None)
            if blog_post_id is not None:
                comment_obj = comment_obj.filter(blog_post_id=blog_post_id)
            serializer = CommentSerializer(comment_obj, many=True)
            return Response({'status': 'success', 'message': 'Comments fetched successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error fetching comments: {str(e)}")
            return Response({'status': 'error', 'message': 'Error fetching comments', 'data': []}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            blog_post = BlogPost.objects.get(id=request.data['blog_post'])
        except BlogPost.DoesNotExist:
            logger.error(f"Blog post does not exist with id {request.data['blog_post']}")
            return Response({'status': 'error', 'message': 'Blog post does not exist', 'data': {}}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, blog_post=blog_post)
            return Response({'status': 'success', 'message': 'Comment created successfully'})
        

#============================================#
#   Blog post comment creation views ends    #                
#============================================#



#============================================#
#           Blog post search starts          #                
#============================================#


class BlogPostSearchAPIView(generics.ListAPIView):
    
    serializer_class = BlogPostSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', None)
        if query is not None:
            queryset = BlogPost.objects.filter(title__icontains=query) | BlogPost.objects.filter(content__icontains=query)
        else:
            queryset = BlogPost.objects.all()
        return queryset

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            response_data = {'status': 'success', 'message': 'Blog posts retrieved successfully', 'data': serializer.data}
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(str(e))
            response_data = {'status': 'error', 'message': 'Failed to retrieve blog posts', 'data': None}
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#============================================#
#           Blog post search ends            #                
#============================================#
