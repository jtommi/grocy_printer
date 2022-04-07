from fastapi import Body, FastAPI, HTTPException
import logging
from string import Template
from datetime import datetime

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)

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


@app.post("/printer/product")
async def print_product(payload: dict = Body(...)):
    try:
        due_date = payload["due_date"].split(" ")[-1]
        due_date = datetime.strptime(due_date, "%Y-%m-%d")
        due_date = due_date.strftime("%d/%m/%y")

        if len(payload["product"]) > name_split and payload["product"].count(" ") > 0:
            name1 = payload["product"].split(" ")[0][:name_split]
            name2 = "".join(payload["product"].split(" ")[1:])[:name_split]
        else:
            name1 = payload["product"][:name_split]
            name2 = payload["product"][name_split : name_split * 2]

        label = template.substitute(
            barcode=payload["grocycode"], name1=name1, name2=name2, date=due_date
        )

        return {"zpl": label}

    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))
