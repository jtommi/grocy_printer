from datetime import datetime
from string import Template

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from zebra import Zebra


class Product(BaseModel):
    product: str
    grocycode: str
    font_family: str = None
    due_date: str


app = FastAPI()

template = ""
with open("template.zpl", "r") as file:
    lines = file.readlines()
    for index, line in enumerate(lines):
        if line.startswith("^FX"):
            continue
        template += line.strip()
    template = Template(template)

name_split = 11


@app.post("/printer/product", status_code=201)
async def print_product(product: Product):
    try:
        due_date = product["due_date"].split(" ")[-1]
        due_date = datetime.strptime(due_date, "%Y-%m-%d")
        due_date = due_date.strftime("%d/%m/%y")

        if len(product["product"]) > name_split and product["product"].count(" ") > 0:
            name1 = product["product"].split(" ")[0][:name_split]
            name2 = "".join(product["product"].split(" ")[1:])[:name_split]
        else:
            name1 = product["product"][:name_split]
            name2 = product["product"][name_split : name_split * 2]

        label = template.substitute(
            barcode=product["grocycode"], name1=name1, name2=name2, date=due_date
        )

        printer = Zebra("zebra")
        printer.output(label)

        return {"zpl": label}

    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))
