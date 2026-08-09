from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Liste des utilisateurs"

    def handle(self, *args, **options):
        users = User.objects.all()
        if not users:
            self.stdout.write(self.style.WARNING("No users found."))
            return

        self.stdout.write(self.style.SUCCESS(f"Found {users.count()} user(s):"))
        for user in users:
            self.stdout.write(f"{user.trigram}- {user.email}")
