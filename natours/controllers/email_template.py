from pathlib import Path

html_template_path = (
    Path(__file__).parent.resolve().parent / "public" / "html" / "email_template.html"
)

print(html_template_path)


def render_email_html(body_template: str):
    with open(html_template_path, "r+") as fp:
        html = fp.read()

        email_html = html.replace("<!-- CONTENT-->", body_template)

    return email_html
