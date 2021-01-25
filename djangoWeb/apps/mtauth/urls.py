from rest_framework.routers import SimpleRouter
from .views import UserRegisterView
from django.urls import path


router = SimpleRouter(trailing_slash=False)
router.register('register', UserRegisterView, base_name='register')

# urlpatterns = [
#     path('register/', UserRegisterView.as_view())
# ]

urlpatterns = router.urls

