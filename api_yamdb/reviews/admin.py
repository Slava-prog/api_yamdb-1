from django.contrib import admin

from .models import Comment, Review


@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'text',
                    'pub_date',
                    'author',
                    'review'
                    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'text',
                    'author',
                    'score',
                    'pub_date'
                    )
