from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.views.generic import TemplateView

from config.settings.base import BASE_DIR

from .services import MarkdownRenderer


class DocubaseIndexView(LoginRequiredMixin, TemplateView):
    """Display list of applications with documentation and core docs."""

    template_name = "docubase/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        apps_with_docs = self._get_apps_with_docs()

        # Get core documentation index if it exists
        core_docs_path = BASE_DIR / "core" / "docs" / "index.md"
        core_content = ""
        if core_docs_path.exists():
            core_content = self._read_and_convert_markdown(core_docs_path)

        context.update(
            {
                "title": "Documentation",
                "apps": apps_with_docs,
                "core_content": core_content,
            }
        )
        return context

    def _get_apps_with_docs(self):
        """Find all apps with docs folders and return their info."""
        apps_dir = BASE_DIR / "app"
        apps = []

        if not apps_dir.exists():
            return apps

        for app_folder in apps_dir.iterdir():
            if app_folder.is_dir():
                docs_path = app_folder / "docs"
                if docs_path.exists() and docs_path.is_dir():
                    app_name = app_folder.name
                    docs_count = len(list(docs_path.glob("*.md")))
                    apps.append(
                        {
                            "name": app_name,
                            "display_name": self._format_app_name(app_name),
                            "docs_count": docs_count,
                        }
                    )

        return sorted(apps, key=lambda x: x["name"])

    @staticmethod
    def _format_app_name(name):
        """Convert app name to display name (e.g., 'jackietrade' -> 'Jackie Trade')."""
        # Handle camelCase
        result = []
        for i, char in enumerate(name):
            if i > 0 and char.isupper():
                result.append(" ")
            result.append(char)
        return "".join(result).title()

    def _read_and_convert_markdown(self, file_path):
        """Read a markdown file and convert to HTML."""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()
            return MarkdownRenderer.render(content)
        except Exception as e:
            return f"<p>Error reading file: {e}</p>"


class DocubaseAppListView(LoginRequiredMixin, TemplateView):
    """Display list of documents for a specific application."""

    template_name = "docubase/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        app_name = kwargs.get("app")

        docs_path = BASE_DIR / "app" / app_name / "docs"
        if not docs_path.exists() or not docs_path.is_dir():
            raise Http404(f"App '{app_name}' not found or has no docs")

        documents = self._get_documents(docs_path, app_name)

        # Get the index.md content if it exists
        index_path = docs_path / "index.md"
        index_content = ""
        if index_path.exists():
            index_content = self._read_and_convert_markdown(index_path)

        context.update(
            {
                "title": f"{self._format_app_name(app_name)} Documentation",
                "current_app": app_name,
                "documents": documents,
                "index_content": index_content,
            }
        )
        return context

    def _get_documents(self, docs_path, app_name):
        """Get list of documents in the app's docs folder."""
        documents = []

        for md_file in sorted(docs_path.glob("*.md")):
            if md_file.name != "index.md":
                doc_name = md_file.stem
                documents.append(
                    {
                        "name": doc_name,
                        "display_name": self._format_doc_name(doc_name),
                        "app": app_name,
                    }
                )

        return documents

    @staticmethod
    def _format_doc_name(name):
        """Convert document name to display name."""
        return name.replace("_", " ").title()

    @staticmethod
    def _format_app_name(name):
        """Convert app name to display name."""
        result = []
        for i, char in enumerate(name):
            if i > 0 and char.isupper():
                result.append(" ")
            result.append(char)
        return "".join(result).title()

    @staticmethod
    def _read_and_convert_markdown(file_path):
        """Read a markdown file and convert to HTML."""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()
            return MarkdownRenderer.render(content)
        except Exception as e:
            return f"<p>Error reading file: {e}</p>"


class DocubaseDocumentView(LoginRequiredMixin, TemplateView):
    """Display a specific document from an application."""

    template_name = "docubase/document.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        app_name = kwargs.get("app")
        doc_name = kwargs.get("doc")

        docs_path = BASE_DIR / "app" / app_name / "docs"
        doc_path = docs_path / f"{doc_name}.md"

        if not doc_path.exists():
            raise Http404(f"Document '{doc_name}' not found in app '{app_name}'")

        content = self._read_and_convert_markdown(doc_path)

        context.update(
            {
                "title": f"{self._format_doc_name(doc_name)} - {
                    self._format_app_name(app_name)
                }",
                "current_app": app_name,
                "document_name": doc_name,
                "display_name": self._format_doc_name(doc_name),
                "content": content,
            }
        )
        return context

    @staticmethod
    def _format_doc_name(name):
        """Convert document name to display name."""
        return name.replace("_", " ").title()

    @staticmethod
    def _format_app_name(name):
        """Convert app name to display name."""
        result = []
        for i, char in enumerate(name):
            if i > 0 and char.isupper():
                result.append(" ")
            result.append(char)
        return "".join(result).title()

    @staticmethod
    def _read_and_convert_markdown(file_path):
        """Read a markdown file and convert to HTML."""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()
            return MarkdownRenderer.render(content)
        except Exception as e:
            return f"<p>Error reading file: {e}</p>"
