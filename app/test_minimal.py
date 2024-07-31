from fasthtml.common import *

app, rt = fast_app(debug=True)


@rt("/")
def get():
    return Div(H1("Hello, World!"), P("This is a simple test route."))


serve()
