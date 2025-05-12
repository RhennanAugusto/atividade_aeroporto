from rest_framework.routers import DefaultRouter
from .views import PassageiroViewSet, VooViewSet, PortaoViewSet

router = DefaultRouter()
router.register(r'passageiros', PassageiroViewSet, basename='passageiro')
router.register(r'voos', VooViewSet, basename='voo')
router.register(r'portoes', PortaoViewSet, basename='portao')

urlpatterns = router.urls
