import os

from django.core.management.base import BaseCommand, CommandError
from PyPDF2 import PdfMerger


class Command(BaseCommand):
    help = "Merge PDF files"

    def add_arguments(self, parser):
        parser.add_argument("folder", type=str, help="Folder containing PDF files")

    def handle(self, *args, **options):
        folder_path = options["folder"]

        if not os.path.isdir(folder_path):
            raise CommandError(f"Folder {folder_path} does not exist")

        pdf_files = sorted(
            [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]
        )

        if not pdf_files:
            raise CommandError(f"No PDF files found in {folder_path}")

        merger = PdfMerger()

        for pdf_file in pdf_files:
            full_path = os.path.join(folder_path, pdf_file)
            self.stdout.write(f"Merging file {pdf_file}")
            merger.append(full_path)

        output_file = os.path.join(folder_path, "merged.pdf")
        merger.write(output_file)
        merger.close()

        self.stdout.write(
            self.style.SUCCESS(f"Merged PDF files saved to {output_file}")
        )
