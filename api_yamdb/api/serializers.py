from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User."""
    class Meta:
        model = CustomUser
        fields = (
            'username', 'email',
            'role', 'bio',
            'first_name', 'last_name',
        )


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор для создания объектов класса User."""
    class Meta:
        model = CustomUser
        fields = ('username', 'email')

    def validate(self, data):
        if data['username'].lower() == 'me':
            raise ValidationError(
                message='Использовать имя "me" в качестве username запрещено!'
            )
        if CustomUser.objects.filter(username=data.get('username')):
            raise serializers.ValidationError(
                'Пользователь с таким "username" уже существует'
            )
        if CustomUser.objects.filter(email=data.get('email')):
            raise serializers.ValidationError(
                'Пользователь с таким "email" уже существует'
            )
        return data


class ObtainTokenSerializer(serializers.ModelSerializer):
    """Сериализатор для объектов класса User при получении токена."""
    username = serializers.RegexField(
        regex=r"^[\w.@+-]+$", max_length=150, required=True
    )
    confirmation_code = serializers.CharField(max_length=150, required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'confirmation_code')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""

    class Meta:
        model = Category
        exclude = ('id', )


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""

    class Meta:
        model = Genre
        exclude = ('id', )


class TitleGETSerializer(serializers.ModelSerializer):
    """Сериализатор для объектов класса Title для обработки GET-запросов"""
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitlePOSTSerializer(serializers.ModelSerializer):
    """Сериализатор для объектов класса Title
    для обработки небезопасных запросов"""
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для класса отзывов."""
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review
        read_only_fields = ('title', 'pub_date', 'author')

    def validate(self, data):
        """Запрещает пользователям оставлять повторные отзывы."""
        if not self.context.get('request').method == 'POST':
            return data
        author = self.context.get('request').user
        title_id = self.context.get('view').kwargs.get('title_id')
        if Review.objects.filter(author=author, title=title_id).exists():
            raise serializers.ValidationError(
                'Вы не можете оставить отзыв повторно.'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для класса комментариев к отзывам."""
    author = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
        read_only_fields = ('author', 'review', 'pub_date')
