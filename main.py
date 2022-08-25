import logging
import os

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from zebra import Zebra

from src.label import generate_label, load_template
from src.product import Product

# Configure logging
uvicorn_logger = logging.getLogger("uvicorn")
access_logger = logging.getLogger("uvicorn.access")
loggers = [uvicorn_logger, access_logger]
stream_formatter = logging.Formatter("%(asctime)s - %(levelname)s : %(message)s")
for logger in loggers:
    if logger.hasHandlers():
        stream_handler = logger.handlers[0]
    else:
        stream_handler = logging.StreamHandler()

    stream_handler.setFormatter(stream_formatter)

    if not logger.hasHandlers():
        logger.addHandler(stream_handler)

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


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f"{exc}".replace("\n", " ").replace("   ", " ")
    uvicorn_logger.error(f"{exc.body}: {exc_str}")
    content = {"message": exc_str, "body": exc.body}
    return JSONResponse(
        content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )
