FROM python:3.7-slim

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt /

RUN pip3 install -r /requirements.txt --no-cache-dir

COPY api_foodgramm/ /

COPY fonts/ /usr/share/fonts

WORKDIR /

CMD ["gunicorn", "api_foodgramm.wsgi:application", "--bind", "0:8000" ]
