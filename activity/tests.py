from datetime import datetime, timedelta

from django.test import TestCase

from activity.models import Activity, ActivityType


class ActivityTestCase(TestCase):
    def setUp(self):
        self.now = datetime.now()
        activity_type = ActivityType.objects.create(name='Yoga')
        Activity.objects.create(name='Classe yoga', start_date=self.now.date(), start_time=self.now.time(),
                                description='Classe dels dimecres de yoga....', activity_type_id=activity_type,
                                duration=60.0, normal_price=0, number_participants=10, location='41.394082, 2.140952')

    def test_activity_creation(self):
        yoga_type = ActivityType.objects.get(name='Yoga')
        yoga_class = Activity.objects.get(activity_type=yoga_type, start_time=self.now.time(),
                                          start_date=self.now.date(), location='41.394082, 2.140952')
        self.assertEqual(yoga_class.duration, 60)
        self.assertEqual(yoga_class.description, 'Classe dels dimecres de yoga....')
        self.assertEqual(yoga_class.name, 'Classe yoga')
        self.assertEqual(yoga_class.normal_price, 0)
        self.assertEqual(yoga_class.number_participants, 10)
        self.assertEqual(yoga_class.only_member, False)
        self.assertEqual(yoga_class.status, Activity.STATUS_PENDING)

    def test_activity_cancel(self):
        yoga_type = ActivityType.objects.get(name='Yoga')
        yoga_class = Activity.objects.get(activity_type=yoga_type, start_time=self.now.time(),
                                          start_date=self.now.date(), location='41.394082, 2.140952')
        yoga_class.status = yoga_class.STATUS_CANCELLED
        yoga_class.save()
        yoga_class = Activity.objects.get(activity_type=yoga_type, start_time=self.now.time(),
                                          start_date=self.now.date(), location='41.394082, 2.140952')
        self.assertEqual(yoga_class.status, yoga_class.STATUS_CANCELLED)

    def test_activity_ended(self):
        yoga_type = ActivityType.objects.get(name='Yoga')
        yoga_class = Activity.objects.get(activity_type=yoga_type, start_time=self.now.time(),
                                          start_date=self.now.date(), location='41.394082, 2.140952')
        yoga_class.start_date -= timedelta(days=1)
        yoga_class.start
        self.assertEqual(yoga_class.status, yoga_class.STATUS_ENDED)
