from fasthtml.common import Html, Script, Style, Template
from fasthtml.components import Zero_md
from pathlib import Path


def md(md_content_or_path, css=""):
    """
    Render Markdown content or load and render a Markdown file using zero-md in FastHTML.

    Parameters:
    md_content_or_path (str or Path): The Markdown content or path to a .md file.
    css (str): Optional CSS to be applied to the rendered Markdown.

    Returns:
    Html: A FastHTML Html component containing the rendered Markdown.
    """
    if isinstance(md_content_or_path, (str, Path)):
        path = Path(md_content_or_path)
        if path.exists() and path.suffix.lower() == ".md":
            with open(path, "r", encoding="utf-8") as f:
                md_content = f.read()
        else:
            md_content = md_content_or_path
    else:
        md_content = md_content_or_path

    css_template = Template(Style(css), data_append=True)

    zero_md_component = Zero_md(css_template, Script(md_content, type="text/markdown"))

    zeromd_headers = [Script(type="module", src="https://cdn.jsdelivr.net/npm/zero-md@3?register")]

    return Html(*zeromd_headers, zero_md_component)
