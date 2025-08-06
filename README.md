# Grocy printer

## Overview

This project provides a label printing solution for [Grocy](https://grocy.info/), a self-hosted groceries and household management solution.  
It listens for new label requests from the Grocy server and prints them using a CUPS server, specifically targeting Zebra printers.

## Code Structure

- **product.py**  
    Defines the `Product` Pydantic model, representing a Grocy product with attributes such as name, Grocy code, and due date.

- **label.py**  
    Contains utilities for label generation, including ZPL (Zebra Programming Language) template handling.  
    - `Label` and `ZPL` Pydantic models represent the label content.
    - Functions:
        - `load_template(template_file: str)`: Loads and processes a ZPL template file.
        - `generate_label(template: Template, product: Product, name_split: int)`: Generates a ZPL label for a given product.

- **main.py**  
    The main FastAPI application that:
    - Configures logging and loads configuration from environment variables.
    - Provides endpoints to print labels and product labels:
        - `POST /printer/label`: Prints a label using provided ZPL content.
        - `POST /printer/product`: Generates and prints a product label from product data.
    - Handles request validation errors with formatted responses.


## Configuration

The application is configured using environment variables, which can be set in the `docker-compose.yml` file or passed directly to the container:

- **CUPS_SERVER**: Hostname of the CUPS server (default: `cups`).
- **LINELENGTH**: Maximum length for product names on labels (default: `15`).
- **PRINTER**: Name of the target printer/print queue as recognized by CUPS (default: `zebra`).
- **DEV**: If set, disables actual printing for development/testing.

You can adjust these variables in the `environment` section of `docker-compose.yml` to match your setup.

## Deployment

1. **Build and Start the Stack**  
    Run the following command in the project directory to build and start both the application and the CUPS server:
    ```sh
    docker-compose up -d --build
    ```

2. **Access the CUPS Web Interface**  
    Once running, open [http://localhost:631](http://localhost:631) in your browser.  
    - Login with the credentials specified in `docker-compose.yml` (default: `print`/`print`).
    - Add and configure your Zebra printer using the CUPS interface.

3. **Application Endpoints**  
    The FastAPI application will be available at [http://localhost:8000](http://localhost:8000).  
    - Use the `/printer/label` and `/printer/product` endpoints to print labels.

4. **Printer Configuration**  
    Ensure the printer name in the environment variable `PRINTER` matches the name configured in CUPS.  
    If unsure, you can list available printers in the [CUPS interface](http://localhost:631) or by running:
    ```sh
    docker exec -it grocy_printer lpstat -p
    ```

5. **Volumes and Persistence**  
    The CUPS container uses Docker volumes (`cups_config`, `cups_services`) to persist configuration and printer settings across restarts.

## Notes

- The application runs as a non-root user for security.
- The CUPS server is isolated in its own container, and the application communicates with it via the network.
- For USB printers, ensure your Docker host provides access to the relevant devices.  
