from rest_framework.routers import DefaultRouter
from .views import BinViewSet

router = DefaultRouter()
router.register(r'bins', BinViewSet, basename='bin')

urlpatterns = router.urls