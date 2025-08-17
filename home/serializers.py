from rest_framework import serializers
from .models import Kompyuter, Comment

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Comment
        fields = ['id', 'user', 'body', 'created_at']

class KompyuterSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(read_only=True, many=True)

    class Meta:
        model = Kompyuter
        fields = ['id', 'model', 'desc', 'price', 'comments']