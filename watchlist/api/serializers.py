from rest_framework import serializers
from watchlist.models import Review, WatchList, StreamPlatform

# class DataValidation():
#     def name_length(values):
#         if len(values) < 2:
#             raise serializers.ValidationError('Name is too Short!!')

class ReviewSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        # fields = '__all__'
        exclude = ('watchlist',)

class WatchListSerializer(serializers.ModelSerializer):
    # name_len = serializers.SerializerMethodField()
    # def get_name_len(self, object):
    #         return len(object.name)    
    review = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = WatchList
        fields = '__all__'
        # exclude = ['id']

        # def validate(self, data):
        #     if data['name'] == data['description']:
        #         raise serializers.ValidationError('Name and description must be different')


class StreamPlatformSerializer(serializers.ModelSerializer):
    # watchlist = WatchListSerializer(many=True, read_only=True)
    watchlist = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='WatchList-detail')
    class Meta:
        model = StreamPlatform
        fields = '__all__'



















# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators=[DataValidation.name_length])
#     description = serializers.CharField()
#     active = serializers.BooleanField()

#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active',instance.active)
#         instance.save()
#         return instance

#     def validate(self, data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError('Name and description must be different')

    # def validate_name(self, values):
    #     if len(values) < 2:
    #         raise serializers.ValidationError('Name is too Short!!')