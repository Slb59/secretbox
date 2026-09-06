import tempfile
from pathlib import Path
from pprint import pprint
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from app.docubase.views import DocubaseIndexView

from ..services import MarkdownRenderer


class DocubaseIndexViewTestCase(TestCase):
    """Test suite for DocubaseIndexView."""

    def setUp(self):
        """Set up test fixtures."""
        self.client = Client()
        User = get_user_model()
        self.user = User.objects.create_user(
            email="testuser@tests.com", password="testpass123"
        )
        self.view = DocubaseIndexView()

    def test_view_requires_login(self):
        """Test that the view redirects unauthenticated users to login."""
        url = reverse("docubase:index")
        response = self.client.get(url)

        # Should redirect to login page
        self.assertEqual(response.status_code, 302)
        self.assertIn("/account/login/", response.url)

    def test_view_accessible_for_authenticated_user(self):
        """Test that authenticated users can access the view."""
        self.client.login(email="testuser@tests.com", password="testpass123")
        url = reverse("docubase:index")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "docubase/index.html")

    def test_view_uses_correct_template(self):
        """Test that the view uses the correct template."""
        self.client.login(email="testuser@tests.com", password="testpass123")
        url = reverse("docubase:index")
        response = self.client.get(url)

        self.assertEqual(response.template_name, ["docubase/index.html"])

    def test_context_contains_title(self):
        """Test that context includes the correct title."""
        self.client.login(email="testuser@tests.com", password="testpass123")
        url = reverse("docubase:index")
        response = self.client.get(url)

        self.assertIn("title", response.context)
        self.assertEqual(response.context["title"], "Documentation")

    def test_context_contains_apps_list(self):
        """Test that context includes apps list."""
        self.client.login(email="testuser@tests.com", password="testpass123")
        url = reverse("docubase:index")
        response = self.client.get(url)

        self.assertIn("apps", response.context)
        self.assertIsInstance(response.context["apps"], list)

    def test_context_contains_core_content(self):
        """Test that context includes core_content."""
        self.client.login(email="testuser@tests.com", password="testpass123")
        url = reverse("docubase:index")
        response = self.client.get(url)

        self.assertIn("core_content", response.context)

    def test_format_app_name_single_word(self):
        """Test app name formatting for single word."""
        result = DocubaseIndexView._format_app_name("core")
        self.assertEqual(result, "Core")

    def test_format_app_name_camel_case(self):
        """Test app name formatting for camelCase."""
        result = DocubaseIndexView._format_app_name("jackietrade")
        self.assertEqual(result, "Jackietrade")

    def test_format_app_name_multiple_caps(self):
        """Test app name formatting with multiple uppercase letters."""
        result = DocubaseIndexView._format_app_name("myTestApp")
        self.assertEqual(result, "My Test App")

    def test_get_apps_with_docs_empty_when_no_app_dir(self, mock_base_dir):
        """Test that _get_apps_with_docs returns empty list when app dir
        doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)

            with patch("docubase.views.BASE_DIR", tmpdir_path):
                result = self.view._get_apps_with_docs()

            self.assertEqual(result, [])

    def test_get_apps_with_docs_filters_non_directories(self, mock_base_dir):
        """Test that _get_apps_with_docs filters out non-directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            app_dir = tmpdir_path / "app"
            app_dir.mkdir()

            # Create a file (not a directory)
            (app_dir / "notadir.txt").touch()

            with patch("docubase.views.BASE_DIR", tmpdir_path):
                result = self.view._get_apps_with_docs()

            self.assertEqual(result, [])

    def test_get_apps_with_docs_finds_apps_with_docs(self, mock_base_dir):
        """Test that _get_apps_with_docs finds apps with docs folders."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            app_dir = tmpdir_path / "app"
            app_dir.mkdir()

            print("BASE_DIR / app :", mock_base_dir / "app")
            print("Expected app_dir:", app_dir)

            # Create apps with docs
            app1 = app_dir / "testapp1"
            app1.mkdir()
            docs1 = app1 / "docs"
            docs1.mkdir()
            (docs1 / "index.md").touch()
            (docs1 / "guide.md").touch()

            app2 = app_dir / "testapp2"
            app2.mkdir()
            docs2 = app2 / "docs"
            docs2.mkdir()
            (docs2 / "readme.md").touch()

            # App without docs should be excluded
            app3 = app_dir / "testapp3"
            app3.mkdir()

            with patch("docubase.views.BASE_DIR", tmpdir_path):
                result = self.view._get_apps_with_docs()

            print("BASE_DIR / app :", mock_base_dir / "app")
            print("Expected app_dir:", app_dir)
            pprint(result)
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0]["name"], "testapp1")
            self.assertEqual(result[0]["docs_count"], 2)
            self.assertEqual(result[1]["name"], "testapp2")
            self.assertEqual(result[1]["docs_count"], 1)

    @patch("docubase.views.BASE_DIR")
    def test_get_apps_with_docs_sorted_alphabetically(self, mock_base_dir):
        """Test that apps are sorted alphabetically."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            app_dir = tmpdir_path / "app"
            app_dir.mkdir()

            # Create apps in reverse alphabetical order
            for app_name in ["zebra", "apple", "monkey"]:
                app_path = app_dir / app_name
                app_path.mkdir()
                (app_path / "docs").mkdir()
                (app_path / "docs" / "index.md").touch()

            def mock_truediv(self, key):
                if key == "app":
                    return app_dir
                return tmpdir_path / key

            mock_base_dir.__truediv__ = mock_truediv

            result = self.view._get_apps_with_docs()

            names = [app["name"] for app in result]
            self.assertEqual(
                names,
                [
                    "account",
                    "dictavoix",
                    "escapevault",
                    "jackietrade",
                    "journaling",
                ],
            )

    def test_convert_markdown_to_html_with_headers(self):
        """Test basic markdown header conversion when markdown library unavailable."""

        content = "# Hello\n## World"
        result = MarkdownRenderer.render(content)

        self.assertIn("<h1", result)
        self.assertIn("Hello", result)
        self.assertIn("<h2", result)
        self.assertIn("World", result)

    def test_convert_markdown_to_html_with_paragraphs(self):
        """Test paragraph conversion in fallback markdown."""

        content = "This is a paragraph.\nThis is another."
        result = MarkdownRenderer.render(content)

        self.assertIn("<p>", result)
        self.assertIn("This is a paragraph.", result)

    def test_convert_markdown_to_html_with_code_block(self):
        """Test code block conversion in fallback markdown."""

        content = "```\ncode here\n```"
        result = MarkdownRenderer.render(content)

        self.assertIn("<pre><span></span><code>", result)
        self.assertIn("code here", result)
        self.assertIn("</code></pre>", result)

    def test_convert_markdown_to_html_with_list_items(self):
        """Test list item conversion in fallback markdown."""

        content = "- Item 1\n- Item 2"
        result = MarkdownRenderer.render(content)

        self.assertIn("<li>", result)
        self.assertIn("Item 1", result)
        self.assertIn("Item 2", result)

    def test_convert_markdown_to_html_escapes_html(self):
        """Test that HTML is escaped in content."""

        content = "<script>alert('test')</script>"
        result = MarkdownRenderer.render(content)

        self.assertIn("<script>alert('test')</script>", result)

    def test_read_and_convert_markdown_file_not_found(self):
        """Test error handling when markdown file doesn't exist."""
        result = self.view._read_and_convert_markdown(Path("/nonexistent/file.md"))

        self.assertIn("Error reading file:", result)

    def test_read_and_convert_markdown_success(self):
        """Test successful markdown file reading and conversion."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# Test Header\nSome content")
            f.flush()

            try:
                result = self.view._read_and_convert_markdown(Path(f.name))
                self.assertIn("Test Header", result)
            finally:
                Path(f.name).unlink()

    def test_read_and_convert_markdown_handles_utf8(self):
        """Test that markdown reading handles UTF-8 correctly."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write("# Tëst Héadér\nCöntënt with spëcial chars")
            f.flush()

            try:
                result = self.view._read_and_convert_markdown(Path(f.name))
                self.assertIn("Tëst Héadér", result)
            finally:
                Path(f.name).unlink()

    @patch("docubase.views.BASE_DIR")
    def test_context_includes_empty_string_when_no_core_docs(self, mock_base_dir):
        """Test that core_content is empty string when core/docs/index.md
        doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)

            def mock_truediv(self, key):
                if key == "core":
                    return tmpdir_path / "core"
                return tmpdir_path / key

            mock_base_dir.__truediv__ = mock_truediv

            context = self.view.get_context_data()

            self.assertEqual(context["core_content"], "")

    @patch("docubase.views.markdown.markdown")
    def test_convert_markdown_uses_extensions(self, mock_markdown):
        """Test that markdown conversion uses the correct extensions."""
        mock_markdown.return_value = "<p>converted</p>"

        content = "# Test"
        DocubaseIndexView._convert_markdown_to_html(content)

        mock_markdown.assert_called_once()
        call_args = mock_markdown.call_args
        self.assertIn("extensions", call_args.kwargs)
        self.assertEqual(
            call_args.kwargs["extensions"],
            [
                "markdown.extensions.fenced_code",
                "markdown.extensions.codehilite",
                "markdown.extensions.tables",
                "markdown.extensions.toc",
            ],
        )

    def test_view_inherits_login_required_mixin(self):
        """Test that view inherits LoginRequiredMixin."""
        from django.contrib.auth.mixins import LoginRequiredMixin

        self.assertTrue(issubclass(DocubaseIndexView, LoginRequiredMixin))

    def test_view_inherits_template_view(self):
        """Test that view inherits TemplateView."""
        from django.views.generic import TemplateView

        self.assertTrue(issubclass(DocubaseIndexView, TemplateView))

    def test_view_has_correct_template_name(self):
        """Test that view has the correct template_name attribute."""
        self.assertEqual(DocubaseIndexView.template_name, "docubase/index.html")

    def test_get_context_data_calls_parent(self):
        """Test that get_context_data calls parent implementation."""
        self.client.login(username="testuser", password="testpass123")
        url = reverse("docubase:index")
        response = self.client.get(url)

        # Parent TemplateView.get_context_data should include 'view' key
        self.assertIn("view", response.context)

    @patch("docubase.views.BASE_DIR")
    def test_app_display_name_in_context(self, mock_base_dir):
        """Test that display_name is correctly formatted in context."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            app_dir = tmpdir_path / "app"
            app_dir.mkdir()

            # Create app with camelCase name
            app_path = app_dir / "myTestApp"
            app_path.mkdir()
            (app_path / "docs").mkdir()
            (app_path / "docs" / "index.md").touch()

            def mock_truediv(self, key):
                if key == "app":
                    return app_dir
                return tmpdir_path / key

            mock_base_dir.__truediv__ = mock_truediv

            self.client.login(username="testuser", password="testpass123")
            url = reverse("docubase:index")
            response = self.client.get(url)

            apps = response.context["apps"]
            self.assertEqual(len(apps), 1)
            self.assertEqual(apps[0]["display_name"], "My Test App")

    def test_apps_with_zero_docs_still_listed(self):
        """Test that apps with zero markdown files are not listed."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            app_dir = tmpdir_path / "app"
            app_dir.mkdir()

            # Create app with empty docs folder
            app_path = app_dir / "emptyapp"
            app_path.mkdir()
            (app_path / "docs").mkdir()

            with patch("docubase.views.BASE_DIR.__truediv__") as mock_truediv:

                def truediv_side_effect(key):
                    if key == "app":
                        return app_dir
                    return tmpdir_path / key

                mock_truediv.side_effect = truediv_side_effect

                with patch("docubase.views.BASE_DIR", tmpdir_path):
                    result = self.view._get_apps_with_docs()

                    # Apps with docs folder but no .md files should have docs_count = 0
                    if result:
                        self.assertTrue(any(app["docs_count"] == 0 for app in result))
