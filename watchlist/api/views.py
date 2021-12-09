# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework import mixins
from rest_framework import generics

from watchlist.api.permissions import AdminOrReadOnly, ReviewOrReadOnly
from watchlist.models import WatchList, StreamPlatform, Review
from .serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer

#concrete views

class ReviewCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        movie = WatchList.objects.get(pk=pk)

        user_review = self.request.user
        review_queryset = Review.objects.filter(watchlist=movie, owner=user_review)

        if review_queryset.exists():
            raise ValidationError("you have already reviewed this movie.")

        if movie.num_of_ratings == 0:
            movie.avg_rating = serializer.validated_data['rating']
        else:
            movie.avg_rating = (movie.avg_rating*movie.num_of_ratings+serializer.validated_data['rating'])/(movie.num_of_ratings + 1)
        movie.num_of_ratings += 1
        movie.save()
        serializer.save(watchlist=movie, owner=user_review)


class ReviewListView(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewOrReadOnly]

#mixins views

# class ReviewListView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


#class Based View

# class ReviewDetailView(APIView):
    #   permission_classes = [IsAuthenticated]

#     def get(self, request, pk):
#         review = Review.objects.get(pk=pk)
#         serializer = ReviewSerializer(review)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         review = Review.objects.get(pk=pk)
#         serializer = ReviewSerializer(review, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StreamPlatformListView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        streamplatform = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(streamplatform, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StreamPlatformDetailView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        streamplatform = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(streamplatform, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        streamplatform = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(streamplatform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status={'Error': 'Serializer Error'})

class WatchListView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        watchlist = WatchList.objects.all()
        serializer = WatchListSerializer(watchlist, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class WatchDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer


# class WatchDetailView(APIView):
#     permission_classes = [IsAuthenticated]
#     def get(self, request, pk):
#         try:
#             watchlist = WatchList.objects.get(pk=pk)
#         except:
#             return Response({'Error': 'Movie Not Found'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = WatchListSerializer(watchlist)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         watchlist = WatchList.objects.get(pk=pk)
#         serializer = WatchListSerializer(watchlist, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

#     def delete(self, request, pk):
#         watchlist = WatchList.objects.get(pk=pk)
#         watchlist.delete()
#         return Response('Movie deleted successfully')


# class ReviewListView(APIView):
# permission_classes = [IsAuthenticated]

#     def get(self, request):
#         review = Review.objects.all()
#         serializer = ReviewSerializer(review, many=True)
#         return Response(serializer.data)

#     def post(self, request, *args, **kwargs):
#         serializer = ReviewSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#function based views

# @api_view(['GET','POST'])
#   @permission_classes([IsAuthenticated])
# def movie_list(request):
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data)

#     if request.method == 'POST':
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

# @api_view(['GET','PUT','DELETE'])
# def movie_details(request, pk):
#     if request.method == 'GET':
#         try:
#             movies = Movie.objects.get(pk=pk)
#         except:
#             return Response({'Error': 'Movie Not Found'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = MovieSerializer(movies)
#         return Response(serializer.data)
    
#     if request.method == 'PUT':
#         movies = Movie.objects.get(pk=pk)
#         serializer = MovieSerializer(movies, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
    
#     if request.method == 'DELETE':
#         movies = Movie.objects.get(pk=pk)
#         movies.delete()
#         return Response('Movie deleted successfully')