from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import FollowViewSet, subscribe

router_v1 = DefaultRouter()
router_v1.register('users/subscriptions', FollowViewSet,
                   basename='subscriptions')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('users/<int:id>/subscribe/', subscribe),
]
