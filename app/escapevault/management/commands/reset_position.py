from django.core.management.base import BaseCommand
from escapevault.models import NomadePosition
from tests.factories.nomadeposition import NomadePositionFactory


class Command(BaseCommand):
    help = "Réinitialise les NomadePosition avec des données de test"

    def handle(self, *args, **kwargs):
        NomadePosition.objects.all().delete()
        self.stdout.write("Toutes les NomadePosition supprimées.")

        np = NomadePositionFactory(category="home")
        np.save()
        for _ in range(3):
            np = NomadePositionFactory(category="nomade")
            np.save()

        self.stdout.write(self.style.SUCCESS("4 NomadePosition créées."))
