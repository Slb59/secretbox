import os
from datetime import date
from getpass import getpass

from django.core.management.base import BaseCommand, CommandError
from PyPDF2 import PdfWriter


class Command(BaseCommand):
    help = "Merge PDF files"

    def add_arguments(self, parser):
        parser.add_argument("folder", type=str, help="Folder containing PDF files")

    def handle(self, *args, **options):
        folder_path = options["folder"]
        output_filename = f"{date.today():%Y%m%d}-merged.pdf"

        if not os.path.isdir(folder_path):
            raise CommandError(f"Folder {folder_path} does not exist")

        pdf_files = sorted(
            [
                f
                for f in os.listdir(folder_path)
                if f.lower().endswith(".pdf") and f != output_filename
            ]
        )

        if not pdf_files:
            raise CommandError(f"No PDF files found in {folder_path}")

        merger = PdfWriter()

        for pdf_file in pdf_files:
            full_path = os.path.join(folder_path, pdf_file)
            self.stdout.write(f"Merging file {pdf_file}")
            merger.append(full_path)

        password = getpass("Enter password for merged PDF: ")
        if not password:
            raise CommandError("The PDF password cannot be empty")

        output_file = os.path.join(folder_path, output_filename)
        merger.encrypt(password)
        merger.write(output_file)
        merger.close()

        self.stdout.write(
            self.style.SUCCESS(f"Merged PDF files saved to {output_file}")
        )
