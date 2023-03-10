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


class UserSerializerReadOnly(serializers.ModelSerializer):
    """Сериализатор для модели User, позволяющий
    осуществлять только безопасные запросы."""
    role = serializers.CharField(read_only=True)

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
        if data['username'] == 'me':
            raise ValidationError(
                message='Использовать имя "me" в качестве username запрещено!'
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
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitlePOSTSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='Slug',
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='Slug',
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


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для класса комментариев к отзывам."""
    author = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
        read_only_fields = ('author', 'review', 'pub_date')
