from rest_framework import serializers

from activity.models import Activity


class ActivitySerializer(serializers.HyperlinkedModelSerializer):
    photo_url = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    def get_status(self, activity):
        return activity.get_status_display()

    def get_photo_url(self, activity):
        request = self.context.get('request')
        photo_url = activity.photo.url
        return request.build_absolute_uri(photo_url)

    class Meta:
        model = Activity
        fields = ['id', 'name', 'description', 'photo_url', 'activity_type_id', 'start_date', 'start_time', 'duration',
                  'normal_price', 'member_price', 'number_participants', 'status', 'location', 'only_member']
