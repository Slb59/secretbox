from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Creation d'un utilisateur"

    def add_arguments(self, parser):
        parser.add_argument("email", type=str, help="Email of the user to create")
        parser.add_argument("password", type=str, help="Password of the user to create")
        parser.add_argument("trigram", type=str, help="Trigram of the user to create")

    def handle(self, *args, **options):
        email = options["email"]
        password = options["password"]

        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.ERROR(f"User with email {email} already exists.")
            )
            return

        user = User.objects.create_user(email=email, password=password)
        user.save()
        self.stdout.write(
            self.style.SUCCESS(f"User with email {email} created successfully.")
        )
