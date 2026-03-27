from rest_framework.routers import DefaultRouter
from .views import CircuitViewSet

router = DefaultRouter()
router.register(r'circuits', CircuitViewSet, basename='circuit')

urlpatterns = router.urls