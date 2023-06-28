from rest_framework import serializers
from blog.models import Post, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']


class PostSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True)
    author = serializers.StringRelatedField()
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ('author',)


class PostPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'body')
