from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from blog.models import Post
from .serializers import PostSerializer, PostCreateSerializer, PostPatchSerializer
from .permissions import IsAuthorOnly
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView


class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.prefetch_related('tags')
    serializer_class = PostSerializer


class PostCreateAPIView(generics.CreateAPIView):

    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GetTokenAPIView(APIView):
    def post(self, request):
        if {'username'}.issubset(request.data) and {'password'}.issubset(request.data):
            username = request.data['username']
            password = request.data['password']
            print(request.data)
            user = authenticate(requset=request, username=username, password=password)
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                print(type(token))
                return Response({'token': token.key}, status.HTTP_200_OK)
            else:
                return Response({'detail': 'не верный лоигн, или пароль'}, status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'отсутсвует лоигн, или пароль'}, status.HTTP_400_BAD_REQUEST)


class PatchPostAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthorOnly]
    queryset = Post.objects.all()
    serializer_class = PostPatchSerializer


class DeletePostAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthorOnly]
    queryset = Post.objects.all()
