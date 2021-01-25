from django.urls import path
from rest_framework.routers import SimpleRouter

from apps.userAuth.views.v1.views import SendCodeView, UserViewSet


router = SimpleRouter(trailing_slash=False)
router.register('user', UserViewSet, base_name='user')

urlpatterns = [
    path('sendcode', SendCodeView.as_view(), name='sendcode'),
    # path('register', RegisterView.as_view(), name='register'),
    # path('active', ActiveView.as_view(), name='active'),
]

urlpatterns += router.urls
