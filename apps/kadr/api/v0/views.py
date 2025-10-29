from rest_framework import generics
from apps.kadr.models import AcademicYear
from .serializer import AcademicYearSerializer
from rest_framework.permissions import AllowAny


class AcademicYearAPIView(generics.ListAPIView):
    queryset = AcademicYear.objects.prefetch_related(
        'courses__directions__subjects'
    ).all().order_by('-id')
    serializer_class = AcademicYearSerializer
    permission_classes = [AllowAny]


academic_year_list_view = AcademicYearAPIView.as_view()
