import duckdb
import markdown
import pandas as pd
import toml
from fasthtml.common import (
    H1,
    Button,
    Div,
    Form,
    Input,
    MarkdownJS,
    P,
    Style,
    Table,
    Td,
    Th,
    Tr,
    Ul,
    fast_app,
    serve,
)


def render_markdown(md_content):
    """
    Convert Markdown content to FastHTML components.
    
    Parameters:
    md_content (str): The Markdown content to be converted.
    
    Returns:
    Div: A FastHTML Div containing the rendered content.
    """
    html_content = markdown.markdown(md_content)
    
    # Parse the HTML content and convert it to FastHTML components
    components = []
    for line in html_content.split('\n'):
        if line.startswith('<h1>'):
            components.append(H1(line[4:-5]))
        elif line.startswith('<h2>'):
            components.append(H2(line[4:-5]))
        elif line.startswith('<h3>'):
            components.append(H3(line[4:-5]))
        elif line.startswith('<p>'):
            components.append(P(line[3:-4]))
        elif line.startswith('<ul>'):
            ul_items = []
            for item in line[4:-5].split('<li>'):
                if item:
                    ul_items.append(Li(item.strip('</li>')))
            components.append(Ul(*ul_items))
        # Add more conditions for other HTML elements as needed
    
    return Div(*components)

class DataSource:
    def __init__(self, config):
        self.config = config
        self.con = duckdb.connect(":memory:")
        self.table_name = self.load_data(table_name=self.config["data"]["table_name"])
        self.default_query = f"{self.config['data']['default_query']}".replace(
            "{table_name}", self.table_name
        )

    def load_data(self, table_name="movies"):
        url = self.config["data"]["url"]
        df = pd.read_csv(url, delimiter=self.config["data"]["delimiter"])
        self.con.execute(f"CREATE TABLE {table_name} AS SELECT * FROM df")
        return table_name

    def execute_query(self, query):
        return self.con.execute(query).fetchdf()


class MovieDataApp:
    def __init__(self, config):
        self.config = config
        self.app, self.rt = fast_app(debug=True)
        self.data_source = DataSource(config)
        self.setup_routes()
        self.load_styles()

    def setup_routes(self):
        self.rt("/")(self.get)
        self.rt("/query", methods=["POST"])(self.query)

    def load_styles(self):
        css_file = self.config["styles"]["dataframe_css"]
        with open(css_file, "r") as f:
            self.dataframe_style = f.read()

    def get(self):
        result = self.data_source.execute_query(self.data_source.default_query)
        return Div(
            Style(self.dataframe_style),
            H1(f"Data Display - {self.data_source.table_name} table"),
            P("Top 5 Occupations by User Count:"),
            render_markdown(f"`{self.data_source.default_query}`"),
            self.create_table(result),
            P("Enter your SQL query:"),
            Form(
                Input(type="text", name="query", placeholder="Enter SQL query here"),
                Button("Submit", type="submit"),
                hx_post="/query",
            ),
        )

    async def query(self, request):
        form_data = await request.form()
        query = form_data.get("query", "")
        result = self.data_source.execute_query(query)
        return Div(Style(self.dataframe_style), H1("Query Results"), self.create_table(result))

    def create_table(self, df):
        return Table(
            # {"class": "dataframe"},
            Tr(*[Th(col) for col in df.columns]),
            *[Tr(*[Td(cell) for cell in row]) for row in df.values],
        )

    def serve(self, host="127.0.0.1", port=5001):
        serve(host=host, port=port)


config = toml.load("app/config.toml")

movie_app = MovieDataApp(config)
app = movie_app.app

if __name__ == "__main__":
    movie_app.serve(host=config["server"]["host"], port=config["server"]["port"])
