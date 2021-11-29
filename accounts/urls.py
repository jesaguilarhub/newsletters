from rest_framework.routers import DefaultRouter
from accounts.views import AccountViewSet

router = DefaultRouter()
router.register('accounts', AccountViewSet)

urlpatterns = router.urls