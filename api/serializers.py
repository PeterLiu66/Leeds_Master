from rest_framework import serializers

from user.models import Rate, Movie, Comment


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate

    def to_representation(self, instance):
        return {'Name': instance.movie.name, 'Rating': instance.mark, 'Created at': instance.create_time.strftime('%Y-%m-%d %H:%M:%S')}


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment

    def to_representation(self, instance):
        return {'Name': instance.movie.name, 'Comments': instance.content,'Comments_id': instance.pk, 'Created at': instance.create_time.strftime('%Y-%m-%d %H:%M:%S'), 'Likes': instance.likecomment_set.count()}


class CollectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie

    def to_representation(self, instance):
        return {'Name': instance.name, 'Director':instance.director,'Release Date':instance.years,'Views':instance.num}


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['name', 'image_link', 'id', 'years', 'd_rate', 'director']
