FROM python:3.9-slim

WORKDIR /usr/src/etl

RUN apt-get update && apt-get install -y wget unzip && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb && \
    apt-get clean

# Copy just the requirements files and install them
COPY tools/requirements_tools.txt requirements_tools.txt
COPY etl/requirements_etl.txt requirements_etl.txt

# Copy the database file ONLY if exists
RUN if [ -f etl/public/database.json ]; then cp etl/public/database.json public/database.json; else echo "No database.json file found"; fi

# Install the requirements
RUN pip install -r requirements_tools.txt
RUN pip install -r requirements_etl.txt


# Now copy the rest of your application
COPY etl .
COPY tools /usr/src/tools

ENV PYTHONPATH /usr/src

CMD ["python", "run.py"]
