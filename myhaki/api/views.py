from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated
from django.db.models import Sum
from lawyers.models import Lawyer, CPDPoint
from .serializers import LawyerSerializer, CPDPointSerializer

class IsLSKAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'lsk_admin'

class LawyerViewSet(viewsets.ModelViewSet):
    queryset = Lawyer.objects.all()
    serializer_class = LawyerSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'create', 'update', 'partial_update', 'destroy']:
            return [IsLSKAdmin()]
        return super().get_permissions()

class CPDPointViewSet(viewsets.ModelViewSet):
    queryset = CPDPoint.objects.all()
    serializer_class = CPDPointSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsLSKAdmin()]
        return [IsAuthenticated()]

class LawyerCPDView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, lawyer_id):
        total_points = CPDPoint.objects.filter(lawyer_id=lawyer_id).aggregate(total=Sum('points_earned'))['total'] or 0
        return Response({'lawyer_id': lawyer_id, 'total_cpd_points': total_points})