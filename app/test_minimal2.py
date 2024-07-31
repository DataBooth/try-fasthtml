from fasthtml.common import *

app, rt = fast_app()


@rt("/")
def home():
    return Div(P("Hello World!"), hx_get="/change")


@rt("/change")
def change_text():
    return P("Nice to be here!")


serve()
