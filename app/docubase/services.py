import markdown


class MarkdownRenderer:
    """A simple Markdown renderer that converts markdown text to HTML."""

    @staticmethod
    def render(markdown_text):
        return markdown.markdown(
            markdown_text,
            extensions=[
                "fenced_code",
                "codehilite",
                "tables",
                "toc",
                "nl2br",
            ],
            extension_configs={
                "codehilite": {
                    "guess_lang": False,
                },
                "toc": {
                    "permalink": True,
                },
            },
        )
