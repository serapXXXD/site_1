from django.contrib.auth import authenticate
from django.db.utils import IntegrityError
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from authentication.models import Subscription, Like
from blog.models import Post, Category, Tag
from .serializers import (PostSerializer, PostCreateSerializer, PostPatchSerializer, CategorySerializer,
                          UserSerializer, TagSerializer, LoginSerializer, TokenSerializer, ErrorSerializer,
                          LikeSerializer)
from .permissions import IsAdminOrReadOnly, IsObjectAuthor
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework import mixins
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PostFilter
from drf_yasg.utils import swagger_auto_schema, no_body
from drf_yasg import openapi


User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [IsObjectAuthor]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilter

    def get_serializer_class(self):
        if self.action == 'create':
            return PostCreateSerializer
        elif self.action == "update" or self.action == "partial_update":
            return PostPatchSerializer
        else:
            return PostSerializer

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        sub = Subscription.objects.filter(subscriber=request.user)
        authors = [s.author for s in sub]
        queryset = self.get_queryset().filter(author__in=authors)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            return response
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    @swagger_auto_schema(responses={201: openapi.Response(description='лайк поставлен', schema=LikeSerializer()),
                                    200: openapi.Response(description='лайк удалён', schema=LikeSerializer())
                                    },
                         request_body=no_body)
    @action(methods=['POST'], permission_classes=[IsAuthenticated], detail=True)
    def like(self, request, pk):
        like, created = Like.objects.get_or_create(liker=request.user, liked_post=get_object_or_404(Post, pk=pk))
        likes = like.liked_post.likes.count()
        if created:
            return Response({'likes': likes}, status=status.HTTP_201_CREATED)

        like.delete()
        likes = like.liked_post.likes.count()
        return Response({'likes': likes}, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        if 'search' in self.request.query_params.keys():
            queryset = queryset.filter(
                Q(body__icontains=self.request.query_params.get('search')) |
                Q(title__icontains=self.request.query_params.get('search')))
        return queryset


class GetTokenAPIView(APIView):
    @swagger_auto_schema(responses={200: TokenSerializer(), 400: ErrorSerializer()}, request_body=LoginSerializer())
    def post(self, request):
        if {'username'}.issubset(request.data) and {'password'}.issubset(request.data):
            username = request.data['username']
            password = request.data['password']
            user = authenticate(requset=request, username=username, password=password)
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status.HTTP_200_OK)
            else:
                return Response({'detail': 'не верный лоигн, или пароль'}, status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'отсутсвует лоигн, или пароль'}, status.HTTP_400_BAD_REQUEST)


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
                Subscription.objects.create(
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


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminOrReadOnly]
