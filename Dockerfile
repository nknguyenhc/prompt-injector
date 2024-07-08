FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

RUN python manage.py migrate && python setup.py

EXPOSE 80

CMD gunicorn --bind 0.0.0.0:80 "prompt_injector.wsgi:application"
