# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-slim

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app


# Install Packages (basic tools, cups, basic drivers, HP drivers)
RUN apt-get update \
    && apt-get install -y \
    sudo \
    cups-client \
    cups-bsd \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Add user and disable sudo password checking
RUN useradd \
    --groups=sudo,lp,lpadmin \
    --create-home \
    --home-dir=/home/print \
    --shell=/bin/bash \
    --password=$(mkpasswd print) \
    print \
    && sed -i '/%sudo[[:space:]]/ s/ALL[[:space:]]*$/NOPASSWD:ALL/' /etc/sudoers

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
RUN usermod -a -G lpadmin appuser
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "main:app"]
