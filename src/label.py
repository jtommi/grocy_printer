import os
from datetime import datetime
from string import Template

import pendulum

from src.product import Product


def load_template(template_file: str) -> Template:
    template = ""
    # Remove comments and newlines from the ZPL template
    with open(template_file, "r") as file:
        lines = file.readlines()
        for _, line in enumerate(lines):
            if line.startswith("^FX"):
                continue
            template += line.strip()
        return Template(template)


def generate_label(template: Template, product: Product, name_split: int) -> str:
    due_date = product.due_date.split(" ")[-1]
    due_date = datetime.strptime(due_date, "%Y-%m-%d")
    due_date = due_date.strftime("%d / %m / %y")

    if len(product.name) > name_split and product.name.count(" ") > 0:
        name1 = product.name.split(" ")[0][:name_split]
        name2 = " ".join(product.name.split(" ")[1:])[:name_split]
    else:
        name1 = product.name[:name_split]
        name2 = product.name[name_split : name_split * 2]

    tz = pendulum.timezone(os.getenv("TZ", "UTC"))
    return template.substitute(
        barcode=product.grocycode,
        name1=name1,
        name2=name2,
        due_date=due_date,
        print_date=datetime.now(tz).strftime("%d/%m/%y"),
    )
