from rest_framework.viewsets import ReadOnlyModelViewSet

from activity.models import Activity
from api.serializers import ActivitySerializer


class ActivityViewSet(ReadOnlyModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
