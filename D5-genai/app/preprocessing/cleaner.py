import re
from html.parser import HTMLParser


class HTMLTextExtractor(HTMLParser):
    """Convert HTML into readable text while preserving headings."""

    HEADING_TAGS = {
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
    }

    BLOCK_TAGS = {
        "p",
        "div",
        "section",
        "article",
        "li",
        "ul",
        "ol",
        "br",
        "tr",
    }

    def __init__(self) -> None:
        super().__init__()

        self.parts: list[str] = []
        self.current_heading: str | None = None

    def handle_starttag(
        self,
        tag: str,
        attrs,
    ) -> None:

        tag = tag.lower()

        if tag in self.HEADING_TAGS:
            self.current_heading = tag

        elif tag in self.BLOCK_TAGS:
            self.parts.append("\n")

    def handle_endtag(
        self,
        tag: str,
    ) -> None:

        tag = tag.lower()

        if tag in self.HEADING_TAGS:

            self.parts.append("\n")
            self.current_heading = None

        elif tag in self.BLOCK_TAGS:

            self.parts.append("\n")

    def handle_data(
        self,
        data: str,
    ) -> None:

        text = data.strip()

        if not text:
            return

        if self.current_heading:

            prefix = "#" * int(
                self.current_heading[1]
            )

            self.parts.append(
                f"\n{prefix} {text}\n"
            )

        else:

            self.parts.append(
                f" {text} "
            )


def html_to_text(
    html: str,
) -> str:

    parser = HTMLTextExtractor()

    parser.feed(html)
    parser.close()

    return "".join(parser.parts)


def clean_text(
    text: str,
    source_extension: str = "",
) -> str:

    if not text:
        return ""

    text = text.replace(
        "\r\n",
        "\n",
    )

    text = text.replace(
        "\r",
        "\n",
    )

    if source_extension.lower() in {
        ".html",
        ".htm",
    }:

        text = html_to_text(text)

    # Remove HTML comments.
    text = re.sub(
        r"<!--.*?-->",
        "",
        text,
        flags=re.DOTALL,
    )

    # Normalize spaces and tabs.
    text = re.sub(
        r"[ \t]+",
        " ",
        text,
    )

    # Normalize excessive blank lines.
    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text,
    )

    cleaned_lines = []

    for line in text.split("\n"):

        line = line.strip()

        if not line:
            continue

        # Remove whitespace before markdown headings.
        line = re.sub(
            r"^(#{1,6})\s+",
            r"\1 ",
            line,
        )

        cleaned_lines.append(line)

    return "\n".join(
        cleaned_lines
    ).strip()