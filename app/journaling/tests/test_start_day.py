from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from journaling.memo import Memo


class StartDayViewTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="secretpass123",
        )
        self.client.force_login(self.user)

    def test_update_earliest_todo_dates_for_all_matching_tasks(self):
        earliest = date(2026, 8, 10)
        next_date = date(2026, 8, 12)
        selected_date = date(2026, 8, 14)

        memo_earliest_1 = Memo.objects.create(
            user=self.user,
            state="todo",
            description="First earliest task",
            planned_date=earliest,
        )
        memo_earliest_2 = Memo.objects.create(
            user=self.user,
            state="todo",
            description="Second earliest task",
            planned_date=earliest,
        )
        Memo.objects.create(
            user=self.user,
            state="todo",
            description="Later task",
            planned_date=next_date,
        )
        Memo.objects.create(
            user=self.user,
            state="done",
            description="Done task",
            planned_date=date(2026, 8, 9),
        )

        response = self.client.post(
            reverse("journaling:start_day"),
            data={"planned_date": selected_date.isoformat()},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content.decode(),
            {"success": True, "updated": 2, "target_date": selected_date.isoformat()},
        )

        memo_earliest_1.refresh_from_db()
        memo_earliest_2.refresh_from_db()
        self.assertEqual(memo_earliest_1.planned_date, selected_date)
        self.assertEqual(memo_earliest_2.planned_date, selected_date)

        later = Memo.objects.get(description="Later task")
        self.assertEqual(later.planned_date, next_date)

        done = Memo.objects.get(description="Done task")
        self.assertEqual(done.planned_date, date(2026, 8, 9))
