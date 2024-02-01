FROM python:3.8-slim

WORKDIR /usr/src/app

COPY app .

COPY tools /usr/src/tools

ENV PYTHONPATH /usr/src

RUN pip install --no-cache-dir -r requirements_app.txt

EXPOSE 5000

ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app"

ENV FLASK_ENV=development

ENV FLASK_APP=app.py

CMD ["flask", "run", "--host=0.0.0.0"]
