from datetime import datetime
from string import Template

import pandas as pd


def read_template(file: str) -> Template:
    with open(file, "r") as f:
        content = f.read()
    return Template(content)


df = pd.read_csv("export.csv")
df = df.astype(
    {
        "repository_stars_count": "Int64",
    }
)
df = df.fillna(
    {
        "repository_domain": "",
        "description": "",
        "repository_last_update": "",
        "distribution": "",
    }
)

header = (
    "<thead>\n"
    "<tr>\n"
    "<th>Name</th>\n"
    "<th>Repository</th>\n"
    "<th>Repository Stars Count</th>\n"
    "<th>Repository Last Update</th>\n"
    "<th>Repository Domain</th>\n"
    "<th>Categories</th>\n"
    "<th>Compatibility</th>\n"
    "<th>Frameworks</th>\n"
    "<th>Distribution</th>\n"
    "<th>Description</th>\n"
    "</tr>\n"
    "</thead>\n"
)

table_data = "<tbody>\n"
for index, row in df.iterrows():
    name = f"<a href='{row['url']}'>{row['name']}</a></td>"
    table_data += (
        "<tr>\n"
        "<td>"
        f"{name}"
        "\n"
        f"<td><a href='{row['repository']}'>{row['repository']}</a></td>"
        "\n"
        f"<td>{row['repository_stars_count']}</td>"
        "\n"
        f"<td>{row['repository_last_update']}</td>"
        "\n"
        f"<td>{row['repository_domain']}</td>"
        "\n"
        f"<td>{row['categories']}</td>"
        "\n"
        f"<td>{row['compatibility']}</td>"
        "\n"
        f"<td>{row['frameworks']}</td>"
        "\n"
        f"<td>{row['distribution']}</td>"
        "\n"
        f"<td>{row['description']}</td>"
        "\n"
        "</tr>\n"
    )
table_data += "</tbody>\n"

date_update = datetime.today().strftime("%Y-%m-%d")

formatted_message = read_template("template.html").safe_substitute(
    {"date_update": date_update, "header": header, "table_data": table_data}
)
with open("docs/index.html", "w") as f:
    f.write(formatted_message)
