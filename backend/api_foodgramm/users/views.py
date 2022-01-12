from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import CustomUser, Follow
from .serializer import FollowUserSerializers


@api_view(['GET', 'DELETE'])
def subscribe(request, id):
    """Follow and unfollow users."""
    if request.method == 'GET':
        following = CustomUser.objects.get(id=id)
        if not Follow.objects.filter(user=request.user,
                                     following=following).exists():
            if request.user != following:
                Follow.objects.get_or_create(user=request.user,
                                             following=following)
                serializer = FollowUserSerializers(
                    following,
                    context={'request': request})
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        following = CustomUser.objects.get(id=id)
        if request.user != following:
            Follow.objects.filter(user=request.user,
                                  following=following).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class FollowViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FollowUserSerializers

    def get_queryset(self):
        """Filter queryset by following user."""
        followers = CustomUser.objects.filter(
            followers__user=self.request.user)
        return followers
