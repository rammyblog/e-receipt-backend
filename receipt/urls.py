from rest_framework.routers import DefaultRouter
from .views import ReceiptViewsets


router = DefaultRouter()
router.register(r'', ReceiptViewsets, basename='receipt')
urlpatterns = router.urls