from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LawyerViewSet, CPDPointViewSet, LawyerCPDView

router = DefaultRouter()
router.register(r'lawyers', LawyerViewSet)
router.register(r'cpd-points', CPDPointViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('lawyers/<int:lawyer_id>/cpd-total/', LawyerCPDView.as_view(), name='lawyer_cpd_total'),
]