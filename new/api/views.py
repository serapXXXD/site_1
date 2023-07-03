from django.contrib.auth import authenticate
from django.db.utils import IntegrityError
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from authentication.models import Subscription
from blog.models import Post, Category
from .serializers import PostSerializer, PostCreateSerializer, PostPatchSerializer, CategorySerializer, UserSerializer
from .permissions import IsAuthorOnly, IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework import mixins
from django.shortcuts import get_object_or_404

User = get_user_model()


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


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class UserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=['POST'], detail=True)
    def subscribe(self, request, pk):
        author = get_object_or_404(User, pk=pk)

        if request.user != author:
            try:
                subscription = Subscription.objects.create(
                    subscriber=request.user, author=author)
            except IntegrityError:
                return Response({'error': 'уже подписан'}, status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'на себя нельзя подписаться'}, status.HTTP_400_BAD_REQUEST)

        return Response({'detail': 'вы успешно подписались'}, status.HTTP_201_CREATED)

    @action(methods=['DELETE'], detail=True)
    def unsubscribe(self, request, pk):
        unsubscribe = Subscription.objects.filter(author_id=pk, subscriber=request.user)

        if unsubscribe.exists():
            unsubscribe.delete()
            return Response({'detail': 'Вы успешно отписались'}, status.HTTP_201_CREATED)
        else:
            return Response({'error': 'подписка не найдена'}, status.HTTP_400_BAD_REQUEST)
