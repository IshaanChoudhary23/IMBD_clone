from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from watchlist_app.models import WatchList,StreamPlatform,Review
from watchlist_app.api.serializers import WatchListSerializer,StreamPlateformSerializer,ReviewSerializer
# from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import  APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework.throttling import AnonRateThrottle,UserRateThrottle,ScopedRateThrottle
from watchlist_app.api.permissions import AdminorReadOnly,ReviewUserOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from watchlist_app.api.pagination import WatchListPagination

class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk=self.kwargs.get('pk')
        watchlist=WatchList.objects.get(pk=pk)

        # serializer.save(watchlist=watchlist)
        review_user=self.request.user
        review_queryset=Review.objects.filter(watchlist=watchlist,review_user=review_user)
        if review_queryset.exists():
            raise ValidationError("you have laready review this itme!!!")



        if watchlist.number_rating==0:
            watchlist.avg_rating=serializer.validated_data['rating']
        else:
            watchlist.avg_rating=(watchlist.avg_rating+serializer.validated_data['rating'])/2

        watchlist.number_rating=watchlist.number_rating+1
        watchlist.save()


        serializer.save(watchlist=watchlist,review_user=review_user)





class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle,UserRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields=['reviewuser__username','active']
    def get_queryset(self):
        pk=self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # throttle_classes = [AnonRateThrottle,UserRateThrottle]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope='review-detail'

    # permission_classes = [IsAuthenticated]






# class ReviewDetail(mixins.RetrieveModelMixin,generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#
#
#
# class ReviewList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
















class StreamPlatformAV(APIView):
    def get(self,request):
        platform=StreamPlatform.objects.all()
        serializer=StreamPlateformSerializer(platform,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer=StreamPlateformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class StreamPlatformDetailAV(APIView):
    def get(self,request,pk):
        try:
            platform=StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error':'streamplatform not found'},status=status.HTTP_404_NOT_FOUND)

        serializer=StreamPlateformSerializer(platform)
        return Response(serializer.data)

    def put(self,request,pk):
        platform=StreamPlatform.objects.get(pk=pk)
        serializer=StreamPlateformSerializer(platform,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WatchListAV(APIView):
    pagination_class=WatchListPagination
    def get(self,request):
        movies = WatchList.objects.all()
        serializer=WatchListSerializer(movies,many=True)
        return Response(serializer.data)


    def post(self,request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class WatchDetailAV(APIView):


    def get(self,request,pk):
        try:
            movie=WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'error':'movie not found'},status=status.HTTP_400_BAD_REQUEST)
        serializer=WatchListSerializer(movie)
        return Response(serializer.data)

    def put(self,request,pk):
        movie=WatchList.objects.get(pk=pk)
        serializer=WatchListSerializer(movie,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    def delete(self,request,pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
































































# @api_view(['GET', 'POST'])
# def movie_list(request):
#     if request.method =='GET':
#         movies=Movie.objects.all()
#         serializer=MovieSerializer(movies,many=True)
#         return Response(serializer.data)
#     if request.method=="POST":
#         serializer=MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
#
# @api_view(['GET', 'PUT','DELETE'])
# def movie_detail(request,pk):
#     if request.method=="GET":
#         try:
#             movie=Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist:
#             return Response({'error':'movie not found'},status=status.HTTP_400_BAD_REQUEST)
#         serializer=MovieSerializer(movie)
#         return Response(serializer.data)
#     if request.method=="PUT":
#         movie=Movie.objects.get(pk=pk)
#         serializer=MovieSerializer(movie,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#     if request.method=="DELETE":
#         movie=Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
#
