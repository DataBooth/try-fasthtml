from fasthtml.common import *

app, rt = fast_app()


@rt("/")
def get():
    return Div(
        H1("FastHTML Capabilities Showcase"),
        P("Explore the various features of FastHTML below:"),
        Ul(
            Li(A("Basic Elements", href="/elements")),
            Li(A("Interactivity", href="/interactivity")),
            Li(A("Routing", href="/routing")),
        ),
    )


@rt("/elements")
def get():
    return Div(
        H2("Basic Elements"),
        P("This is a paragraph."),
        Img(src="https://via.placeholder.com/150", alt="Placeholder Image"),
        A("Back to Home", href="/"),
    )


@rt("/interactivity")
def get():
    return Div(
        H2("Interactivity"),
        P("Click the button to change the text below:"),
        Button("Click Me", hx_get="/change_text"),
        Div(id="text_div", children=[P("Original Text")]),
        A("Back to Home", href="/"),
    )


@rt("/change_text")
def get():
    return P("Text Changed!")


@rt("/routing")
def get():
    return Div(
        H2("Routing"),
        P("This page demonstrates routing in FastHTML."),
        A("Back to Home", href="/"),
    )


serve()
