
FROM python:3.7-slim

RUN mkdir /app

COPY requirements.txt /app

RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY api_foodgramm/ /app

COPY fonts/ /usr/share/fonts

WORKDIR /app

CMD ["gunicorn", "api_foodgramm.wsgi:application", "--bind", "0:8000" ]
