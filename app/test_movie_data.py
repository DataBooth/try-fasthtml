import duckdb
from fasthtml.common import fast_app, serve, Div, H1, P, Table, Tr, Td, Th
import pandas as pd

# Download the dataset
url = "https://raw.githubusercontent.com/justmarkham/DAT8/master/data/u.user"
df = pd.read_csv(url, delimiter="|")

# Connect to DuckDB and load the dataset
con = duckdb.connect()
con.execute("CREATE TABLE movies AS SELECT * FROM df;")

app, rt = fast_app(debug=True)


@rt("/")
def get():
    result = con.execute(
        "SELECT occupation, COUNT(*) AS count FROM movies GROUP BY occupation ORDER BY count DESC LIMIT 5;"
    ).fetchall()
    print(result)
    return Div(
        H1("DuckDB Data Display"),
        P("Top 5 Occupations by User Count:"),
        Table(
            Tr(Th("Occupation"), Th("Count")),
            *[Tr(Td(row[0]), Td(row[1])) for row in result],
        ),
    )


serve()
