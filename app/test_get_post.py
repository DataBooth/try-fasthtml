from fasthtml.common import *  # fast_app, serve, Div, P, Form, Input, Button

app, rt = fast_app(debug=True)


@rt("/")
def get():
    return Div(
        P("Submit your name:"),
        Form(
            Input(type="text", name="name"),
            Button("Submit", type="submit"),
            hx_post="/submit",
        ),
    )


@rt("/submit", methods=["POST"])
async def post(request):
    form_data = await request.form()
    name = form_data.get("name", "Guest")
    return P(f"Hello, {name}!")


serve()
