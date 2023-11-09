FROM python:3.11-alpine

RUN mkdir /code

WORKDIR /code

COPY . .

RUN pip install -r ./requirements.txt

CMD ["gunicorn", "new.wsgi:application", "--bind", "0.0.0.0:8000"]



