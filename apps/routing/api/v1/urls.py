from rest_framework.routers import DefaultRouter
from .views import RoutePlanViewSet

router = DefaultRouter()
router.register(r'routes', RoutePlanViewSet, basename='route')

urlpatterns = router.urls