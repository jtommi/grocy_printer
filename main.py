import os

from fastapi import FastAPI
from zebra import Zebra

from src.label import generate_label, load_template
from src.product import Product


app = FastAPI()

template = load_template("template.zpl")

name_split = int(os.getenv("LINELENGTH", default=15))
printer_name = os.getenv("PRINTER", default="zebra")

printer = Zebra(printer_name)

@app.post("/printer/product", status_code=201)
async def print_product(product: Product):
    label = generate_label(template, product, name_split)

    printer.output(label)

    return {"zpl": label}
